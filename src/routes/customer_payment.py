from typing import Annotated, List, Optional, Sequence
from fastapi import APIRouter, Depends, Response, Security, status
from sqlalchemy import select
from src.models.user_model import Customer, User_payment
from src.schemas.customer_schemas import CustomerContactCreate, CustomerContactInfo, CustomerCreate, CustomerPayment, CustomerPaymentCreate, CustomerPaymentUpdate, CustomerResponse
from src.schemas.user_schemas import TokenData, UserCreate, UserResponse
import src.services.customer_payment_service as service
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.oauth2 import get_current_user
from sqlalchemy.orm import Session, joinedload
from src.database import get_db

router = APIRouter()

router = APIRouter(prefix="/customers_payment", 
                   responses={404: {"message": "No hay de eso"}},
                   tags=["customers_payment"])



@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CustomerPayment])

def get_by_user_id(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_read"])],
    session: Session = Depends(get_db)):
    try:
        customer: Optional[Customer] = session.scalars(select(Customer).filter_by(user_id = user_data.user_id)).first()
        customer_payment = session.scalars(select(User_payment).filter_by(customer_id = customer.id)).all()

        return customer_payment
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontro metodo de pago")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= CustomerPayment)

def customer_payment_create(
    customer_create: CustomerPaymentCreate, 
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_write"])], 
    session: Session = Depends(get_db)):
 
    try:
        customer: Optional[Customer] = session.scalars(select(Customer).filter_by(user_id = user_data.user_id)).first()
        if not customer:
            raise Exception
        customer_payment = User_payment(customer_id=customer.id, **customer_create.dict())
        
        
        session.add(customer_payment)
        session.commit()
        session.refresh(customer_payment)
       
        return customer_payment
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo registrar")
    

@router.put("/", status_code=status.HTTP_200_OK, response_model= CustomerPayment)

def payment_update(
    payment_update: CustomerPaymentUpdate, 
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_write"])],
    session: Session = Depends(get_db)):

    try:
        customer = session.scalars(select(Customer).filter_by(user_id = user_data.user_id)).first()
        if not customer:
           raise Exception
        
        payment_query = session.query(User_payment).filter(User_payment.id == payment_update.id)
      
        if not payment_query.first() and payment_query.first().customer_id != customer.id:
            raise Exception
        payment_query.update(payment_update.dict(), synchronize_session=False)
        session.commit()
        return payment_query.first()
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo registrar")


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)

def payment_delete(
    payment_id: int, 
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_write"])],
    session: Session = Depends(get_db)):

    try:
        payment = session.get(User_payment, payment_id)
        if not payment:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontro el metodo de pago")
        customer = session.scalars(select(Customer).filter_by(user_id = user_data.user_id)).first()
        if not customer:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontro cliente")
        if customer.id != payment.customer_id:
            return Response(status_code=status.HTTP_403_FORBIDDEN, content="el metodo de pago no es del cliente")

       
        if not payment:
            raise Exception
        session.delete(payment)
        session.commit()
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo registrar")