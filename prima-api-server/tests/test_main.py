from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_welcome_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to the Prima API" in response.text
