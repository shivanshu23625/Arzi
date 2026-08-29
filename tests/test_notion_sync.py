import pytest
import json
from flask_backend.app import create_app
from flask_backend.services.notion_service import notion_service
from flask_backend.models.store import db_store

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_notion_status_endpoint(client):
    response = client.get("/api/v1/notion/status")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "notion" in data
    assert "mode" in data["notion"]

def test_notion_configure_endpoint(client):
    payload = {
        "api_key": "secret_test_integration_token_12345",
        "cases_db_id": "test_cases_db_id_67890",
        "run_log_db_id": "test_run_log_db_id_11223",
        "parent_page_id": "test_parent_page_id_44556"
    }
    response = client.post("/api/v1/notion/configure", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert notion_service.api_key == "secret_test_integration_token_12345"
    assert notion_service.cases_db_id == "test_cases_db_id_67890"

def test_notion_sync_all_and_mirror(client):
    # Trigger full sync
    response = client.post("/api/v1/notion/sync-all")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["synced_cases_count"] >= 2
    assert data["synced_run_logs_count"] >= 1

    # Verify mirror endpoint
    mirror_resp = client.get("/api/v1/notion/mirror")
    assert mirror_resp.status_code == 200
    mirror_data = mirror_resp.get_json()
    assert mirror_data["status"] == "success"
    assert mirror_data["total_cases_mirrored"] >= 2
    assert mirror_data["total_logs_mirrored"] >= 1

    # Inspect formatted page blocks for first case
    case_page = mirror_data["cases_database_mirror"][0]
    assert "properties" in case_page
    assert "Case ID" in case_page["properties"]
    assert "Status" in case_page["properties"]
    assert case_page["blocks_count"] >= 5

def test_notion_case_blocks_content():
    case = db_store.get_case("ARZ-1046")
    blocks = notion_service._build_case_notion_blocks(case, host_url="http://localhost:5000")
    assert len(blocks) >= 6
    # Verify callout block with legal dossier
    callout = blocks[0]
    assert callout["type"] == "callout"
    assert "ARZI STATUTORY LEGAL DOSSIER" in callout["callout"]["rich_text"][0]["text"]["content"]

def test_notion_run_log_audit_leaves_proof():
    log_entry = {
        "run_id": "RLOG-NOTION-TEST-001",
        "timestamp": "2026-08-29 11:55:00",
        "event_type": "NOTION_TRACK_VERIFICATION",
        "case_id": "ARZ-1046",
        "actor": "Hackathon Judge",
        "action": "Verified Notion run log timestamp integrity",
        "result": "SUCCESS",
        "correlation_id": "CORR-NOTION-AUDIT"
    }
    result = notion_service.log_run_to_notion(log_entry)
    assert "run_id" in result
    assert result["run_id"] == "RLOG-NOTION-TEST-001"
    assert any(r["run_id"] == "RLOG-NOTION-TEST-001" for r in notion_service.mock_run_log_rows)
