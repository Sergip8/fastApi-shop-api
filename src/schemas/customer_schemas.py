from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, conint
from src.schemas.order_schemas import Order, OrderResponse

from src.schemas.user_schemas import UserResponse


class Customer(BaseModel):
    firstname: str
    lastname: str

class CustomerResponse(Customer):
    id: int
    user: UserResponse
    class Config:
        orm_mode = True

class CustomerCreate(Customer):
    pass
class CustomerUpdate(Customer):
    id: int
    
class CustomerContactInfo(BaseModel):
    address_line1: str
    address_line2: str
    city: str
    postal_code: str
    telephone: str
    class Config:
        orm_mode = True

class CustomerContactCreate(CustomerContactInfo):
    pass

class CustomerContactUpdate(CustomerContactInfo):
    id: int
    pass

class CustomerPayment(BaseModel):
    
    payment_type: str
    provider: str
    account_no: str
    cvv: str
    expiry: str
    
    class Config:
        orm_mode = True

class CustomerPaymentCreate(CustomerPayment):
    pass

class CustomerPaymentUpdate(CustomerPayment):
    id: int
    
    pass


class CustomerOrderResponse(Customer):
    order: List[OrderResponse]
    class Config:
        orm_mode = True

