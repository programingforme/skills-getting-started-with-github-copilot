import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities
def test_get_activities():
    # Arrange: (No setup needed for in-memory data)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Test POST /activities/{activity_name}/signup
def test_signup_for_activity():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up: Remove test user
    client.delete(f"/activities/{activity}/signup?email={email}")

# Test DELETE /activities/{activity_name}/signup
def test_unregister_from_activity():
    # Arrange
    activity = "Chess Club"
    email = "testdelete@mergington.edu"
    # Ensure user is registered first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]

# Test duplicate signup error
def test_duplicate_signup_error():
    # Arrange
    activity = "Chess Club"
    email = "testduplicate@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    client.delete(f"/activities/{activity}/signup?email={email}")

# Test unregistering non-existent participant
def test_unregister_nonexistent_participant():
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]
