from typing import Annotated, List, Sequence
from fastapi import APIRouter, Depends, Response, Security, status
from sqlalchemy import select
from src.models.user_model import ProductInventory
from src.oauth2 import get_current_user
from src.schemas.product_schemas import Inventory, InventoryCreate, InventoryUpdate
from src.schemas.user_schemas import TokenData
import src.services.product_inventory_service as service


from sqlalchemy.orm import Session
from src.database import get_db

router = APIRouter(prefix="/product_inventory", 
                   responses={404: {"message": "No hay de eso"}},
                   tags=["product_inventory"])



@router.get("/{inventory_id}", status_code=status.HTTP_200_OK, response_model=Inventory)

def get_by_id(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["advance_read"])],
    inventory_id: int, 
    session: Session = Depends(get_db)):
    try:
        customer = session.scalars(select(ProductInventory).filter_by(id = inventory_id)).first()
        return customer
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontro inventario")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= Inventory)

def customer_payment_create(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["advance_write"])],
    inventory_create: InventoryCreate, 
    session: Session = Depends(get_db)):

    try:
        product_inventory = ProductInventory(**inventory_create.dict())
        session.add(product_inventory)
        session.commit()
        session.refresh(product_inventory)
        return product_inventory
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo registrar")
     

@router.put("/", status_code=status.HTTP_200_OK, response_model= Inventory)

def product_update(inventory_update: InventoryUpdate, session: Session = Depends(get_db)):

    try:
        inventory_query = session.query(ProductInventory).filter(ProductInventory.id == inventory_update.id)
        inventory_query.update(inventory_update.dict(), synchronize_session=False)
        session.commit()
        return inventory_query.first()

    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo registrar")
