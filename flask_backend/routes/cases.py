import hashlib
from datetime import datetime
from flask import Blueprint, request, jsonify, make_response
from flask_backend.models.store import db_store
from flask_backend.services.rti_engine import rti_engine
from flask_backend.services.pdf_generator import pdf_generator
from flask_backend.services.legal_engine import legal_engine
from flask_backend.services.geo_locator import geo_locator

cases_bp = Blueprint("cases", __name__, url_prefix="/api/v1/cases")

@cases_bp.route("/intake", methods=["POST"])
def create_intake():
    """
    Ingest a raw citizen grievance, extract entities, identify nearest PIO jurisdiction with Haversine distance,
    generate IPC/BNS statutory analysis, and create a case entry in NEEDS_REVIEW status.
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
        query_terms = [search_query]
        if search_query in ("varanasi", "banaras", "kashi", "vns", "assi", "sigra"):
            query_terms = ["varanasi", "banaras", "kashi", "vns", "assi", "sigra"]

        for c in filtered:
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
        "at_risk": len([c for c in all_cases if c.get("confidence", {}).get("risk_level") in ("MEDIUM", "HIGH")]),
        "total": len(all_cases)
    }

    return jsonify({
        "cases": filtered,
        "counts": counts
    }), 200

@cases_bp.route("/compliance-radar", methods=["GET"])
def get_compliance_radar():
    """
    Government Desk PIO Compliance Radar Endpoint.
    Returns real-time SLA metrics, Section 20(1) penalty sums, and Deemed Refusal statistics.
    """
    metrics = db_store.get_compliance_radar_metrics()
    return jsonify({"status": "success", "compliance_radar": metrics}), 200

@cases_bp.route("/nearest-pio", methods=["GET"])
def find_nearest_pio_endpoint():
    """Live geocoding lookup finding the nearest PIO and FAA for an address and department."""
    address = request.args.get("address", "")
    department = request.args.get("department", "Revenue & Land Records")
    narrative = request.args.get("narrative", "")

    result = geo_locator.find_nearest_public_authority(
        category=department,
        address=address,
        narrative=narrative
    )
    return jsonify({"status": "success", "nearest_public_authority": result}), 200

@cases_bp.route("/custom-acts", methods=["GET"])
def list_custom_acts():
    """Retrieve all lawyer-defined custom Acts & Sections."""
    acts = db_store.get_custom_acts()
    return jsonify({"status": "success", "custom_acts": acts}), 200

@cases_bp.route("/custom-acts", methods=["POST"])
def create_custom_act():
    """Add a new lawyer-defined Act, Section or statutory citation."""
    data = request.get_json() or {}
    act_title = data.get("act_title", "").strip()
    section = data.get("section", "").strip()

    if not act_title or not section:
        return jsonify({"error": "Bad Request", "message": "act_title and section are required"}), 400

    new_act = db_store.add_custom_act(data)

    # If a linked case ID was provided, apply immediately
    linked_case_id = data.get("linked_case_id")
    if linked_case_id:
        db_store.apply_custom_act_to_case(linked_case_id, new_act["act_id"], actor=data.get("added_by", "Advocate Counsel"))

    return jsonify({"status": "created", "custom_act": new_act}), 201

@cases_bp.route("/custom-acts/<act_id>", methods=["DELETE"])
def delete_custom_act_endpoint(act_id):
    """Delete a lawyer-defined custom Act."""
    success = db_store.delete_custom_act(act_id)
    if not success:
        return jsonify({"error": "Not Found", "message": f"Custom act {act_id} not found"}), 404
    return jsonify({"status": "deleted", "message": f"Custom act {act_id} deleted successfully."}), 200

@cases_bp.route("/<case_id>/apply-custom-act", methods=["POST"])
def apply_custom_act_endpoint(case_id):
    """Link a custom act to an active case docket."""
    data = request.get_json() or {}
    act_id = data.get("act_id")
    actor = data.get("reviewer", "Advocate Counsel")

    if not act_id:
        return jsonify({"error": "Bad Request", "message": "act_id is required"}), 400

    updated_case = db_store.apply_custom_act_to_case(case_id, act_id, actor=actor)
    if not updated_case:
        return jsonify({"error": "Not Found", "message": "Case or Act ID not found"}), 404

    return jsonify({"status": "applied", "message": f"Custom act {act_id} applied to case {case_id}.", "case": updated_case}), 200

@cases_bp.route("/<case_id>", methods=["GET"])
def get_case_detail(case_id):
    case = db_store.get_case(case_id)
    if not case:
        return jsonify({"error": "Not Found", "message": f"Case {case_id} does not exist"}), 404
    return jsonify({"case": case}), 200

@cases_bp.route("/<case_id>/appeal", methods=["GET", "POST"])
def get_or_create_first_appeal(case_id):
    """Generates / Retrieves First Appeal draft under Section 19(1) of RTI Act 2005."""
    case = db_store.get_case(case_id)
    if not case:
        return jsonify({"error": "Not Found", "message": f"Case {case_id} not found"}), 404

    appeal_draft = legal_engine.generate_first_appeal_draft(case)
    case["first_appeal_draft"] = appeal_draft
    db_store.update_case(case_id, {"first_appeal_draft": appeal_draft})

    return jsonify({"status": "success", "appeal": appeal_draft}), 200

@cases_bp.route("/<case_id>/legal-notice", methods=["GET", "POST"])
def get_or_create_legal_notice(case_id):
    """Generates / Retrieves Advocate Legal Notice under Section 80 CPC & IPC/BNS."""
    case = db_store.get_case(case_id)
    if not case:
        return jsonify({"error": "Not Found", "message": f"Case {case_id} not found"}), 404

    legal_info = case.get("statutory_legal_analysis") or legal_engine.analyze_legal_standing(
        case.get("raw_grievance", ""),
        case.get("department", "Revenue & Land Records")
    )
    notice_draft = legal_engine.generate_legal_notice_draft(case, legal_info)
    case["legal_notice_draft"] = notice_draft
    db_store.update_case(case_id, {"legal_notice_draft": notice_draft})

    return jsonify({"status": "success", "legal_notice": notice_draft}), 200

@cases_bp.route("/<case_id>/transfer-sec6-3", methods=["POST"])
def execute_transfer_sec6_3(case_id):
    """Executes Section 6(3) 5-Day Mandatory Transfer of RTI Application to Competent Public Authority."""
    data = request.get_json() or {}
    new_dept = data.get("target_department")
    reason = data.get("transfer_reason", "Subject matter pertains to transferee public authority.")
    actor = data.get("reviewer", "Designated PIO Desk Officer")

    if not new_dept:
        return jsonify({"error": "Bad Request", "message": "target_department is required"}), 400

    updated_case = db_store.transfer_case_sec6_3(case_id, new_dept, reason, officer_actor=actor)
    if not updated_case:
        return jsonify({"error": "Not Found", "message": f"Case {case_id} not found"}), 404

    return jsonify({
        "status": "transferred",
        "message": f"Case {case_id} successfully transferred to {new_dept} under Section 6(3).",
        "case": updated_case
    }), 200

@cases_bp.route("/<case_id>/update-complainant", methods=["POST"])
def update_complainant_in_place(case_id):
    """In-place update of complainant name, address, contact, or narrative for a specific case ID."""
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

    user_locality = case.get("confidence", {}).get("user_locality", "Local Division")
    dept = case.get("department", "Revenue & Land Records")

    matched_pio = rti_engine.get_pio_for_dept_and_location(
        category=dept,
        user_locality=user_locality,
        user_address=new_address,
        grievance_text=new_narrative
    )
    case["suggested_pio"] = matched_pio
    case["suggested_faa"] = matched_pio.get("faa")

    case["draft_rti"]["questions"] = rti_engine._generate_rti_questions(
        new_narrative.lower(),
        new_name,
        user_locality,
        dept,
        case.get("application_ref_no"),
        case.get("original_submission_date")
    )

    legal_info = legal_engine.analyze_legal_standing(new_narrative, dept)
    case["statutory_legal_analysis"] = legal_info

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
        ml_reason=case.get("confidence", {}).get("ml_prediction_reason", "Updated complainant details in-place"),
        legal_analysis=legal_info
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
        case.setdefault("confidence", {})["extracted_ref_no"] = ref_no
    if submission_date:
        case["original_submission_date"] = submission_date
        case.setdefault("confidence", {})["extracted_submission_date"] = submission_date

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
        case["suggested_faa"] = matched_pio.get("faa")
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

    legal_info = legal_engine.analyze_legal_standing(case.get("raw_grievance", ""), dept)
    case["statutory_legal_analysis"] = legal_info
    case["first_appeal_draft"] = legal_engine.generate_first_appeal_draft(case)
    case["legal_notice_draft"] = legal_engine.generate_legal_notice_draft(case, legal_info)

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
        ml_reason=case.get("confidence", {}).get("ml_prediction_reason", "Manually updated by Legal Reviewer"),
        legal_analysis=legal_info
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
    case = db_store.get_case(case_id)
    if not case:
        return jsonify({"error": "Not Found", "message": f"Case {case_id} not found"}), 404

    data = request.get_json() or {}
    actor = data.get("reviewer", "Adv. S. Kalra (Legal NGO)")

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
        case.setdefault("confidence", {})["extracted_ref_no"] = ref_no
    if submission_date:
        case["original_submission_date"] = submission_date
        case.setdefault("confidence", {})["extracted_submission_date"] = submission_date

    evidence_gaps = []
    if case.get("application_ref_no") in (None, "", "Not Provided"):
        evidence_gaps.append("Application reference/acknowledgement receipt number not specified")
    if case.get("original_submission_date") in (None, "", "Unconfirmed"):
        evidence_gaps.append("Exact submission date of original grievance unconfirmed")

    case.setdefault("confidence", {})["evidence_gaps"] = evidence_gaps
    case["confidence"]["risk_level"] = "LOW" if len(evidence_gaps) == 0 else "MEDIUM"

    if edited_draft:
        case["draft_rti"].update(edited_draft)
        case["draft_rti"]["version"] += 1

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dispatch_id = f"DSP-{hashlib.md5((case_id + now_str).encode()).hexdigest()[:8].upper()}"

    dispatch_info = {
        "dispatch_id": dispatch_id,
        "channel": data.get("channel", "Registered SpeedPost + Electronic Email"),
        "recipient_email": case.get("suggested_pio", {}).get("email"),
        "recipient_name": case.get("suggested_pio", {}).get("pio_name"),
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
        source="Legal Review Workspace",
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

    doc_type = request.args.get("type", "rti").lower()
    pdf_bytes = pdf_generator.generate_pdf_bytes(case, doc_type=doc_type)
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename="ARZI_{doc_type.upper()}_{case_id}.pdf"'
    return response
