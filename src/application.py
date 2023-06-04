from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import product_supplier, user, customer, customer_contact_info, customer_payment, product_category, product, order, product_inventory
from src.models import user_model
from src.database import engine

origins = [
    "http://localhost:4200"
]
user_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
   
app.include_router(user.router)
app.include_router(customer.router)
app.include_router(customer_contact_info.router)
app.include_router(customer_payment.router)
app.include_router(product_supplier.router)
app.include_router(product_category.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(product_inventory.router)