
from typing import List
import pytest
from sqlalchemy import create_engine
from src.models import user_model
from fastapi.testclient import TestClient
from src.application import app
from src.oauth2 import create_token
from src.database import SessionLocal
from src.config import settings
from src.database import get_db
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL_TEST = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test'    


engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    user_model.Base.metadata.drop_all(engine)
    user_model.Base.metadata.create_all(engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "xfg@ff.com", "password": "1234", "permissions":["basic_write","basic_read",]}
    res = client.post("/users/", json= user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_advance_user(client):
    user_data = {"email": "xfkkg@ff.com", "password": "1234", "permissions":  ["basic_write",
    "basic_read",
    "advance_write",
    "advance_read"]}
    res = client.post("/users/", json= user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user




@pytest.fixture
def test_other_user(client):
    user_data = {"email": "xxx@ff.com", "password": "1234", "permissions":["basic_write","basic_read",]}
    res = client.post("/users/", json= user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user_without_permissions(client):
    user_data = {"email": "xxx@ff.com", "password": "1234", "permissions":[]}
    res = client.post("/users/", json= user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token_without_permissions(test_user_without_permissions):
    #print(create_token({"user_id": test_user["id"], "email": test_user["email"]}))
    return create_token({"user_id": test_user_without_permissions["id"], "email": test_user_without_permissions["email"], "scopes": test_user_without_permissions["permissions"]["permissions"]})

@pytest.fixture
def token_advance_user(test_advance_user):
    #print(create_token({"user_id": test_user["id"], "email": test_user["email"]}))
    return create_token({"user_id": test_advance_user["id"], "email": test_advance_user["email"], "scopes": test_advance_user["permissions"]["permissions"]})



@pytest.fixture
def token(test_user):
    #print(create_token({"user_id": test_user["id"], "email": test_user["email"]}))
    return create_token({"user_id": test_user["id"], "email": test_user["email"], "scopes": test_user["permissions"]["permissions"]})

@pytest.fixture
def auth_client_without_permissions(client, token_without_permissions):
    #print(token)
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_without_permissions}"
    }
    return client

@pytest.fixture
def auth_client_advance(client, token_advance_user):
    #print(token)
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_advance_user}"
    }
    return client


@pytest.fixture
def auth_client(client, token):
    #print(token)
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_customer(session, test_user,):
    post_data = {
    "firstname": "sasffg",
    "lastname": "asf"
    }
    customer = user_model.Customer(user_id=test_user["id"], **post_data, )
    session.add(customer)
    session.commit()
    session.refresh(customer)
    session.close()
    return customer

@pytest.fixture
def test_other_customer(session, test_other_user):
    post_data = {
    "firstname": "rdjtgykj",
    "lastname": "dgykk"
    }
    customer = user_model.Customer(user_id=test_other_user["id"], **post_data)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    session.close()
    return customer

@pytest.fixture
def test_customer_payment(session, test_customer, test_other_customer):
    payment_data =[{
    "payment_type": "visa",
    "provider": "stri",
    "account_no": "1231454",
    "cvv": "abc",
    "expiry": "11/28",
    "customer_id": test_customer.id
    },
    {
    "payment_type": "visa",
    "provider": "stri",
    "account_no": "1231454",
    "cvv": "abc",
    "expiry": "11/28",
    "customer_id": test_customer.id
    },
    {
    "payment_type": "visa",
    "provider": "stri",
    "account_no": "1231454",
    "cvv": "abc",
    "expiry": "11/28",
    "customer_id": test_other_customer.id
    },]
    
    payments = [user_model.User_payment(**p) for p in payment_data]
    session.add_all(payments)
    session.commit()
    payments = session.query(user_model.User_payment).all()
    return payments

@pytest.fixture
def test_customer_contact(session, test_customer):
    contact_data ={
  "address_line1": "string",
  "address_line2": "string",
  "city": "string",
  "postal_code": "string",
  "telephone": "string",
  "customer_id": test_customer.id
}
    
    contact = user_model.User_contact_info(**contact_data)
    session.add(contact)
    session.commit()
    contact = session.query(user_model.User_contact_info).first()
    return contact
        

