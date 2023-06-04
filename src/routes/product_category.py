from typing import Annotated, List, Sequence
from fastapi import APIRouter, Depends, Response, Security, status
from src.models.user_model import ProductCategory
from src.schemas.customer_schemas import CustomerContactCreate, CustomerContactInfo, CustomerCreate, CustomerResponse
from src.schemas.product_schemas import Category, CategoryCreate, CategoryUpdate
from src.schemas.user_schemas import TokenData, UserCreate, UserResponse
import src.services.product_category_service as service
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.oauth2 import get_current_user
from sqlalchemy.orm import Session
from src.database import get_db

router = APIRouter()

router = APIRouter(prefix="/product_category", 
                   responses={404: {"message": "No hay de eso"}},
                   tags=["product_category"])



@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Category])

def search_by_name(name: str, session: Session = Depends(get_db)):
  
    try:
        category_query = session.query(ProductCategory).filter(ProductCategory.name.startswith(name))
        return category_query.all()
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontraroo categorias")

@router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model=Category)

def get_by_id(category_id: int, 
              user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_read"])],
              session: Session = Depends(get_db)):
  
    try:
        category = session.get(ProductCategory, category_id)
        return category
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontro la categoria")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= Category)

def category_create(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["advance_write"])],
    category_create: CategoryCreate, 
    session: Session = Depends(get_db)):

    try:
        product_category = ProductCategory(**category_create.dict())
        session.add(product_category)
        session.commit()
        session.refresh(product_category)
        
        return product_category
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo registrar")
    
@router.put("/", status_code=status.HTTP_200_OK, response_model= Category)

def product_update(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["advance_write"])],
    category_update: CategoryUpdate, 
    session: Session = Depends(get_db)):

    try:
        inventory_query = session.query(ProductCategory).filter(ProductCategory.id == category_update.id)
        inventory_query.update(category_update.dict(), synchronize_session=False)
        session.commit()
        return inventory_query.first()
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo registrar")
 