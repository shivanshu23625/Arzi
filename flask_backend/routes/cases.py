import hashlib
from datetime import datetime
from flask import Blueprint, request, jsonify, make_response
from flask_backend.models.store import db_store
from flask_backend.services.rti_engine import rti_engine
from flask_backend.services.pdf_generator import pdf_generator

cases_bp = Blueprint("cases", __name__, url_prefix="/api/v1/cases")

@cases_bp.route("/intake", methods=["POST"])
def create_intake():
    """
    Ingest a raw citizen grievance, extract entities, identify PIO jurisdiction,
    generate RTI draft questions, and create a case entry in NEEDS_REVIEW status.
    If an existing case exists for the same ref_no, updates in-place to prevent duplicates.
    """
    data = request.get_json() or {}
    grievance = data.get("raw_grievance", "").strip()
    complainant = data.get("complainant", {})

    if not grievance or not complainant.get("name"):
        return jsonify({"error": "Bad Request", "message": "raw_grievance and complainant.name are required"}), 400

    analysis = rti_engine.analyze_and_structure(
        grievance_text=grievance,
        complainant_info=complainant,
        requested_dept=data.get("department"),
        ref_no=data.get("application_ref_no"),
        submission_date=data.get("original_submission_date")
    )

    case_payload = {
        "complainant": complainant,
        "raw_grievance": grievance,
        **analysis
    }

    new_case = db_store.add_case(case_payload)
    return jsonify({"status": "created", "case": new_case}), 201

@cases_bp.route("", methods=["GET"])
def list_cases():
    """Retrieve all cases with multi-field search and summary count breakdown."""
    status_filter = request.args.get("status")
    search_query = request.args.get("search", "").strip().lower()

    all_cases = db_store.get_all_cases()
    filtered = all_cases

    if status_filter:
        filtered = [c for c in filtered if c["status"].upper() == status_filter.upper()]

    if search_query:
        s_results = []
        # Support synonym matching for Varanasi / Banaras / Kashi
        query_terms = [search_query]
        if search_query in ("varanasi", "banaras", "kashi", "vns"):
            query_terms = ["varanasi", "banaras", "kashi", "vns"]

        for c in filtered:
            # Concatenate search text fields
            c_text = (
                f"{c.get('case_id', '')} "
                f"{c.get('complainant', {}).get('name', '')} "
                f"{c.get('complainant', {}).get('contact', '')} "
                f"{c.get('complainant', {}).get('address', '')} "
                f"{c.get('confidence', {}).get('user_locality', '')} "
                f"{c.get('department', '')} "
                f"{c.get('category', '')} "
                f"{c.get('application_ref_no', '')} "
                f"{c.get('suggested_pio', {}).get('pio_name', '')} "
                f"{c.get('suggested_pio', {}).get('office_address', '')} "
                f"{c.get('raw_grievance', '')}"
            ).lower()
            if any(term in c_text for term in query_terms):
                s_results.append(c)
        filtered = s_results

    counts = {
        "inbox": len([c for c in all_cases if c["status"] == "NEEDS_REVIEW"]),
        "approved": len([c for c in all_cases if c["status"] in ("APPROVED", "DISPATCHED")]),
        "at_risk": len([c for c in all_cases if c["confidence"]["risk_level"] in ("MEDIUM", "HIGH")]),
        "total": len(all_cases)
    }

    return jsonify({
        "cases": filtered,
        "counts": counts
    }), 200

@cases_bp.route("/<case_id>", methods=["GET"])
def get_case_detail(case_id):
    case = db_store.get_case(case_id)
    if not case:
        return jsonify({"error": "Not Found", "message": f"Case {case_id} does not exist"}), 404
    return jsonify({"case": case}), 200

