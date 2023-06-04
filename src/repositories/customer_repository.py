

from typing import List
from fastapi import Depends
from sqlalchemy import and_, select
from src.database import SessionLocal
from src.models.user_model import Customer, Order
from src.oauth2 import get_current_user
from sqlalchemy.orm import joinedload, contains_eager

from src.schemas.customer_schemas import CustomerResponse, CustomerCreate


def add(customer_create: CustomerCreate, user_id: int ) -> Customer:
    with SessionLocal() as session:
        
        
        customer = Customer(user_id=user_id, **customer_create.dict())
        
        
        session.add(customer)
        session.commit()
        session.refresh(customer)
        session.close()
        
        return customer
    
def get_customer(user_id: int):
    with SessionLocal() as session:
        customer = session.scalars(select(Customer).options(joinedload(Customer.user)).filter_by(user_id = user_id).limit(1)).first()

    return customer

def get_orders(user_id: int):
    with SessionLocal() as session:
        customer = session.scalars(select(Customer).options(joinedload(Customer.order)).filter_by(user_id = user_id).limit(1)).first()
    if not customer:
        raise Exception
    return customer
