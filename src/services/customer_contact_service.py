
from src.models.user_model import Customer, User_contact_info
import src.repositories.customer_contact_repository as repository
from src.schemas.customer_schemas import CustomerContactInfo, CustomerResponse

def customer_contact_create(customer_create, user_id) -> User_contact_info:
    
    return repository.add(customer_create, user_id)

def get_customer_contact(user_id):
    return repository.get_customer_contact(user_id)

def customer_contact_update(contact_update, user_id):
    return repository.contact_update(contact_update, user_id)
