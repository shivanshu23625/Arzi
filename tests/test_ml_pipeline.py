import pytest
from flask_backend.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        # Reset ML vector store before each test session
        client.post("/api/v1/reset")
        yield client

def test_ml_pipeline_authentic_request(client):
    payload = {
        "request_id": "test-ml-001",
        "raw_text": "Can you provide a summary of project status?"
    }
    res = client.post("/api/v1/process", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["request_id"] == "test-ml-001"
    assert data["status"] == "PROCESS_EXECUTION_SUCCESS"
    assert data["output"] is not None
    assert "confidence" in data
    assert data["confidence"]["confidence_score"] >= 0.50

def test_ml_pipeline_spam_detection(client):
    payload = {
        "request_id": "test-ml-002",
        "raw_text": "CLAIM YOUR FREE MONEY WINNER CASINO LOTTERY"
    }
    res = client.post("/api/v1/process", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["request_id"] == "test-ml-002"
    assert data["status"] == "REJECTED_SPAM"

def test_ml_pipeline_duplicate_short_circuit(client):
    query = "Unique citizen query regarding water pipe replacement."
    payload1 = {"request_id": "test-ml-dup-1", "raw_text": query}
    res1 = client.post("/api/v1/process", json=payload1)
    assert res1.status_code == 200
    assert res1.get_json()["status"] == "PROCESS_EXECUTION_SUCCESS"

    # Second identical query should be short-circuited as duplicate
    payload2 = {"request_id": "test-ml-dup-2", "raw_text": query}
    res2 = client.post("/api/v1/process", json=payload2)
    assert res2.status_code == 200
    assert res2.get_json()["status"] == "SHORT_CIRCUIT_DUPLICATE"

def test_ml_pipeline_sql_injection_rejection(client):
    payload = {
        "request_id": "test-ml-004",
        "raw_text": "drop table users; SELECT * FROM credentials WHERE '1'='1';"
    }
    res = client.post("/api/v1/process", json=payload)
    assert res.status_code == 400
    data = res.get_json()
    assert data["request_id"] == "test-ml-004"
    assert data["status"] == "REJECTED_INPUT"
    assert "rejection_reason" in data

