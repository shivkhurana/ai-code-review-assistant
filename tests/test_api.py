from fastapi.testclient import TestClient
from app.node_api import app

client = TestClient(app)


def test_chat_endpoint_returns_response():
    response = client.post("/chat", json={"query": "Explain why the model should prefer explicit logic."})
    assert response.status_code == 200
    payload = response.json()
    assert "response" in payload
    assert payload["style_score"] >= 0.0
    assert payload["latency_ms"] >= 0.0


def test_chat_endpoint_rejects_empty_query():
    response = client.post("/chat", json={"query": ""})
    assert response.status_code == 400


def test_health_endpoint_returns_prompt():
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert "prompt" in payload
