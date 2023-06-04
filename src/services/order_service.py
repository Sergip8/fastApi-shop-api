from src.models.user_model import Customer
import src.repositories.order_repository as repository
from src.schemas.customer_schemas import CustomerResponse

def create_order(customer_create, user_id):
    
    return repository.add(customer_create, user_id)

def get_user_by_id(user_id):
    return repository.get_customer(user_id)