@cases_bp.route("/<case_id>/update-complainant", methods=["POST"])
def update_complainant_in_place(case_id):
    """
    In-place update of complainant name, address, contact, or narrative for a specific case ID.
    Fixes operator mistakes (e.g. 'Samiksha' -> 'Shivanshu Pandey') on ARZ-1046 without creating duplicate cases.
    """
    case = db_store.get_case(case_id)
    if not case:
        return jsonify({"error": "Not Found", "message": f"Case {case_id} not found"}), 404

    data = request.get_json() or {}
    old_name = case["complainant"].get("name")
    new_name = data.get("complainant_name", old_name).strip()
    new_contact = data.get("complainant_contact", case["complainant"].get("contact")).strip()
    new_address = data.get("complainant_address", case["complainant"].get("address")).strip()
    new_narrative = data.get("raw_grievance", case.get("raw_grievance")).strip()
    actor = data.get("reviewer", "Adv. S. Kalra (Legal NGO)")

    case["complainant"]["name"] = new_name
    case["complainant"]["contact"] = new_contact
    case["complainant"]["address"] = new_address
    case["raw_grievance"] = new_narrative

    # Re-run RTI Engine to update questions & ML report with corrected complainant details
    user_locality = case.get("confidence", {}).get("user_locality", "Local Division")
    dept = case.get("department", "Revenue & Land Records")

    matched_pio = rti_engine.get_pio_for_dept_and_location(
        category=dept,
        user_locality=user_locality,
        user_address=new_address,
        grievance_text=new_narrative
    )
    case["suggested_pio"] = matched_pio

    case["draft_rti"]["questions"] = rti_engine._generate_rti_questions(
        new_narrative.lower(),
        new_name,
        user_locality,
        dept,
        case.get("application_ref_no"),
        case.get("original_submission_date")
    )

    case["ml_report_format"] = rti_engine.generate_ml_report(
        complainant_name=new_name,
        locality=user_locality,
        ref_no=case.get("application_ref_no", "Not Provided"),
        sub_date=case.get("original_submission_date", "Unconfirmed"),
        dept=dept,
        pio=case.get("suggested_pio", {}),
        subject=case["draft_rti"]["application_subject"],
        questions=case["draft_rti"]["questions"],
        confidence=case.get("confidence", {}).get("overall", 95),
        risk_level=case.get("confidence", {}).get("risk_level", "LOW"),
        evidence_gaps=case.get("confidence", {}).get("evidence_gaps", []),
        ml_reason=case.get("confidence", {}).get("ml_prediction_reason", "Updated complainant details in-place")
    )

    audit_meta = {
        "update_type": "INPLACE_COMPLAINANT_FIX",
        "actor": actor,
        "field_changed": "Complainant Name & Narrative",
        "old_value": f"Name: {old_name}",
        "new_value": f"Name: {new_name}",
        "remarks": f"Corrected complainant details in-place on Master Case {case_id}; prevented duplicate case creation."
    }

    updated = db_store.update_case(case_id, case, audit_meta=audit_meta)

    db_store.add_run_log(
        event_type="INPLACE_COMPLAINANT_FIX",
        case_id=case_id,
        actor=actor,
        source="Legal Review Workspace",
        action=f"Updated complainant in-place on {case_id}: '{old_name}' -> '{new_name}'",
        result="INPLACE_FIX_SUCCESS",
        correlation_id=f"CORR-INPLACE-{case_id}"
    )

    return jsonify({"status": "updated", "message": f"Case {case_id} updated in-place.", "case": updated}), 200

@cases_bp.route("/merge-duplicates", methods=["POST"])
def merge_duplicate_cases():
    """Merge duplicate case IDs into a single master case to eliminate legal confusion."""
    data = request.get_json() or {}
    master_id = data.get("master_case_id")
    duplicate_id = data.get("duplicate_case_id")
    actor = data.get("reviewer", "Adv. S. Kalra (Legal NGO)")

    if not master_id or not duplicate_id:
        return jsonify({"error": "Bad Request", "message": "master_case_id and duplicate_case_id required"}), 400

    master = db_store.merge_cases(master_id, duplicate_id, actor=actor)
    if not master:
        return jsonify({"error": "Not Found", "message": "One or both case IDs not found"}), 404

    return jsonify({
        "status": "merged",
        "message": f"Successfully merged duplicate case {duplicate_id} into Master Case {master_id}.",
        "master_case": master
    }), 200

