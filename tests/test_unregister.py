from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_removes_student_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    before = activities[activity_name]["participants"][:]
    assert email in before

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

    activities[activity_name]["participants"] = before


def test_unregister_returns_404_for_unknown_activity():
    response = client.delete("/activities/Unknown Activity/unregister?email=test@example.com")

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
