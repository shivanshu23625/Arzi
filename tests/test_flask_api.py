import pytest
import json
from flask_backend.app import create_app
from flask_backend.middleware.repo_validator import repo_validator

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["framework"] == "Flask 3.x Python"
    assert data["status"] == "online"

def test_list_cases(client):
    response = client.get("/api/v1/cases")
    assert response.status_code == 200
    data = response.get_json()
    assert "cases" in data
    assert "counts" in data
    assert len(data["cases"]) >= 2

def test_create_intake_case(client):
    payload = {
        "complainant": {
            "name": "Anil Kumar",
            "contact": "+91-9988776655",
            "address": "B-12, Sector 4, Rohini, Delhi",
            "language": "Hindi"
        },
        "raw_grievance": "My application for land record mutation khasra 45/12 submitted 4 months ago at Tehsil office Rohini is pending without reasons.",
        "department": "Revenue & Land Records"
    }
    response = client.post("/api/v1/cases/intake", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "created"
    case = data["case"]
    assert case["complainant"]["name"] == "Anil Kumar"
    assert case["category"] == "Revenue & Land Records"
    assert case["status"] == "NEEDS_REVIEW"
    assert len(case["draft_rti"]["questions"]) >= 3
    # Verify IPC/BNS and Geospatial outputs
    assert "statutory_legal_analysis" in case
    assert len(case["statutory_legal_analysis"]["ipc_sections"]) > 0
    assert len(case["statutory_legal_analysis"]["bns_sections"]) > 0
    assert "geospatial_meta" in case

def test_varanasi_banaras_intake_and_search(client):
    payload = {
        "complainant": {
            "name": "Shivanshu Pandey",
            "contact": "+91-9988776655",
            "address": "Assi Ghat, Varanasi / Banaras, Uttar Pradesh - 221005",
            "language": "Hindi / English"
        },
        "raw_grievance": "My land mutation khasra 88/14 application (Ref VNS-99401) submitted on 10-Jan-2026 at Tehsil Kachehri Varanasi / Banaras is pending beyond the 30-day statutory limit.",
        "application_ref_no": "VNS-99401",
        "original_submission_date": "10-Jan-2026"
    }
    response = client.post("/api/v1/cases/intake", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    case = data["case"]
    assert "Varanasi" in case["suggested_pio"]["office_address"] or "Banaras" in case["suggested_pio"]["office_address"]
    assert case["category"] == "Revenue & Land Records"
    assert case["application_ref_no"] == "VNS-99401"
    case_id = case["case_id"]

    # Verify IPC & BNS 2023 matches
    legal = case["statutory_legal_analysis"]
    assert any("420" in s or "218" in s for s in legal["ipc_sections"])
    assert any("318" in s or "231" in s for s in legal["bns_sections"])

    # Test search with 'Varanasi'
    s_response = client.get("/api/v1/cases?search=Varanasi")
    assert s_response.status_code == 200
    s_data = s_response.get_json()
    assert len(s_data["cases"]) >= 1

    # Test synonym search with 'banaras'
    b_response = client.get("/api/v1/cases?search=banaras")
    assert b_response.status_code == 200
    b_data = b_response.get_json()
    assert len(b_data["cases"]) >= 1

    # Test department override to Police & Law Enforcement
    o_response = client.post(f"/api/v1/cases/{case_id}/override", json={
        "department": "Police & Law Enforcement",
        "reviewer": "Advocate Reviewer"
    })
    assert o_response.status_code == 200
    o_case = o_response.get_json()["case"]
    assert o_case["department"] == "Police & Law Enforcement"
    assert "Varanasi" in o_case["suggested_pio"]["office_address"] or "Banaras" in o_case["suggested_pio"]["office_address"]

def test_first_appeal_generation(client):
    # Test First Appeal generation under Section 19(1)
    response = client.get("/api/v1/cases/ARZ-1046/appeal")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    appeal = data["appeal"]
    assert "FIRST APPEAL" in appeal["appeal_type"]
    assert len(appeal["grounds_of_appeal"]) >= 3

def test_section_6_3_transfer(client):
    # Test Section 6(3) 5-Day Mandatory Transfer
    payload = {
        "target_department": "Food & Civil Supplies",
        "transfer_reason": "RTI subject matter pertains to PDS food distribution wing.",
        "reviewer": "Tehsildar PIO Desk"
    }
    response = client.post("/api/v1/cases/ARZ-1046/transfer-sec6-3", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "transferred"
    assert data["case"]["status"] == "TRANSFERRED_SEC_6_3"
    assert data["case"]["department"] == "Food & Civil Supplies"

def test_compliance_radar_endpoint(client):
    response = client.get("/api/v1/cases/compliance-radar")
    assert response.status_code == 200
    data = response.get_json()
    assert "compliance_radar" in data
    radar = data["compliance_radar"]
    assert radar["total_cases"] >= 2
    assert radar["statutory_rate_per_day_inr"] == 250

def test_multi_format_pdf_generation(client):
    # 1. Standard RTI Form-A PDF
    r1 = client.get("/api/v1/cases/ARZ-1042/pdf?type=rti")
    assert r1.status_code == 200
    assert r1.content_type == "application/pdf"
    assert len(r1.data) > 100

    # 2. First Appeal PDF
    r2 = client.get("/api/v1/cases/ARZ-1042/pdf?type=appeal")
    assert r2.status_code == 200
    assert r2.content_type == "application/pdf"
    assert len(r2.data) > 100

    # 3. Legal Notice PDF
    r3 = client.get("/api/v1/cases/ARZ-1042/pdf?type=notice")
    assert r3.status_code == 200
    assert r3.content_type == "application/pdf"
    assert len(r3.data) > 100

def test_approve_case(client):
    payload = {
        "reviewer": "Advocate Legal Officer",
        "notes": "Approved for RTI filing.",
        "channel": "Registered SpeedPost + Email"
    }
    response = client.post("/api/v1/cases/ARZ-1042/approve", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "approved"
    assert data["case"]["status"] == "APPROVED"
    assert "dispatch_info" in data["case"]

def test_run_log_audit(client):
    response = client.get("/api/v1/run-log")
    assert response.status_code == 200
    data = response.get_json()
    assert "run_logs" in data
    assert len(data["run_logs"]) > 0

def test_custom_acts_lifecycle(client):
    # 1. List custom acts
    res = client.get("/api/v1/cases/custom-acts")
    assert res.status_code == 200
    data = res.get_json()
    assert "custom_acts" in data
    assert len(data["custom_acts"]) >= 3

    # 2. Create custom act
    new_act_payload = {
        "act_title": "Transfer of Property Act, 1882",
        "section": "Section 54 & Section 122 (Sale & Gift Deed Validity)",
        "domain": "Revenue & Land Records",
        "statutory_grounds": "Requires registered conveyance deed for immovable property transfer.",
        "punishment_or_relief": "Cancellation of fraudulent mutation and restoration of legal title.",
        "added_by": "Adv. S. Kalra"
    }
    create_res = client.post("/api/v1/cases/custom-acts", json=new_act_payload)
    assert create_res.status_code == 201
    create_data = create_res.get_json()
    act_id = create_data["custom_act"]["act_id"]
    assert "ACT-" in act_id

    # 3. Apply custom act to an active case
    apply_res = client.post("/api/v1/cases/ARZ-1046/apply-custom-act", json={"act_id": act_id, "reviewer": "Adv. S. Kalra"})
    assert apply_res.status_code == 200
    apply_data = apply_res.get_json()
    assert apply_data["status"] == "applied"
    case = apply_data["case"]
    assert any("Transfer of Property Act" in a for a in case["statutory_legal_analysis"]["allied_acts"])

    # 4. Delete custom act
    del_res = client.delete(f"/api/v1/cases/custom-acts/{act_id}")
    assert del_res.status_code == 200
    assert del_res.get_json()["status"] == "deleted"

def test_github_repo_kill_switch(client):
    repo_validator.toggle_kill_switch(True)
    try:
        response = client.get("/api/v1/cases")
        assert response.status_code == 503
        data = response.get_json()
        assert data["integrity_breach"] is True
        assert "Repository Binding Revoked" in data["error"]
    finally:
        repo_validator.toggle_kill_switch(False)

    response = client.get("/api/v1/cases")
    assert response.status_code == 200

def test_area_and_domain_pio_assignment(client):
    # 1. Register a complaint in Varanasi for Food & Civil Supplies
    payload = {
        "complainant": {
            "name": "Kavita Devi",
            "contact": "+91-9876500000",
            "address": "Nadesar, Varanasi / Banaras, Uttar Pradesh - 221002",
            "language": "Hindi"
        },
        "raw_grievance": "My ration quota (Ref VNS-FOOD-881) is not being distributed at Nadesar PDS shop. Officer is unresponsive.",
        "department": "Food & Civil Supplies",
        "application_ref_no": "VNS-FOOD-881"
    }
    res = client.post("/api/v1/cases/intake", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    case = data["case"]
    case_id = case["case_id"]

    # Verify nearest PIO of DOMAIN was assigned
    suggested = case["suggested_pio"]
    assert suggested["department"] == "Food & Civil Supplies"
    assert "V. P. Singh" in suggested["pio_name"] or "Food" in suggested["department"]
    assert "nearby_area_pios" in case
    assert len(case["nearby_area_pios"]) >= 4

    # Verify all nearby PIOs in that area are included and ranked
    area_pios = case["nearby_area_pios"]
    assert any(p["is_assigned"] for p in area_pios)
    # The assigned domain officer has is_domain_match == True and is_assigned == True
    assigned_match = [p for p in area_pios if p["is_assigned"]][0]
    assert assigned_match["is_domain_match"] is True

    # 2. Test GET /cases/<case_id>/nearby-pios
    geo_res = client.get(f"/api/v1/cases/{case_id}/nearby-pios")
    assert geo_res.status_code == 200
    geo_data = geo_res.get_json()
    assert geo_data["case_id"] == case_id
    assert len(geo_data["nearby_area_pios"]) >= 4

    # 3. Test re-assigning PIO via POST /cases/<case_id>/assign-pio
    alt_pio = area_pios[0] if area_pios[0]["id"] != assigned_match["id"] else area_pios[1]
    assign_res = client.post(f"/api/v1/cases/{case_id}/assign-pio", json={
        "pio": alt_pio,
        "reviewer": "Adv. S. Kalra"
    })
    assert assign_res.status_code == 200
    reassigned_case = assign_res.get_json()["case"]
    assert reassigned_case["suggested_pio"]["pio_name"] == alt_pio["pio_name"]

def test_48_hour_life_and_liberty_detection(client):
    # Ingest a critical life & liberty grievance (hospital ICU oxygen failure & contaminated water)
    payload = {
        "complainant": {
            "name": "Sunita Verma",
            "contact": "+91-9988776655",
            "address": "Sigra, Varanasi, Uttar Pradesh - 221010",
            "language": "Hindi"
        },
        "raw_grievance": "EMERGENCY: Contaminated poisonous water in municipal line causing severe epidemic in Sigra. Multiple patients in hospital ICU on ventilator. Threat to life. Officer refusing inspection.",
        "department": "Municipal Public Works & Drainage"
    }
    res = client.post("/api/v1/cases/intake", json=payload)
    assert res.status_code == 201
    case = res.get_json()["case"]
    case_id = case["case_id"]

    # Statutory 48-Hour SLA Assertion under Section 7(1) Proviso
    assert case["is_life_liberty"] is True
    assert case["statutory_sla_hours"] == 48
    assert case["sla_days_remaining"] == 2
    assert "PROVISO TO SECTION 7(1)" in case["draft_rti"]["application_subject"]
    assert "MANDATORY STATUTORY DISCLOSURE WITHIN 48 HOURS" in case["draft_rti"]["questions"][0]

    # Test First Appeal reflects 48-Hour Deemed Refusal & Article 21
    appeal_res = client.get(f"/api/v1/cases/{case_id}/appeal")
    assert appeal_res.status_code == 200
    appeal = appeal_res.get_json()["appeal"]
    assert appeal["is_life_liberty"] is True
    assert "48-HOUR LIFE & LIBERTY EMERGENCY" in appeal["subject"]
    assert any("Article 21" in g for g in appeal["grounds_of_appeal"])

def test_toggle_urgency_endpoint(client):
    # Intake standard case
    payload = {
        "complainant": {"name": "Rohan Gupta", "address": "Civil Lines, Prayagraj"},
        "raw_grievance": "Delay in mutation of agricultural plot.",
        "department": "Revenue & Land Records"
    }
    res = client.post("/api/v1/cases/intake", json=payload)
    case_id = res.get_json()["case"]["case_id"]

    # Toggle to urgent Life & Liberty
    toggle_res = client.post(f"/api/v1/cases/{case_id}/toggle-urgency", json={"is_urgent": True, "reviewer": "Advocate Kalra"})
    assert toggle_res.status_code == 200
    data = toggle_res.get_json()
    assert data["is_life_liberty"] is True
    assert data["statutory_sla_hours"] == 48
    assert data["sla_days_remaining"] == 2

    # Toggle back to standard 30-day
    toggle_res2 = client.post(f"/api/v1/cases/{case_id}/toggle-urgency", json={"is_urgent": False, "reviewer": "Advocate Kalra"})
    assert toggle_res2.status_code == 200
    data2 = toggle_res2.get_json()
    assert data2["is_life_liberty"] is False
    assert data2["statutory_sla_hours"] == 720
    assert data2["sla_days_remaining"] == 30

def test_section_8_shield_endpoint(client):
    # Verify Section 8 Exemption Shield for police inaction case
    res = client.post(f"/api/v1/cases/ARZ-1046/section8-shield", json={
        "public_interest_reason": "Corruption and illegal extortion in public office"
    })
    assert res.status_code == 200
    data = res.get_json()
    shield = data["section_8_shield"]
    assert shield["public_interest_override_applicable"] is True
    assert len(shield["section_8_risks_identified"]) > 0
    assert "STATUTORY REBUTTAL NOTICE" in shield["statutory_rebuttal_draft"]
    assert "Section 8(2)" in shield["section_8_2_override_text"]

def test_postal_slip_and_pdf(client):
    # 1. Test Postal Slip metadata and SVG Barcode
    res = client.get("/api/v1/cases/ARZ-1046/postal-slip")
    assert res.status_code == 200
    slip = res.get_json()["postal_slip"]
    assert slip["consignment_number"].startswith("EM")
    assert slip["consignment_number"].endswith("IN")
    assert "<svg" in slip["barcode_svg"]
    assert "Section 27 of the General Clauses Act" in slip["legal_notice"]

    # 2. Test PDF generation for postal slip
    pdf_res = client.get("/api/v1/cases/ARZ-1046/pdf?type=slip")
    assert pdf_res.status_code == 200
    assert pdf_res.headers["Content-Type"] == "application/pdf"
    assert len(pdf_res.data) > 500

def test_pincode_lookup_endpoint(client):
    # 1. Karnataka Bangalore PIN 560001
    res_blr = client.get("/api/v1/cases/pincode-lookup?pincode=560001")
    assert res_blr.status_code == 200
    data_blr = res_blr.get_json()
    assert data_blr["status"] == "success"
    assert data_blr["pincode"] == "560001"
    assert "Karnataka" in data_blr["state"]
    assert "Karnataka Land Revenue Act" in data_blr["land_codex"]["primary_land_act"]
    assert "Bhoomi" in data_blr["land_codex"]["digital_land_portal"]
    assert "Tahsildar" in data_blr["assigned_pio"]["designation"]

    # 2. Maharashtra Mumbai PIN 400001
    res_mum = client.get("/api/v1/cases/pincode-lookup?pincode=400001")
    assert res_mum.status_code == 200
    data_mum = res_mum.get_json()
    assert "Maharashtra" in data_mum["state"]
    assert "Maharashtra Land Revenue Code" in data_mum["land_codex"]["primary_land_act"]
    assert "MahaBhulekh" in data_mum["land_codex"]["digital_land_portal"]

    # 3. Rajasthan Jaipur PIN 302001
    res_jpr = client.get("/api/v1/cases/pincode-lookup?pincode=302001")
    assert res_jpr.status_code == 200
    data_jpr = res_jpr.get_json()
    assert "Rajasthan" in data_jpr["state"]
    assert "Rajasthan Land Revenue Act" in data_jpr["land_codex"]["primary_land_act"]

    # 4. Bihar Patna PIN 800001
    res_pat = client.get("/api/v1/cases/pincode-lookup?pincode=800001")
    assert res_pat.status_code == 200
    data_pat = res_pat.get_json()
    assert "Bihar" in data_pat["state"]
    assert "Bihar Land Mutation Act" in data_pat["land_codex"]["primary_land_act"]
    assert "Circle Officer" in data_pat["land_codex"]["pio_title"]

    # 5. Invalid PIN validation
    res_inv = client.get("/api/v1/cases/pincode-lookup?pincode=999")
    assert res_inv.status_code == 400

def test_all_india_land_intake_routing(client):
    # Intake Karnataka Land Grievance with 560001 PIN
    payload_karnataka = {
        "complainant": {
            "name": "Basavaraj Gowda",
            "contact": "+91-9845012345",
            "address": "Indiranagar, Bengaluru, Karnataka",
            "pincode": "560001"
        },
        "raw_grievance": "My land mutation application for RTC Pahani extract transfer submitted 90 days ago is illegally held up at Tahsildar office Bangalore.",
        "department": "Revenue & Land Records"
    }
    res_k = client.post("/api/v1/cases/intake", json=payload_karnataka)
    assert res_k.status_code == 201
    case_k = res_k.get_json()["case"]
    
    assert case_k["pincode"] == "560001"
    assert "Karnataka" in case_k["state"]
    assert "Karnataka Land Revenue Act" in case_k["statutory_jurisdiction"]["primary_land_act"]
    assert "Tahsildar" in case_k["suggested_pio"]["designation"]
    assert "Varanasi" not in case_k["suggested_pio"]["office_address"]
    # Check that questions cite Karnataka Land Revenue Act and RTC/Pahani
    q_joined = " ".join(case_k["draft_rti"]["questions"])
    assert "Karnataka Land Revenue Act" in q_joined
    assert "Section 128" in q_joined or "RTC" in q_joined

    # Verify searchable by PIN in list_cases
    search_res = client.get("/api/v1/cases?search=560001")
    assert search_res.status_code == 200
    found_cases = search_res.get_json()["cases"]
    assert any(c["case_id"] == case_k["case_id"] for c in found_cases)

    # Intake Maharashtra Land Grievance with 400001 PIN
    payload_mh = {
        "complainant": {
            "name": "Sachin Deshmukh",
            "contact": "+91-9820011223",
            "address": "Dadar, Mumbai, Maharashtra - 400001"
        },
        "raw_grievance": "Ferfar mutation entry and Satbara 7/12 extract not updated after sale deed execution.",
        "department": "Revenue & Land Records"
    }
    res_mh = client.post("/api/v1/cases/intake", json=payload_mh)
    assert res_mh.status_code == 201
    case_mh = res_mh.get_json()["case"]
    assert case_mh["pincode"] == "400001"
    assert "Maharashtra" in case_mh["state"]
    assert "Maharashtra Land Revenue Code" in case_mh["statutory_jurisdiction"]["primary_land_act"]
    q_mh_joined = " ".join(case_mh["draft_rti"]["questions"])
    assert "Maharashtra Land Revenue Code" in q_mh_joined


