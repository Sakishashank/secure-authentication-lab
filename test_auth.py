import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_register(client):
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    assert response.status_code == 201


def test_login(client):
    client.post(
        "/register",
        json={
            "username": "loginuser",
            "password": "password123"
        }
    )

    response = client.post(
        "/login",
        json={
            "username": "loginuser",
            "password": "password123"
        }
    )

    assert response.status_code == 200


def test_wrong_password(client):
    client.post(
        "/register",
        json={
            "username": "wrongpass",
            "password": "password123"
        }
    )

    response = client.post(
        "/login",
        json={
            "username": "wrongpass",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_protected_route(client):
    response = client.get("/profile")

    assert response.status_code == 401


def test_logout(client):
    client.post(
        "/register",
        json={
            "username": "logoutuser",
            "password": "password123"
        }
    )

    client.post(
        "/login",
        json={
            "username": "logoutuser",
            "password": "password123"
        }
    )

    response = client.post("/logout")

    assert response.status_code == 200


def test_invalid_password(client):
    response = client.post(
        "/register",
        json={
            "username": "short",
            "password": "123"
        }
    )

    assert response.status_code == 400