# tests/test_categories.py
import pytest


def test_get_categories_empty(client):
    response = client.get("/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_category(client, auth_headers):
    response = client.post("/categories/", json={
        "name": "Tortas",
        "description": "Tortas artesanales",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Tortas"
    assert data["is_active"] is True


def test_create_category_duplicate(client, auth_headers):
    client.post("/categories/", json={"name": "Bebidas"}, headers=auth_headers)
    response = client.post("/categories/", json={"name": "Bebidas"}, headers=auth_headers)
    assert response.status_code == 409


def test_create_category_unauthorized(client):
    response = client.post("/categories/", json={"name": "Extras"})
    assert response.status_code == 401


def test_get_category_by_id(client, auth_headers):
    client.post("/categories/", json={"name": "Postres"}, headers=auth_headers)
    response = client.get("/categories/1")
    assert response.status_code == 200


def test_update_category(client, auth_headers):
    response = client.put("/categories/1", json={
        "description": "Nueva descripción",
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["description"] == "Nueva descripción"


def test_get_category_not_found(client):
    response = client.get("/categories/9999")
    assert response.status_code == 404