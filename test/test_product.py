

import pytest

from src.models.user_model import Product, ProductCategory, ProductInventory, Suppliers


def test_get_supplier(auth_client_advance, test_supplier):
    supplier_id = test_supplier.id
    res = auth_client_advance.get(f"/supplier/{supplier_id}")
    assert res.status_code == 200
    assert res.json()["address"] == test_supplier.address
    assert res.json()["telephone"] == test_supplier.telephone
    assert res.json()["email"] == test_supplier.email

def test_get_supplier_without_permission(auth_client, test_supplier):
    supplier_id = test_supplier.id
    res = auth_client.get(f"/supplier/{supplier_id}")
    assert res.status_code == 401

@pytest.mark.parametrize("name, address, city, supplier_id, postal_code, telephone, country, web_page, email", [
    ("dghfhfff", "wwwwww", "bog", "65413516", "654655", "5646518", "setr", "wwwfsadfsdg", "qqq@qq.com"),
    ("dgfff", "wwwww", "bog", "65456316", "744655", "886456518", "setr", "wwwfsadfsdg", "rrr@qq.com"),
    ("dghfh", "wwww", "bog", "43543516", "577855", "11521518", "setr", "wwwfsadfsdg", "aaa@qq.com"),

])
def test_create_supplier(auth_client_advance, name, address, city, supplier_id, postal_code, telephone, country, web_page, email):
    res = auth_client_advance.post(
        "/supplier/", json={"name": name, "address": address, "city": city, 
                             "supplier_id": supplier_id, "postal_code": postal_code, 
                             "telephone": telephone, "country": country, 
                             "web_page": web_page, "email": email})

    created_post = Suppliers(**res.json())
    assert res.status_code == 201
    assert created_post.address == address
    assert created_post.postal_code == postal_code
   
def test_create_supplier_without_permission(auth_client):
    res = auth_client.post(
        "/supplier/", json={"name": "name", "address": "address", "city": "city", 
                             "supplier_id": "supplier_id", "postal_code": "postal_code", 
                             "telephone": "telephone", "country": "country", 
                             "web_page": "web_page", "email": "email"})
    assert res.status_code == 401

def test_update_supplier(auth_client_advance, test_supplier):
    res = auth_client_advance.put(
        "/supplier/", json={"name": "name", "address": "address", "city": "city", 
                             "supplier_id": "supplier_id", "postal_code": "postal", 
                             "telephone": "telephone", "country": "country", 
                             "web_page": "web_page", "email": "user@example.com", "id": test_supplier.id})
    assert res.status_code == 200

#=========================== test product category ============================

def test_get_category(auth_client, test_category):
    category_id = test_category.id
    res = auth_client.get(f"/product_category/{category_id}")
    assert res.status_code == 200
    assert res.json()["name"] == test_category.name
    assert res.json()["description"] == test_category.description
    assert res.json()["images"] == test_category.images

def test_search_category(client, test_category):
    
    res = client.get("/product_category?name=st")
    assert res.status_code == 200
    assert res.json()[0]["name"] == test_category.name
    assert res.json()[0]["description"] == test_category.description
    assert res.json()[0]["images"] == test_category.images

@pytest.mark.parametrize("name, description, images", [
    ("dghfhfff", "wwwwww", ["qqefogb", "oisjgodsg", "ifjgidfgn", "sgokgpoos"]),
    ("dgfff", "wwwww", ["oafgfggb", "oodsg", "oishdgoigdo"]),
    ("dghfh", "wwww", ["oid", "asffodsg"]),

])
def test_create_category(auth_client_advance, name, description, images):
    res = auth_client_advance.post(
        "/product_category/", json={"name": name, "description": description, "images": images,})

    created_post = ProductCategory(**res.json())
    assert res.status_code == 201
    assert created_post.name == name
    assert created_post.description == description

def test_update_category_without_permission(auth_client, test_category):
    res = auth_client.put(
        "/product_category/", json={"name": "name", "description": "description", "images": ["images","images","images"], "id":test_category.id})
    assert res.status_code == 401
   
def test_create_category_without_permission(auth_client):
    res = auth_client.post(
        "/product_category/", json={"name": "name", "description": "description", "images": ["images","images","images"]})
    assert res.status_code == 401

def test_update_category(auth_client_advance, test_category):
    res = auth_client_advance.put(
        "/product_category/", json={"name": "name", "description": "description", "images": ["images","images","images"], "id":test_category.id})
    assert res.status_code == 200
    
#=========================== test product ============================


def test_get_product(auth_client_advance, test_product):
    product_id = test_product.id
    res = auth_client_advance.get(f"/product/{product_id}")
    assert res.status_code == 200
    assert res.json()["name"] == test_product.name
    assert res.json()["SKU"] == test_product.SKU
    assert res.json()["tax"] == test_product.tax

@pytest.mark.parametrize("name, description, SKU, unit_price, tax, discontinued", [
    ("dghfhfff", "wwwwww", "676dd", 222.2, 5, False),
    ("dgfff", "wwwww", "dd546", 5466.2, 19, True),
    ("dghfh", "wwww", "baa54", 4894.2, 10, False),

])
def test_create_product(auth_client_advance, test_supplier, test_category, name, description, SKU, unit_price, tax, discontinued):
    res = auth_client_advance.post(
        "/product/", json={"name": name, "description": description, "SKU": SKU, 
                             "unit_price": unit_price, "tax": tax, 
                             "discontinued": discontinued,
                             "supplier_id": test_supplier.id,
                             "category_id": test_category.id})

    created_product = Product(**res.json())
    assert res.status_code == 201
    assert created_product.unit_price == unit_price
    assert created_product.SKU == SKU

def test_update_product(auth_client_advance, test_product):
    res = auth_client_advance.put(
        "/product/", json={"name": "name", "description": "description", "SKU": "SKU", 
                             "unit_price": 5546545, "tax": 5, 
                             "discontinued": True,
                             "id": test_product.id,
                             "supplier_id": test_product.supplier_id,
                             "category_id": test_product.category_id})

    
    assert res.status_code == 200
    
def test_search_product(client, test_products):
    limit = 3
    res = client.get(f"/product?name=sg&limit={limit}")
    assert res.status_code == 200
    assert len(res.json()) == limit

#=========================== test product inventory ============================

def test_get_product_inventory(auth_client_advance, test_inventory):
    inventory_id = test_inventory.id
    res = auth_client_advance.get(f"/product_inventory/{inventory_id}")
    assert res.status_code == 200
    assert res.json()["units_in_stock"] == test_inventory.units_in_stock
    assert res.json()["qty_per_unit"] == test_inventory.qty_per_unit

@pytest.mark.parametrize("units_in_stock, qty_per_unit", [
    (200, 10),
    (543, 5),
    (88, 8),

])
def test_create_inventory(auth_client_advance, test_product, units_in_stock, qty_per_unit):
    res = auth_client_advance.post(
        "/product_inventory/", json={"units_in_stock": units_in_stock, "qty_per_unit": qty_per_unit, "product_id": test_product.id})

    created_post = ProductInventory(**res.json())
    assert res.status_code == 201
    assert created_post.units_in_stock == units_in_stock
    assert created_post.qty_per_unit == qty_per_unit

def test_update_inventory(auth_client_advance, test_inventory, ):
    res = auth_client_advance.put(
        "/product_inventory/", json={"units_in_stock": 455, "qty_per_unit": 7, "product_id": test_inventory.product_id, "id": test_inventory.id})

    assert res.status_code == 200
  