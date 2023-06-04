from typing import Annotated, List, Sequence
from fastapi import APIRouter, Depends, Response, Security, status
from sqlalchemy import select
from src.models.user_model import Customer
from src.schemas.customer_schemas import (
    CustomerCreate,
    CustomerOrderResponse,
    CustomerResponse,
    CustomerUpdate,
)
from src.schemas.user_schemas import TokenData, UserCreate, UserResponse
import src.services.customer_service as service
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.oauth2 import get_current_user
from sqlalchemy.orm import Session, joinedload
from src.database import get_db

router = APIRouter()

router = APIRouter(
    prefix="/customers",
    responses={404: {"message": "No hay de eso"}},
    tags=["customers"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=CustomerResponse)
def get_by_id(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_read"])],
    session: Session = Depends(get_db),
    
):
    try:
        customer = session.scalars(
            select(Customer)
            .options(joinedload(Customer.user))
            .filter_by(user_id=user_data.user_id)
            .limit(1)
        ).first()
        return customer
    except:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND, content="no se encontro al usuario"
        )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CustomerResponse)
def customer_create(
    customer_create: CustomerCreate,
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_write"])],
    session: Session = Depends(get_db),
):
    try:
        customer = Customer(user_id=user_data.user_id, **customer_create.dict())
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer
    except Exception:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="no se pudo registrar los datos",
        )


@router.put("/", status_code=status.HTTP_200_OK, response_model=CustomerResponse)
def customer_update(
    customer_update: CustomerUpdate,
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_write"])],
    session: Session = Depends(get_db),
):
    try:
        customer = session.query(Customer).filter(Customer.id == customer_update.id)
        if not customer.first():
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="no existe el registro del cliente",
            )

        if customer.first().user_id != user_data.user_id:
            return Response(
                status_code=status.HTTP_403_FORBIDDEN,
                content="el registro no es del usuario",
            )

        customer.update(customer_update.dict(), synchronize_session=False)
        session.commit()
        return customer.first()
    except Exception:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST, content="no se pudo registrar"
        )


@router.get(
    "/order", status_code=status.HTTP_200_OK, response_model=CustomerOrderResponse
)
def get_orders(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_write"])],
    session: Session = Depends(get_db),
    sta: str = "",
):
    try:
        customer = session.scalars(
            select(Customer)
            .options(joinedload(Customer.order))
            .filter_by(user_id=user_data.user_id)
            .limit(1)
        ).first()
        if sta != "":
            order = []
            for o in customer.order:
                if o.status == sta:
                    order.append(o)
            customer.order = order
    except Exception:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST, content="no tiene ordenes"
        )
    return customer


@router.get(
    "/order/status",
    status_code=status.HTTP_200_OK,
    response_model=CustomerOrderResponse,
)
def get_orders_by_status(
    user_data: Annotated[TokenData, Security(get_current_user, scopes=["basic_write"])],
    sta: str = "",
    session: Session = Depends(get_db),
):
    try:
        return service.get_orders_by_status(user_data.user_id, sta)
    except Exception:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST, content=f"no tiene ordenes {sta}"
        )


# @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)

# def remove(user_id: int,):
#     try:
#         service.delete_user_by_id(user_id)
#     except Exception:
#         return Response(status_code=status.HTTP_404_NOT_FOUND, content="no se encontro al usuario")
