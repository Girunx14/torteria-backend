# tests/test_products.py


def test_create_product(client, auth_headers):
    # Primero asegurar que existe la categoría
    client.post("/categories/", json={"name": "TestCat"}, headers=auth_headers)

    response = client.post("/products/", json={
        "name": "Torta de Jamón",
        "description": "Con queso y jalapeño",
        "price": 55.00,
        "category_id": 1,
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Torta de Jamón"
    assert float(data["price"]) == 55.0


def test_get_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_product_by_id(client):
    response = client.get("/products/1")
    assert response.status_code == 200


def test_get_product_not_found(client):
    response = client.get("/products/9999")
    assert response.status_code == 404


def test_update_product(client, auth_headers):
    response = client.put("/products/1", json={
        "price": 60.00,
    }, headers=auth_headers)
    assert response.status_code == 200
    assert float(response.json()["price"]) == 60.0


def test_create_product_invalid_price(client, auth_headers):
    response = client.post("/products/", json={
        "name": "Producto inválido",
        "price": -10.00,
        "category_id": 1,
    }, headers=auth_headers)
    assert response.status_code == 422


def test_create_product_unauthorized(client):
    response = client.post("/products/", json={
        "name": "Sin auth",
        "price": 50.00,
        "category_id": 1,
    })
    assert response.status_code == 401