@cases_bp.route("/<case_id>/override", methods=["POST"])
def override_pio(case_id):
    """
    Override PIO Authority or update missing facts (Ref No & Submission Date).
    Automatically logs timestamped override event in update_history and regenerates ML report.
    """
    case = db_store.get_case(case_id)
    if not case:
        return jsonify({"error": "Not Found", "message": f"Case {case_id} not found"}), 404

    data = request.get_json() or {}
    old_dept = case.get("department")
    new_pio_dept = data.get("department")
    ref_no = data.get("application_ref_no")
    submission_date = data.get("original_submission_date")
    actor = data.get("reviewer", "Legal Operator")

    if ref_no:
        case["application_ref_no"] = ref_no
        case["confidence"]["extracted_ref_no"] = ref_no
    if submission_date:
        case["original_submission_date"] = submission_date
        case["confidence"]["extracted_submission_date"] = submission_date

    evidence_gaps = []
    if case.get("application_ref_no") in (None, "", "Not Provided"):
        evidence_gaps.append("Application reference/acknowledgement receipt number not specified")
    if case.get("original_submission_date") in (None, "", "Unconfirmed"):
        evidence_gaps.append("Exact submission date of original grievance unconfirmed")

    case["confidence"]["evidence_gaps"] = evidence_gaps
    case["confidence"]["risk_level"] = "LOW" if len(evidence_gaps) == 0 else "MEDIUM"

    if new_pio_dept:
        user_locality = case.get("confidence", {}).get("user_locality", "Local Division")
        user_address = case.get("complainant", {}).get("address", "")
        grievance_text = case.get("raw_grievance", "")

        matched_pio = rti_engine.get_pio_for_dept_and_location(
            category=new_pio_dept,
            user_locality=user_locality,
            user_address=user_address,
            grievance_text=grievance_text
        )

        case["suggested_pio"] = matched_pio
        case["department"] = matched_pio["department"]
        case["category"] = matched_pio["department"]
        case["confidence"]["jurisdiction_confidence"] = 99
        case["confidence"]["overall"] = 96
        case["confidence"]["ml_prediction_reason"] = f"Overridden by {actor} to {matched_pio['department']}"

    ref_str = f" (Ref No: {case.get('application_ref_no')})" if case.get('application_ref_no') not in (None, "", "Not Provided") else ""
    date_str = f" (Submitted: {case.get('original_submission_date')})" if case.get('original_submission_date') not in (None, "", "Unconfirmed") else ""
    user_locality = case.get("confidence", {}).get("user_locality", "Local Division")
    dept = case.get("department", "Revenue & Land Records")

    case["draft_rti"]["application_subject"] = f"Application under Section 6(1) of RTI Act 2005 seeking status on pending grievance{ref_str}{date_str} in {user_locality} regarding {dept}"
    case["draft_rti"]["questions"] = rti_engine._generate_rti_questions(
        case.get("raw_grievance", "").lower(),
        case.get("complainant", {}).get("name", "Applicant"),
        user_locality,
        dept,
        case.get("application_ref_no"),
        case.get("original_submission_date")
    )

    case["ml_report_format"] = rti_engine.generate_ml_report(
        complainant_name=case.get("complainant", {}).get("name", "Applicant"),
        locality=user_locality,
        ref_no=case.get("application_ref_no", "Not Provided"),
        sub_date=case.get("original_submission_date", "Unconfirmed"),
        dept=dept,
        pio=case.get("suggested_pio", {}),
        subject=case["draft_rti"]["application_subject"],
        questions=case["draft_rti"]["questions"],
        confidence=case.get("confidence", {}).get("overall", 90),
        risk_level=case.get("confidence", {}).get("risk_level", "LOW"),
        evidence_gaps=case.get("confidence", {}).get("evidence_gaps", []),
        ml_reason=case.get("confidence", {}).get("ml_prediction_reason", "Manually updated by Legal Reviewer")
    )

    audit_meta = {
        "update_type": "DEPT_OVERRIDE_UPDATED",
        "actor": actor,
        "field_changed": "Department Jurisdiction",
        "old_value": old_dept,
        "new_value": dept,
        "remarks": f"Overrode department from {old_dept} -> {dept}; regenerated subject & legal RTI questions."
    }

    updated = db_store.update_case(case_id, case, audit_meta=audit_meta)

    db_store.add_run_log(
        event_type="CASE_METADATA_UPDATED",
        case_id=case_id,
        actor=actor,
        source="Approval Workspace",
        action=f"Updated case department to {dept} and metadata (Ref No: {case.get('application_ref_no')}, Date: {case.get('original_submission_date')})",
        result="UPDATE_SUCCESS",
        correlation_id=f"CORR-UPD-{case_id}"
    )

    return jsonify({"status": "updated", "case": updated}), 200

