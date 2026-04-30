import pytest
from app import app, users, next_id


# -------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------

@pytest.fixture
def client():
    """Create a test client with a clean state before each test."""
    app.config["TESTING"] = True

    # Reset store to a known state
    users.clear()
    users.extend([
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob",   "email": "bob@example.com"},
    ])

    import app as app_module
    app_module.next_id = 3

    with app.test_client() as client:
        yield client


# -------------------------------------------------------------------
# GET /api/users
# -------------------------------------------------------------------

class TestGetUsers:
    def test_returns_200(self, client):
        res = client.get("/api/users")
        assert res.status_code == 200

    def test_returns_list(self, client):
        res = client.get("/api/users")
        data = res.get_json()
        assert isinstance(data, list)
        assert len(data) == 2

    def test_user_fields_present(self, client):
        res = client.get("/api/users")
        user = res.get_json()[0]
        assert "id"    in user
        assert "name"  in user
        assert "email" in user


# -------------------------------------------------------------------
# GET /api/users/<id>
# -------------------------------------------------------------------

class TestGetUser:
    def test_existing_user(self, client):
        res = client.get("/api/users/1")
        assert res.status_code == 200
        assert res.get_json()["name"] == "Alice"

    def test_missing_user_returns_404(self, client):
        res = client.get("/api/users/999")
        assert res.status_code == 404
        assert "error" in res.get_json()


# -------------------------------------------------------------------
# POST /api/users
# -------------------------------------------------------------------

class TestCreateUser:
    def test_creates_user(self, client):
        payload = {"name": "Charlie", "email": "charlie@example.com"}
        res = client.post("/api/users", json=payload)
        assert res.status_code == 201
        data = res.get_json()
        assert data["name"]  == "Charlie"
        assert data["email"] == "charlie@example.com"
        assert "id" in data

    def test_missing_name_returns_400(self, client):
        res = client.post("/api/users", json={"email": "x@example.com"})
        assert res.status_code == 400

    def test_missing_email_returns_400(self, client):
        res = client.post("/api/users", json={"name": "X"})
        assert res.status_code == 400

    def test_empty_body_returns_400(self, client):
        res = client.post("/api/users", data="not-json",
                          content_type="text/plain")
        assert res.status_code == 400

    def test_user_count_increases(self, client):
        client.post("/api/users", json={"name": "D", "email": "d@d.com"})
        res = client.get("/api/users")
        assert len(res.get_json()) == 3


# -------------------------------------------------------------------
# PUT /api/users/<id>
# -------------------------------------------------------------------

class TestUpdateUser:
    def test_update_name(self, client):
        res = client.put("/api/users/1", json={"name": "Alicia"})
        assert res.status_code == 200
        assert res.get_json()["name"] == "Alicia"

    def test_update_email(self, client):
        res = client.put("/api/users/1", json={"email": "new@example.com"})
        assert res.status_code == 200
        assert res.get_json()["email"] == "new@example.com"

    def test_update_missing_user_returns_404(self, client):
        res = client.put("/api/users/999", json={"name": "Ghost"})
        assert res.status_code == 404

    def test_empty_body_leaves_user_unchanged(self, client):
        original = client.get("/api/users/1").get_json()
        client.put("/api/users/1", json={})
        updated = client.get("/api/users/1").get_json()
        assert original == updated


# -------------------------------------------------------------------
# DELETE /api/users/<id>
# -------------------------------------------------------------------

class TestDeleteUser:
    def test_deletes_user(self, client):
        res = client.delete("/api/users/1")
        assert res.status_code == 200
        assert "message" in res.get_json()

    def test_deleted_user_no_longer_accessible(self, client):
        client.delete("/api/users/1")
        res = client.get("/api/users/1")
        assert res.status_code == 404

    def test_user_count_decreases(self, client):
        client.delete("/api/users/1")
        res = client.get("/api/users")
        assert len(res.get_json()) == 1

    def test_delete_missing_user_returns_404(self, client):
        res = client.delete("/api/users/999")
        assert res.status_code == 404
