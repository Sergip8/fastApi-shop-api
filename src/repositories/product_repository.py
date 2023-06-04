from typing import Optional
from fastapi import Depends
from sqlalchemy import select, update
from src.database import SessionLocal
from src.models.user_model import Product, ProductCategory, User_contact_info, Customer


from src.schemas.customer_schemas import CustomerContactCreate
from src.schemas.product_schemas import CategoryCreate, ProductCreate, ProductResponse, ProductUpdate


def add(category_create: ProductCreate) -> Product:
    print(category_create)
    with SessionLocal() as session:

        product_category = Product(**category_create.dict())
        
        session.add(product_category)
        session.commit()
        session.refresh(product_category)
        session.close()
        return product_category
    
def get_product(product_id: int):
    with SessionLocal() as session:
        product = session.scalars(select(Product).filter_by(id = product_id).limit(1)).first()
        if not product:
            raise Exception
    return product

def update_product(product_update: ProductUpdate):
    with SessionLocal() as session:
        product_query = session.query(Product).filter(Product.id == product_update.id)
       
        if not product_query.first():
            raise Exception
        product_query.update(product_update.dict(), synchronize_session=False)
        session.commit()
    return product_query.first()

def search_product(product_search_char: str):
    with SessionLocal() as session:
        product_query = session.query(Product).filter(Product.name.startswith(product_search_char))
    if not product_query:
        raise Exception
    return product_query.all()