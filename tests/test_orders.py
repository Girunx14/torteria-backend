# tests/test_orders.py
import pytest


@pytest.fixture(scope="session")
def order_product_id(client, auth_headers):
    """Crea categoría y producto dedicados para tests de órdenes."""
    cat = client.post("/categories/", json={
        "name": "Cat Ordenes",
        "description": "Para tests de órdenes",
    }, headers=auth_headers)
    category_id = cat.json()["id"]

    prod = client.post("/products/", json={
        "name": "Producto Test Orden",
        "description": "Para tests",
        "price": 50.00,
        "category_id": category_id,
    }, headers=auth_headers)
    return prod.json()["id"]


@pytest.fixture(scope="session")
def created_order_id(client, order_product_id):
    """Crea una orden y retorna su id."""
    response = client.post("/orders/", json={
        "items": [{"product_id": order_product_id, "quantity": 2}],
        "notes": "Sin cebolla",
    })
    assert response.status_code == 201
    return response.json()["id"]


def test_create_order(client, order_product_id):
    response = client.post("/orders/", json={
        "items": [{"product_id": order_product_id, "quantity": 2}],
        "notes": "Sin cebolla",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert float(data["total"]) == 100.0
    assert len(data["items"]) == 1


def test_create_order_empty_items(client):
    response = client.post("/orders/", json={"items": []})
    assert response.status_code == 422


def test_get_orders_requires_auth(client):
    response = client.get("/orders/")
    assert response.status_code == 401


def test_get_orders_as_admin(client, auth_headers):
    response = client.get("/orders/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_order_status(client, auth_headers, created_order_id):
    response = client.put(f"/orders/{created_order_id}", json={
        "status": "completed",
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_update_order_invalid_status(client, auth_headers, created_order_id):
    response = client.put(f"/orders/{created_order_id}", json={
        "status": "inexistente",
    }, headers=auth_headers)
    assert response.status_code == 400


def test_stats_after_completed_order(client, auth_headers):
    response = client.get("/stats/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_orders"] >= 1
    assert data["total_revenue"] > 0