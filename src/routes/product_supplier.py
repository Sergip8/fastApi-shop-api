from typing import Annotated, List, Sequence
from fastapi import APIRouter, Depends, Response, Security, status
from src.models.user_model import Suppliers
from src.oauth2 import get_current_user
from src.schemas.product_schemas import Supplier, SupplierCreate, SupplierUpdate
from src.schemas.user_schemas import TokenData
import src.services.product_supplier_service as service

from sqlalchemy.orm import Session
from src.database import get_db

router = APIRouter()

router = APIRouter(prefix="/supplier", 
                   responses={404: {"message": "No hay de eso"}},
                   tags=["supplier"])
 


@router.get("/{supplier_id}", status_code=status.HTTP_200_OK, response_model=Supplier)

def get_by_id(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["advance_read"])],
    supplier_id: int, 
    session: Session = Depends(get_db)):
    try:
        customer = session.get(Suppliers, supplier_id)
        return customer
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontro al usuario")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= Supplier)

def customer_supplier_create(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["advance_write"])],
    supplier_create: SupplierCreate, 
    session: Session = Depends(get_db)):

    try:
        supplier = Suppliers(**supplier_create.dict())
        session.add(supplier)
        session.commit()
        session.refresh(supplier)
        
        return supplier
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo registrar")


@router.put("/", status_code=status.HTTP_200_OK, response_model= Supplier)
def supplier_update(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["advance_write"])],
    supplier_update: SupplierUpdate, 
    session: Session = Depends(get_db)):

    try:
        inventory_query = session.query(Suppliers).filter(Suppliers.id == supplier_update.id)
        inventory_query.update(supplier_update.dict(), synchronize_session=False)
        session.commit()
        return inventory_query.first()
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo registrar")


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Supplier])

def search_by_name(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["advance_read"])],
    name: str, 
    session: Session = Depends(get_db)):
  
    try:
        product_query = session.query(Suppliers).filter(Suppliers.name.startswith(name))
        return product_query.all()
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontraroo categorias")