import pytest
from core.database import Base, get_db, get_test_db, test_engine
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def create_test_tables():
    Base.metadata.create_all(bind=test_engine)
    yield
    for tbl in reversed(Base.metadata.sorted_tables):
        with test_engine.connect() as conn:
            conn.execute(tbl.delete())
            conn.commit()


def email_not_breached(test_client):
    pass
    # response = test_client.post("/data/", json=)


def test_get_breachdata_by_email_no_leak(test_client):
    """GET /breach/email/{email} with an email not leaked"""
    response = test_client.get("/breach/email/example@mail.com")
    assert response.status_code == 200
    assert response.json() == {"email": "example@mail.com"}
