import decimal
from typing import Annotated, List, Optional, Sequence
from fastapi import APIRouter, Depends, Response, Security, status
from sqlalchemy import select
from src.models.user_model import Customer, Order, OrderItems, Product
from src.schemas.customer_schemas import CustomerCreate, CustomerResponse
from src.schemas.order_schemas import CreateOrder, OrderResponse
from src.schemas.user_schemas import TokenData
import src.services.order_service as service
from src.oauth2 import get_current_user
from sqlalchemy.orm import Session, joinedload
from src.database import get_db

router = APIRouter(prefix="/order", 
                   responses={404: {"message": "No hay de eso"}},
                   tags=["order"])



@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)

def get_by_id(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["advance_read"])],
    order_id: int, 
    session: Session = Depends(get_db)):
    try:
        customer = session.scalars(select(Order).filter_by(id = order_id)).first()
        return customer
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontro al usuario")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= OrderResponse)

def order_create(
    order_create: CreateOrder, 
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_read"])],
    session: Session = Depends(get_db)):

    
    
        customer = session.scalars(select(Customer).filter_by(user_id = user_data.user_id)).first()
        _o = order_create.dict()
        item_order =  _o.pop("items_order")
        print("--------------")
        print(customer.id)
        # if customer == None:
        #     raise Exception
        order = Order(customer_id=customer.id, **_o)
        session.add(order)
        session.commit()
        session.refresh(order)
        for o in item_order:
            product = session.get(Product, o["product_id"])
            if product == None:
                Exception
            orderI = OrderItems(order_id= order.id, qty= o["qty"], product_id= o["product_id"], price= product.unit_price*o["qty"]+ product.unit_price*o["qty"]*product.tax/100 )
            order.total += orderI.price
            session.add(orderI)
            print("-----------entre-----------")
            
        session.commit()
        session.refresh(order)
        # order_items = session.scalars(
        #     select(Order)
        #     .options(joinedload(Order.order_items))
        #     .filter_by(id =order.id)
        # ).first()
        return order     

    
     