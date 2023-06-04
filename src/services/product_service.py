from src.models.user_model import Customer, Product, ProductCategory, Suppliers
import src.repositories.product_repository as repository
from src.schemas.customer_schemas import CustomerResponse
from src.schemas.product_schemas import ProductResponse

def create_product(category_create) -> Product:
    
    return repository.add(category_create)

def get_by_id(product_id):
    return repository.get_product(product_id)

def update_product(update_product):
    return repository.update_product(update_product,)

def search_product(name:str):
    return repository.search_product(name)