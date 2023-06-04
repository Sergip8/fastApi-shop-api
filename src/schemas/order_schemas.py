

from typing import List
from pydantic import BaseModel

from src.schemas.product_schemas import ProductResponse

class ItemOrder(BaseModel):
    
    qty: int
    product_id: int


class Order(BaseModel):
    
    total: float = 0
    status: str
    class Config:
        orm_mode = True

class CreateOrder(Order):
    items_order: List[ItemOrder]
    class Config:
        orm_mode = True
    pass

class ItemsOrderResponse(BaseModel):
    price: float
    qty: int
    product: ProductResponse
    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    total: float 
    status: str
    order_items: List[ItemsOrderResponse]
    
    class Config:
        orm_mode = True



