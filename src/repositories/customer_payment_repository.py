from typing import List, Optional
from fastapi import Depends
from sqlalchemy import select, update
from src.database import SessionLocal
from src.models.user_model import User_contact_info, Customer, User_payment


from src.schemas.customer_schemas import CustomerPaymentCreate, CustomerPaymentUpdate


def add(customer_create: CustomerPaymentCreate, user_id: int ) -> User_payment:
    with SessionLocal() as session:

        customer: Optional[Customer] = session.scalars(select(Customer).filter_by(user_id = user_id).limit(1)).first()
        if not customer:
            raise Exception

        print(customer.id)
        customer_payment = User_payment(customer_id=customer.id, **customer_create.dict())
        
        
        session.add(customer_payment)
        session.commit()
        session.refresh(customer_payment)
        session.close()
        return customer_payment
    
def get_customer_payment(user_id: int) -> List[User_payment]:
    with SessionLocal() as session:
        customer: Optional[Customer] = session.scalars(select(Customer).filter_by(user_id = user_id).limit(1)).first()
        customer_payment = session.query(User_payment).filter(User_payment.customer_id == customer.id).all()
    return customer_payment

def update_payment(payment_update: CustomerPaymentUpdate, user_id: int) -> User_payment:
    with SessionLocal() as session:
        customer = session.scalars(select(Customer).filter_by(user_id = user_id).limit(1)).first()
       
        if not customer:
           raise Exception
        #payment_query = session.scalars(select(User_payment).where((User_payment.id == payment_update.id)& (User_payment.customer_id == customer.id)))
        
        payment_query = session.query(User_payment).filter(User_payment.id == payment_update.id)

        # payment_query = session.execute(update(User_payment)
        # .where((User_payment.id == payment_update.id)& 
        # (User_payment.customer_id == customer.id))
        # .values(payment_update.dict()).execution_options(
        # synchronize_session="evaluate"
        # ))
        
      
        if not payment_query.first() and payment_query.first().customer_id != customer.id:
            raise Exception
        payment_query.update(payment_update.dict(), synchronize_session=False)
        session.commit()
        return payment_query.first()

def delete_by_id(payment_id: int) -> None:
    with SessionLocal() as session:
        payment_delete: Optional[User_payment] = session.get(User_payment, payment_id)
        if not payment_delete:
            raise Exception
        session.delete(payment_delete)
        session.commit()