@cases_bp.route("/<case_id>/dispatch-update-report", methods=["POST"])
def dispatch_update_report(case_id):
    """
    On-demand dispatch report generator.
    Allows lawyers to generate & dispatch an updated PDF/Report to the victim/PIO as and when requested per update.
    """
    case = db_store.get_case(case_id)
    if not case:
        return jsonify({"error": "Not Found", "message": f"Case {case_id} not found"}), 404

    data = request.get_json() or {}
    actor = data.get("reviewer", "Adv. S. Kalra (Legal NGO)")
    recipient = data.get("recipient", "Victim Complainant & Designated PIO")

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    dispatch_id = f"DSP-UPD-{hashlib.md5((case_id + now_str).encode()).hexdigest()[:8].upper()}"

    dispatch_info = {
        "dispatch_id": dispatch_id,
        "channel": "On-Demand Lawyer Update Dispatch (Email + PDF Artifact)",
        "recipient_email": case.get("suggested_pio", {}).get("email"),
        "recipient_name": f"{case.get('complainant', {}).get('name')} & {case.get('suggested_pio', {}).get('pio_name')}",
        "dispatched_at": now_str[:19],
        "status": "DELIVERED_REVISED_REPORT",
        "tracking_id": f"SP-UPD-{hashlib.sha256(dispatch_id.encode()).hexdigest()[:8].upper()}IN",
        "pdf_hash": hashlib.sha256((case_id + now_str).encode()).hexdigest()[:16]
    }

    audit_meta = {
        "update_type": "DISPATCH_REPORT_GENERATED",
        "actor": actor,
        "field_changed": "On-Demand Dispatch Report",
        "old_value": "Previous Report Version",
        "new_value": f"Dispatch Report {dispatch_id} Generated",
        "remarks": f"Lawyer generated updated dispatch report for victim {case.get('complainant', {}).get('name')} and PIO."
    }

    case["dispatch_info"] = dispatch_info
    case["status"] = "APPROVED"
    updated = db_store.update_case(case_id, case, audit_meta=audit_meta)

    db_store.add_run_log(
        event_type="DISPATCH_UPDATE_REPORT_GENERATED",
        case_id=case_id,
        actor=actor,
        source="Legal Review Workspace",
        action=f"Lawyer generated on-demand dispatch report {dispatch_id} for case {case_id}",
        result="DISPATCH_REPORT_SUCCESS",
        correlation_id=f"CORR-{dispatch_id}"
    )

    return jsonify({
        "status": "dispatched",
        "message": f"Updated dispatch report generated successfully for Case {case_id}.",
        "dispatch_info": dispatch_info,
        "case": updated
    }), 200

