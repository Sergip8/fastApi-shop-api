from typing import Annotated, List, Sequence
from fastapi import APIRouter, Depends, Response, Security, status
from sqlalchemy import select
from src.models.user_model import Product
from src.schemas.customer_schemas import CustomerContactCreate, CustomerContactInfo, CustomerCreate, CustomerPayment, CustomerPaymentCreate, CustomerResponse
from src.schemas.product_schemas import ProductCreate, ProductResponse, ProductResponseWithSupplierAndCategory, ProductUpdate, Supplier, SupplierCreate
from src.schemas.user_schemas import TokenData, UserCreate, UserResponse
import src.services.product_service as service
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.oauth2 import get_current_user
from sqlalchemy.orm import Session
from src.database import get_db

router = APIRouter()

router = APIRouter(prefix="/product", 
                   responses={404: {"message": "No hay de eso"}},
                   tags=["product"])


@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponseWithSupplierAndCategory)

def get_by_id(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["advance_read"])],
    product_id: int, 
    session: Session = Depends(get_db)):
    try:
        product = session.scalars(select(Product).filter_by(id = product_id)).first()
        return product
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontro el producto")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= ProductResponse)

def product_create(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["advance_write"])],
    product_create: ProductCreate, 
    session: Session = Depends(get_db),
    ):

  
        product_category = Product(**product_create.dict())
        session.add(product_category)
        session.commit()
        session.refresh(product_category)
        return product_category
    
       


@router.put("/", status_code=status.HTTP_200_OK, response_model= ProductResponse)

def product_update(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["advance_write"])],
    product_update: ProductUpdate, 
    session: Session = Depends(get_db)):

    try:
        product_query = session.query(Product).filter(Product.id == product_update.id)
        product_query.update(product_update.dict(), synchronize_session=False)
        session.commit()
        return product_query.first()
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo registrar")

@router.get("/", status_code=status.HTTP_200_OK, response_model= List[ProductResponse])

def search_product(name: str, limit: int = 2, session: Session = Depends(get_db)):

    try:
        product_query = session.query(Product).filter(Product.name.startswith(name)).limit(limit)
        return product_query.all()
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo registrar")