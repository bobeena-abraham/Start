import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    if email in client.get("/activities").json()[activity]["participants"]:
        client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Clean up
    client.post(f"/activities/{activity}/unregister?email={email}")

def test_signup_duplicate():
    activity = "Chess Club"
    email = "michael@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_invalid_email():
    activity = "Chess Club"
    email = "invalidemail"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "Invalid email format" in response.json()["detail"]

def test_signup_activity_not_found():
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
