from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_breachdata_by_email():
    response = client.get("/breach/email/example@mail.com")
    assert response.status_code == 200
    assert response.json() == {"email": "example@mail.com"}
