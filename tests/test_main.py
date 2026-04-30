import pytest
from app.main import app 

# -------------------------------------------------------------------
# Fixture
# -------------------------------------------------------------------

@pytest.fixture
def client():
    """Set up a test client before each test."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# -------------------------------------------------------------------
# GET /health
# -------------------------------------------------------------------

class TestHealthCheck:
    def test_returns_200(self, client):
        res = client.get("/health")
        assert res.status_code == 200

    def test_returns_ok_status(self, client):
        res = client.get("/health")
        data = res.get_json()
        assert data["status"] == "ok"

    def test_response_is_json(self, client):
        res = client.get("/health")
        assert res.content_type == "application/json"


# -------------------------------------------------------------------
# GET /
# -------------------------------------------------------------------

class TestHome:
    def test_returns_200(self, client):
        res = client.get("/")
        assert res.status_code == 200

    def test_returns_message(self, client):
        res = client.get("/")
        data = res.get_json()
        assert "message" in data
        assert data["message"] == "Hello from my app!"

    def test_response_is_json(self, client):
        res = client.get("/")
        assert res.content_type == "application/json"


# -------------------------------------------------------------------
# Unknown routes
# -------------------------------------------------------------------

class TestUnknownRoutes:
    def test_unknown_route_returns_404(self, client):
        res = client.get("/unknown")
        assert res.status_code == 404
