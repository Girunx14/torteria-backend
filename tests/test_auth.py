# tests/test_auth.py
def test_login_success(client):
    response = client.post("/auth/login", data={
        "username": "testadmin",
        "password": "test1234",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    response = client.post("/auth/login", data={
        "username": "testadmin",
        "password": "incorrecta",
    })
    assert response.status_code == 401


def test_me_authenticated(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testadmin"
    assert response.json()["role"] == "admin"


def test_me_unauthenticated(client):
    response = client.get("/auth/me")
    assert response.status_code == 401