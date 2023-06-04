from typing import List, Optional
from fastapi import Depends
from sqlalchemy import select
from src.database import SessionLocal
from src.models.user_model import User_contact_info, Customer
from src.oauth2 import get_current_user

from src.schemas.customer_schemas import CustomerContactCreate, CustomerContactUpdate


def add(customer_create: CustomerContactCreate, user_id: int ) -> User_contact_info:
    with SessionLocal() as session:

        customer: Optional[Customer] = session.scalars(select(Customer).filter_by(user_id = user_id).limit(1)).first()
        if not customer:
            raise Exception

        print(customer.id)
        customer_contact = User_contact_info(customer_id=customer.id, **customer_create.dict())
        
        
        session.add(customer_contact)
        session.commit()
        session.refresh(customer_contact)
        session.close()
        return customer_contact
    


def get_customer_contact(user_id: int) -> User_contact_info:
    with SessionLocal() as session:
        customer: Optional[Customer] = session.scalars(select(Customer).filter_by(user_id = user_id).limit(1)).first()
        if not customer:
            raise Exception
        customer_contact = session.query(User_contact_info).filter(User_contact_info.customer_id == customer.id).first()
    return customer_contact

def contact_update(contact_update: CustomerContactUpdate, user_id: int) -> User_contact_info:
    with SessionLocal() as session:
        customer = session.scalars(select(Customer).filter_by(user_id = user_id).limit(1)).first()
       
        if not customer:
           raise Exception
        #payment_query = session.scalars(select(User_payment).where((User_payment.id == payment_update.id)& (User_payment.customer_id == customer.id)))
        
        payment_query = session.query(User_contact_info).filter(User_contact_info.id == contact_update.id)
        if not payment_query.first() and payment_query.first().customer_id != customer.id:
            raise Exception
        payment_query.update(contact_update.dict(), synchronize_session=False)
        session.commit()
        return payment_query.first()