def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    target_email = "daniel@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants"
    before = client.get("/activities").json()[activity_name]["participants"]
    assert target_email in before

    # Act
    response = client.delete(endpoint, params={"email": target_email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {target_email} from {activity_name}"
    after = client.get("/activities").json()[activity_name]["participants"]
    assert target_email not in after


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    endpoint = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(endpoint, params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "absent@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(endpoint, params={"email": missing_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
