

import pytest
from src.models.user_model import Customer
from src.schemas.customer_schemas import CustomerContactInfo, CustomerPayment, CustomerResponse


def test_get_customer_user(auth_client, test_customer):
    res = auth_client.get("/customers/")
    assert res.status_code == 200
    assert res.json()["firstname"] == test_customer.firstname
    assert res.json()["lastname"] == test_customer.lastname
    
def test_get_customer_user_without_permission(auth_client_without_permissions, test_customer):
    res = auth_client_without_permissions.get("/customers/")
    assert res.status_code == 401
  

def test_unauth_get_customer(client, test_customer):
    res = client.get("/customers/")
    print(res.status_code)
    assert res.status_code == 401

@pytest.mark.parametrize("firstname, lastname", [
    ("dghfhfff", "wwwwww"),
    ("dsfsdgggg", "bbbbbbb"),
    ("ggnnnbvv", "wahoo"),
])
def test_create_customer(auth_client, test_user, firstname, lastname):
    res = auth_client.post(
        "/customers/", json={"firstname": firstname, "lastname": lastname})

    created_post = CustomerResponse(**res.json())
    assert res.status_code == 201
    assert created_post.firstname == firstname
    assert created_post.lastname == lastname
    assert created_post.user.id == test_user['id']    
    assert created_post.user.email == test_user["email"]


def test_create_customer_without_permission(auth_client_without_permissions, test_user,):
    res = auth_client_without_permissions.post(
        "/customers/", json={"firstname": "firstname", "lastname": "lastname"})

    assert res.status_code == 401
   

def test_update_customer(auth_client, test_user, test_customer):
    data = {
        "firstname": "updated title",
        "lastname": "updatd content",
        "id": test_customer.id
    }
    res = auth_client.put(f"/customers/", json=data)
    updated_post = CustomerResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.firstname == data['firstname']
    assert updated_post.lastname == data['lastname']
    
def test_get_payments_customer(auth_client, test_customer_payment):
    res = auth_client.get("/customers_payment/")
    assert res.status_code == 200
    #assert len(res.json()) == len(test_customer_payment)


def test_unauth_get_customer_payment(client, test_customer_payment):
    res = client.get("/customers_payment/")
    print(res.status_code)
    assert res.status_code == 401

def test_delete_customer_payment_auth(auth_client, test_user, test_customer_payment):
    res = auth_client.delete(f"/customers_payment/{test_customer_payment[0].id}")
    assert res.status_code == 204

def test_delete_other_user_post(auth_client, test_user, test_customer_payment):
    res = auth_client.delete(
        f"/customers_payment/{test_customer_payment[2].id}")
    assert res.status_code == 403


def test_delete_customer_payment_no_auth(client, test_user, test_customer_payment):
    res = client.delete(f"/customers_payment/{test_customer_payment[0].id}")
    assert res.status_code == 401

def test_delete_customer_payment_auth_no_exist(auth_client, test_user, test_customer_payment):
    res = auth_client.delete(f"/customers_payment/{200000}")
    assert res.status_code == 404

@pytest.mark.parametrize("payment_type, provider, account_no, cvv, expiry", [
    ("visa", "wwwwww", "65165", "542", "11/28"),
    ("vaso", "bbbbbbb", "845156", "545", "03/28"),
    ("vosa", "wahoo", "6541654", "661", "05/28"),
])
def test_create_customer_payment(auth_client, test_user, test_customer, payment_type, provider, account_no, cvv, expiry):
    res = auth_client.post(
        "/customers_payment/", json={"payment_type": payment_type, "provider": provider, "account_no": account_no, "cvv": cvv, "expiry": expiry})

    created_post = CustomerPayment(**res.json())
    assert res.status_code == 201
    assert created_post.provider == provider
    assert created_post.account_no == account_no
    

def test_update_customer_payment(auth_client, test_user, test_customer_payment):
    data = {
        "payment_type": "visa",
        "provider": "stridf",
        "account_no": "1231454",
        "cvv": "569",
        "expiry": "11/28",
        "id": test_customer_payment[0].id
    }
    res = auth_client.put(f"/customers_payment/", json=data)
    updated_post = CustomerPayment(**res.json())
    assert res.status_code == 200
    assert updated_post.provider == data['provider']
    assert updated_post.payment_type == data['payment_type']
    

def test_get_contact_customer(auth_client, test_customer_contact):
    res = auth_client.get("/customers_contact/")
    assert res.status_code == 200
    #assert len(res.json()) == len(test_customer_payment)

def test_unauth_get_customer_contact(client, test_customer_contact):
    res = client.get("/customers_contact/")
    print(res.status_code)
    assert res.status_code == 401

@pytest.mark.parametrize("address_line1, address_line2, city, postal_code, telephone", [
    ("asdf556f", "fd65h45g", "ggggg", "112223", "56456546"),
    ("g4654fd6", "f56d5fg5", "fffff", "522134", "78645663"),
    ("tf65y465", "sd5f56s5", "ddddd", "333466", "04564533"),
])
def test_create_customer_contact(auth_client, test_user, test_customer, address_line1, address_line2, city, postal_code, telephone):
    res = auth_client.post(
        "/customers_contact/", json={"address_line1": address_line1, "address_line2": address_line2, "city": city, "postal_code": postal_code, "telephone": telephone})

    created_post = CustomerContactInfo(**res.json())
    assert res.status_code == 201
    assert created_post.address_line1 == address_line1
    assert created_post.postal_code == postal_code
    

def test_update_customer_contact(auth_client, test_user, test_customer_contact):
    data = {
        "address_line1": "string",
        "address_line2": "string",
        "city": "string",
        "postal_code": "string",
        "telephone": "65416516",
        "id": test_customer_contact.id
    }
    res = auth_client.put(f"/customers_contact/", json=data)
    updated_post = CustomerContactInfo(**res.json())
    assert res.status_code == 200
    assert updated_post.address_line1 == data['address_line1']
    assert updated_post.telephone == data['telephone']