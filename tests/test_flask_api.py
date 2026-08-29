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
