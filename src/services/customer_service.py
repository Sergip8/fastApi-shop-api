
from src.models.user_model import Customer
import src.repositories.customer_repository as repository
from src.schemas.customer_schemas import CustomerResponse

def create_customer(customer_create, user_id) -> Customer:
    
    return repository.add(customer_create, user_id)

def get_user_by_id(user_id):
    return repository.get_customer(user_id)

def get_orders(user_id):
    return repository.get_orders(user_id)

def get_orders_by_status(user_id, sta):
    customer = repository.get_orders(user_id)
    order = []
    for o in customer.order:
        if o.status == sta:
            order.append(o)
    customer.order = order
    return customer