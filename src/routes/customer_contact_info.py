from typing import Annotated, List, Optional, Sequence
from fastapi import APIRouter, Depends, Response, Security, status
from sqlalchemy import select
from src.models.user_model import Customer, User_contact_info
from src.schemas.customer_schemas import CustomerContactCreate, CustomerContactInfo, CustomerContactUpdate, CustomerCreate, CustomerResponse
from src.schemas.user_schemas import TokenData, UserCreate, UserResponse
import src.services.customer_contact_service as service
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.oauth2 import get_current_user
from sqlalchemy.orm import Session
from src.database import get_db

router = APIRouter()

router = APIRouter(prefix="/customers_contact", 
                   responses={404: {"message": "No hay de eso"}},
                   tags=["customers_contact"])



@router.get("/", status_code=status.HTTP_200_OK, response_model=CustomerContactInfo)

def get_by_id(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_read"])],
    session: Session = Depends(get_db)):
    try:
        customer: Optional[Customer] = session.scalars(select(Customer).filter_by(user_id = user_data.user_id).limit(1)).first()
        if not customer:
            raise Exception
        customer_contact = session.query(User_contact_info).filter(User_contact_info.customer_id == customer.id).first()
        return customer_contact

    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontro informacion de contacto")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= CustomerContactInfo)

def customer_contact_create(
    customer_create: CustomerContactCreate, 
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_write"])], 
    session: Session = Depends(get_db)):

    try:
        customer: Optional[Customer] = session.scalars(select(Customer).filter_by(user_id = user_data.user_id)).first()
        if not customer:
            raise Exception
        customer_contact = User_contact_info(customer_id=customer.id, **customer_create.dict())
        
        
        session.add(customer_contact)
        session.commit()
        session.refresh(customer_contact)
        return customer_contact
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo registrar")
    

@router.put("/", status_code=status.HTTP_200_OK, response_model= CustomerContactInfo)

def contact_update(
    contact_update: CustomerContactUpdate, 
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_write"])],
    session: Session = Depends(get_db)):

    try:
        customer = session.scalars(select(Customer).filter_by(user_id = user_data.user_id)).first()
       
        if not customer:
           raise Exception
        #payment_query = session.scalars(select(User_payment).where((User_payment.id == payment_update.id)& (User_payment.customer_id == customer.id)))
        
        payment_query = session.query(User_contact_info).filter(User_contact_info.id == contact_update.id)
        if not payment_query.first() and payment_query.first().customer_id != customer.id:
            raise Exception
        payment_query.update(contact_update.dict(), synchronize_session=False)
        session.commit()
        return payment_query.first()
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo actualizar los datos")
 