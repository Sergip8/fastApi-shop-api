from typing import Optional
from fastapi import Depends
from sqlalchemy import select
from src.database import SessionLocal
from src.models.user_model import ProductCategory, User_contact_info, Customer
from src.oauth2 import get_current_user

from src.schemas.customer_schemas import CustomerContactCreate
from src.schemas.product_schemas import CategoryCreate, CategoryUpdate


def add(category_create: CategoryCreate) -> ProductCategory:
    print(category_create)
    with SessionLocal() as session:

      

        product_category = ProductCategory(**category_create.dict())
    
        
        
        session.add(product_category)
        session.commit()
        session.refresh(product_category)
        
        return product_category
    
def search_category(category_search_char: str):

    with SessionLocal() as session:
        category_query = session.query(ProductCategory).filter(ProductCategory.name.startswith(category_search_char))
    if not category_query:
        raise Exception
    return category_query.all()
# data = { "name": 'eafgsge', "description": 'The Hobbit', "images": "{ffff, asrgdrh}" }
#         statement = text("""INSERT INTO product_category(name, description, images) VALUES (:name, :description, :images)""")
#         session.execute(statement, **data)

def update(category_update: CategoryUpdate)-> ProductCategory:
    with SessionLocal() as session:
        inventory_query = session.query(ProductCategory).filter(ProductCategory.id == category_update.id)
       
        if not inventory_query.first():
            raise Exception
        inventory_query.update(category_update.dict(), synchronize_session=False)
        session.commit()
    return inventory_query.first()