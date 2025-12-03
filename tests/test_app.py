import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure not already signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400

def test_unregister_participant():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure participant is present
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    # Try removing again
    response_missing = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response_missing.status_code == 404