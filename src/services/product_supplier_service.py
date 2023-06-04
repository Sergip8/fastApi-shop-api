from src.models.user_model import Customer, Product, ProductCategory, Suppliers
import src.repositories.product_supplier_repository as repository
from src.schemas.customer_schemas import CustomerResponse
from src.schemas.product_schemas import ProductResponse

def create_supplier(category_create) -> Suppliers:
    
    return repository.add(category_create)

def get_by_id(product_id):
    return repository.get_supplier(product_id)

def update_supplier(update_product):
    return repository.update(update_product,)

def search_supplier(name:str):
    return repository.search_suppliers(name)