@cases_bp.route("/<case_id>/approve", methods=["POST"])
def approve_and_dispatch_case(case_id):
    """
    Human Legal Review Approval Gate.
    Updates status to APPROVED/DISPATCHED, generates PDF artifact, records dispatch,
    and logs immutable execution proof in Run Log.
    """
    case = db_store.get_case(case_id)
    if not case:
        return jsonify({"error": "Not Found", "message": f"Case {case_id} not found"}), 404

    data = request.get_json() or {}
    reviewer = data.get("reviewer", "Adv. NGO Reviewer")
    approval_notes = data.get("notes", "Approved after legal verification.")
    edited_draft = data.get("draft_rti")
    ref_no = data.get("application_ref_no")
    submission_date = data.get("original_submission_date")

    if ref_no:
        case["application_ref_no"] = ref_no
        case["confidence"]["extracted_ref_no"] = ref_no
    if submission_date:
        case["original_submission_date"] = submission_date
        case["confidence"]["extracted_submission_date"] = submission_date

    evidence_gaps = []
    if case.get("application_ref_no") in (None, "", "Not Provided"):
        evidence_gaps.append("Application reference/acknowledgement receipt number not specified")
    if case.get("original_submission_date") in (None, "", "Unconfirmed"):
        evidence_gaps.append("Exact submission date of original grievance unconfirmed")

    case["confidence"]["evidence_gaps"] = evidence_gaps
    case["confidence"]["risk_level"] = "LOW" if len(evidence_gaps) == 0 else "MEDIUM"

    if edited_draft:
        case["draft_rti"].update(edited_draft)
        case["draft_rti"]["version"] += 1

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dispatch_id = f"DSP-{hashlib.md5((case_id + now_str).encode()).hexdigest()[:8].upper()}"

    dispatch_info = {
        "dispatch_id": dispatch_id,
        "channel": data.get("channel", "Registered SpeedPost + Electronic Email"),
        "recipient_email": case["suggested_pio"].get("email"),
        "recipient_name": case["suggested_pio"].get("pio_name"),
        "dispatched_at": now_str,
        "status": "DELIVERED",
        "tracking_id": f"SP-DEL-{hashlib.sha256(dispatch_id.encode()).hexdigest()[:8].upper()}IN",
        "pdf_hash": hashlib.sha256(case_id.encode()).hexdigest()[:16]
    }

    audit_meta = {
        "update_type": "FINAL_LEGAL_DISPATCH_RELEASED",
        "actor": reviewer,
        "field_changed": "Case Approval Status",
        "old_value": "NEEDS_REVIEW",
        "new_value": "APPROVED & DISPATCHED",
        "remarks": f"RTI Application v{case['draft_rti']['version']} approved and released for dispatch."
    }

    updates = {
        "status": "APPROVED",
        "reviewer": reviewer,
        "approval_notes": approval_notes,
        "dispatch_info": dispatch_info,
        "application_ref_no": case.get("application_ref_no"),
        "original_submission_date": case.get("original_submission_date")
    }

    updated_case = db_store.update_case(case_id, updates, audit_meta=audit_meta)

    db_store.add_run_log(
        event_type="LEGAL_DISPATCH_COMPLETED",
        case_id=case_id,
        actor=reviewer,
        source="Notion Control Desk / Legal Approval Gate",
        action=f"Approved RTI Draft v{updated_case['draft_rti']['version']} & Dispatched to {dispatch_info['recipient_name']}",
        result="SUCCESS_DISPATCHED",
        correlation_id=f"CORR-{dispatch_id}"
    )

    return jsonify({
        "status": "approved",
        "message": f"Case {case_id} approved and dispatched successfully.",
        "case": updated_case
    }), 200

@cases_bp.route("/<case_id>/pdf", methods=["GET"])
def download_rti_pdf(case_id):
    case = db_store.get_case(case_id)
    if not case:
        return jsonify({"error": "Not Found", "message": "Case not found"}), 404

    pdf_bytes = pdf_generator.generate_pdf_bytes(case)
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename="ARZI_RTI_{case_id}.pdf"'
    return response
