
from sqlalchemy import select
from src.database import SessionLocal
from src.models.user_model import Product, ProductInventory
from src.schemas.product_schemas import Inventory, InventoryCreate, InventoryUpdate, ProductCreate, ProductUpdate

def add(inventory_create: InventoryCreate) -> ProductInventory:

    with SessionLocal() as session:

        product_inventory = ProductInventory(**inventory_create.dict())
        
        session.add(product_inventory)
        session.commit()
        session.refresh(product_inventory)
        session.close()
        return product_inventory
    
def get_inventory(product_id: int)-> ProductInventory:
    with SessionLocal() as session:
        customer = session.scalars(select(ProductInventory).filter_by(id = product_id).limit(1)).first()
    if not customer:
        raise Exception
    return customer

def update(inventory_update: InventoryUpdate)-> ProductInventory:
    with SessionLocal() as session:
        inventory_query = session.query(ProductInventory).filter(ProductInventory.id == inventory_update.id)
       
        if not inventory_query.first():
            raise Exception
        inventory_query.update(inventory_update.dict(), synchronize_session=False)
        session.commit()
    return inventory_query.first()

