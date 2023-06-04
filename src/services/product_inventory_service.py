from src.models.user_model import Customer, Product, ProductCategory, ProductInventory, Suppliers
import src.repositories.product_inventory_repository as repository
from src.schemas.customer_schemas import CustomerResponse
from src.schemas.product_schemas import Inventory, ProductResponse

def create_inventory(category_create) -> ProductInventory:
    
    return repository.add(category_create)

def get_by_id(product_id):
    return repository.get_inventory(product_id)

def update_inventory(update_product):
    return repository.update(update_product,)