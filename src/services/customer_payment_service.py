
from src.models.user_model import Customer, User_contact_info, User_payment
import src.repositories.customer_payment_repository as repository
from src.schemas.customer_schemas import CustomerContactInfo, CustomerResponse

def customer_payment_create(customer_create, user_id) -> User_payment:
    
    return repository.add(customer_create, user_id)

def get_user_by_id(user_id):
    return repository.get_customer_payment(user_id)

def customer_payment_update(customer_update, user_id):
    return repository.update_payment(customer_update, user_id)

def customer_payment_delete(payment_id: int):
    return repository.delete_by_id(payment_id)