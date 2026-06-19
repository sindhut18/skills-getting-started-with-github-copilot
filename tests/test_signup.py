def test_signup_adds_participant(client, signup_email):
    # Arrange
    activity_name = "Chess Club"
    endpoint = f"/activities/{activity_name}/signup"
    before = client.get("/activities").json()[activity_name]["participants"]
    assert signup_email not in before

    # Act
    response = client.post(endpoint, params={"email": signup_email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {signup_email} for {activity_name}"
    after = client.get("/activities").json()[activity_name]["participants"]
    assert signup_email in after


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_unknown_activity(client, signup_email):
    # Arrange
    activity_name = "Unknown Activity"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": signup_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
