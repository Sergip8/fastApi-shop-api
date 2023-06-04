from typing import Optional
from fastapi import Depends
from sqlalchemy import select
from src.database import SessionLocal
from src.models.user_model import Suppliers, User_contact_info, Customer, User_payment

from src.schemas.product_schemas import SupplierCreate


def add(supplier_create: SupplierCreate) -> Suppliers:
    with SessionLocal() as session:


       
        supplier = Suppliers(**supplier_create.dict())
        
        
        session.add(supplier)
        session.commit()
        session.refresh(supplier)
        
        return supplier
    
def get_supplier(supplier_id: int):
    with SessionLocal() as session:
        customer = session.get(Suppliers, supplier_id)

    return customer

def search_suppliers(supplier_search_char: str):
    with SessionLocal() as session:
        product_query = session.query(Suppliers).filter(Suppliers.name.startswith(supplier_search_char))
    if not product_query:
        raise Exception
    return product_query.all()