@pytest.fixture
def test_supplier(session):
    supplier_data = {
  "name": "string",
  "address": "string",
  "city": "string",
  "supplier_id": "36516516",
  "postal_code": "stri",
  "telephone": "string",
  "country": "string",
  "web_page": "string",
  "email": "user@example.com"
}
    supplier = user_model.Suppliers(**supplier_data)
    session.add(supplier)
    session.commit()
    session.refresh(supplier)
    session.close()
    return supplier

@pytest.fixture
def test_category(session):
    category_data = {
  "name": "stringasrh",
  "description": "strinsthfth",
  "images": ["segsgsg", "segsesg"]
}
    category = user_model.ProductCategory(**category_data)
    session.add(category)
    session.commit()
    session.refresh(category)
    session.close()
    return category

@pytest.fixture
def test_product(session, test_category, test_supplier):
    data_product = {
  "name": "sgh",
  "description": "shhsgs",
  "SKU": "dshsd",
  "unit_price": 20000.2,
  "tax": 5,
  "discontinued": False,
  "supplier_id": test_supplier.id,
  "category_id": test_category.id
}

    product = user_model.Product(**data_product)
    session.add(product)
    session.commit()
    session.refresh(product)
    session.close()
    return product

@pytest.fixture
def test_products(session, test_category, test_supplier):
    data_product = [{
  "name": "sgh",
  "description": "shhsgs",
  "SKU": "dshsd",
  "unit_price": 20000.2,
  "tax": 5,
  "discontinued": False,
  "supplier_id": test_supplier.id,
  "category_id": test_category.id
},
{
  "name": "sgh",
  "description": "shhsgs",
  "SKU": "dshsd",
  "unit_price": 20000.2,
  "tax": 5,
  "discontinued": False,
  "supplier_id": test_supplier.id,
  "category_id": test_category.id
},
{
  "name": "sgh",
  "description": "shhsgs",
  "SKU": "dshsd",
  "unit_price": 20000.2,
  "tax": 5,
  "discontinued": False,
  "supplier_id": test_supplier.id,
  "category_id": test_category.id
},
{
  "name": "sgh",
  "description": "shhsgs",
  "SKU": "dshsd",
  "unit_price": 20000.2,
  "tax": 5,
  "discontinued": False,
  "supplier_id": test_supplier.id,
  "category_id": test_category.id
},
{
  "name": "sgh",
  "description": "shhsgs",
  "SKU": "dshsd",
  "unit_price": 20000.2,
  "tax": 5,
  "discontinued": False,
  "supplier_id": test_supplier.id,
  "category_id": test_category.id
},]

    product = [user_model.Product(**p) for p in data_product]
    session.add_all(product)
    session.commit()
    payments = session.query(user_model.Product).all()
    return payments

@pytest.fixture
def test_inventory(session, test_product):
    data_inventory = {
  "units_in_stock": 200,
  "qty_per_unit": 2,
  "product_id": test_product.id
}

    inventory = user_model.ProductInventory(**data_inventory)
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    session.close()
    return inventory

@pytest.fixture
def test_order(session, test_customer):
    data_order={
        "total": 544565,
        "status": "paid",
        "customer_id": test_customer.id
    }
    order = user_model.Order(**data_order)
    session.add(order)
    session.commit()
    session.refresh(order)
    session.close()
    return order

@pytest.fixture
def test_items_order(session, test_product, test_order):
    data_items=[{
        "qty": 10,
        "price": 222,
        "product_id": test_product.id,
        "order_id": test_order.id
    },
    {
        "qty": 3,
        "price": 6546,
        "product_id": test_product.id,
        "order_id": test_order.id
    },
    {
        "qty": 156,
        "price": 2234,
        "product_id": test_product.id,
        "order_id": test_order.id
    },
    {
        "qty": 87,
        "price": 44556,
        "product_id": test_product.id,
        "order_id": test_order.id
    },
    {
        "qty": 1,
        "price": 778990,
        "product_id": test_product.id,
        "order_id": test_order.id
    },
    {
        "qty": 10,
        "price": 33445,
        "product_id": test_product.id,
        "order_id": test_order.id
    },
    ]
    order_items = [user_model.OrderItems(**oi) for oi in data_items]
    session.add_all(order_items)
    session.commit()
    order_items = session.query(user_model.OrderItems).all()
    return order_items