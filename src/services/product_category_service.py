from src.models.user_model import Customer, ProductCategory, Suppliers
import src.repositories.product_category_repository as repository
from src.schemas.customer_schemas import CustomerResponse

def category_create(category_create) -> ProductCategory:
    
    return repository.add(category_create)

def get_by_name(name: str):
    return repository.search_category(name)

def update_category(update_product):
    return repository.update(update_product,)

def search_category(name:str):
    return repository.search_category(name)