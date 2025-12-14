import pytest
from app import create_app
from db import db
from models import User

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "ok"

def test_create_user(client):
    payload = {
        "email": "john@example.com",
        "name": "John"
    }
    res = client.post("/users", json=payload)
    assert res.status_code == 201
    assert res.json["email"] == "john@example.com"

def test_get_users(client):
    client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    client.post("/users", json={"name": "Bob", "email": "bob@example.com"})

    res = client.get("/users")
    assert res.status_code == 200
    data = res.json
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[1]["name"] == "Bob"
