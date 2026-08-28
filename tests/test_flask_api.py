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
    assert "Varanasi / Banaras" in case["suggested_pio"]["office_address"]
    assert case["category"] == "Revenue & Land Records"
    assert case["application_ref_no"] == "VNS-99401"
    case_id = case["case_id"]

    # Test global search console endpoint with keyword 'Varanasi'
    s_response = client.get("/api/v1/cases?search=Varanasi")
    assert s_response.status_code == 200
    s_data = s_response.get_json()
    assert len(s_data["cases"]) >= 1
    assert any("Varanasi" in c["suggested_pio"]["office_address"] or "Varanasi" in c["complainant"]["address"] for c in s_data["cases"])

    # Test synonym search with 'banaras'
    b_response = client.get("/api/v1/cases?search=banaras")
    assert b_response.status_code == 200
    b_data = b_response.get_json()
    assert len(b_data["cases"]) >= 1

    # Test department override to Police & Law Enforcement for Banaras complainant
    o_response = client.post(f"/api/v1/cases/{case_id}/override", json={
        "department": "Police & Law Enforcement",
        "reviewer": "Advocate Reviewer"
    })
    assert o_response.status_code == 200
    o_case = o_response.get_json()["case"]
    assert o_case["department"] == "Police & Law Enforcement"
    assert "Varanasi / Banaras" in o_case["suggested_pio"]["office_address"]
    assert "Police Line" in o_case["suggested_pio"]["office_address"]

def test_banaras_police_intake(client):
    payload = {
        "complainant": {
            "name": "Ramesh Gupta",
            "contact": "+91-9876500000",
            "address": "Godowlia Market, Banaras, UP",
            "language": "Hindi"
        },
        "raw_grievance": "FIR complaint regarding shop theft filed at police station / thana in Banaras 2 months ago has no update or investigation report.",
    }
    response = client.post("/api/v1/cases/intake", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    case = data["case"]
    assert case["category"] == "Police & Law Enforcement"
    assert "Varanasi / Banaras" in case["suggested_pio"]["office_address"]
    assert "Shri R. K. Singh" in case["suggested_pio"]["pio_name"]

def test_approve_case(client):
    # Approve case ARZ-1042
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

def test_pdf_generation(client):
    response = client.get("/api/v1/cases/ARZ-1042/pdf")
    assert response.status_code == 200
    assert response.content_type == "application/pdf"
    assert len(response.data) > 100

def test_github_repo_kill_switch(client):
    # Engage Kill-Switch simulation
    repo_validator.toggle_kill_switch(True)
    try:
        response = client.get("/api/v1/cases")
        assert response.status_code == 503
        data = response.get_json()
        assert data["integrity_breach"] is True
        assert "Repository Binding Revoked" in data["error"]
    finally:
        # Restore state
        repo_validator.toggle_kill_switch(False)

    # Verify restored
    response = client.get("/api/v1/cases")
    assert response.status_code == 200
