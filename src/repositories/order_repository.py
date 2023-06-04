from typing import List
from sqlalchemy import select
from src.database import SessionLocal
from src.models.user_model import Customer, Order, OrderItems, Product, ProductInventory
from src.schemas.order_schemas import CreateOrder, ItemOrder
from src.schemas.product_schemas import Inventory, InventoryCreate, InventoryUpdate, ProductCreate, ProductUpdate

def add(create_order: CreateOrder, user_id):

    with SessionLocal() as session:
        customer = session.scalars(select(Customer).filter_by(id = user_id).limit(1)).first()
        if not customer:
            raise Exception
        _o = create_order.dict()
        item_order =  _o.pop("items_order")
        print(item_order)
        order = Order(customer_id=customer.id, **_o)
        session.add(order)

        for o in item_order:
            product = session.get(Product, o["product_id"])
            if not product:
                raise Exception
            orderI = OrderItems(order_id= order.id, qty= o["qty"], product_id= o["product_id"], price= product.unit_price*o["qty"]+ product.unit_price*o["qty"]*product.tax/100 )
            order.total += orderI.price
            session.add(orderI)
        
        session.commit()
        session.refresh(order)
        session.close()
        return order

# def get_inventory(product_id: int)-> ProductInventory:
#     with SessionLocal() as session:
#         customer = session.scalars(select(ProductInventory).filter_by(id = product_id).limit(1)).first()
#     if not customer:
#         raise Exception
   # return customer

# def update(inventory_update: InventoryUpdate)-> ProductInventory:
#     with SessionLocal() as session:
#         inventory_query = session.query(ProductInventory).filter(ProductInventory.id == inventory_update.id)

#         if not inventory_query.first():
#             raise Exception
#         inventory_query.update(inventory_update.dict(), synchronize_session=False)
#         session.commit()
#     return inventory_query.first()