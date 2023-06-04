import datetime
import decimal
from typing import List
from sqlalchemy import ARRAY, TIMESTAMP, Column, ForeignKey, String, Boolean, Integer, Text, DECIMAL, func
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


class Base(DeclarativeBase):
     pass

class User(Base):

     __tablename__ = "users"
     id = Column(Integer, nullable=False, primary_key=True)
     email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
     password: Mapped[str] = mapped_column(String(255), nullable=False)
     is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

     customer: Mapped["Customer"] = relationship(back_populates="user")
     permissions: Mapped["Permissions"] = relationship(back_populates="user")
     

class Permissions(Base):
     __tablename__ = "permissions"
     id = Column(Integer, nullable=False, primary_key=True)
     permissions: Mapped[str] = mapped_column(ARRAY(String), nullable=True) 
     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
     user: Mapped["User"] = relationship(back_populates="permissions")

class Customer(Base):

     __tablename__ = "customers"

     id: Mapped[int] =  mapped_column(nullable=False, primary_key=True)
     firstname: Mapped[str] = mapped_column(String(50), nullable=False)
     lastname: Mapped[str] = mapped_column(String(50), nullable=False)
     created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
     contact_info: Mapped["User_contact_info"] = relationship(back_populates="customer")
     payment: Mapped[List["User_payment"]] = relationship(back_populates="customer")

     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
     user: Mapped["User"] = relationship(back_populates="customer")

     order: Mapped[List["Order"]] = relationship(back_populates="customer")


class User_contact_info(Base):

     __tablename__ = "contact_info"
     id: Mapped[int] =  mapped_column(nullable=False, primary_key=True)
     address_line1: Mapped[str] = mapped_column(String(100), nullable=False)
     address_line2: Mapped[str] = mapped_column(String(100))
     city: Mapped[str] = mapped_column(String(50), nullable=False)
     postal_code: Mapped[str] = mapped_column(String(7), nullable=False)
     telephone: Mapped[str] = mapped_column(String(12), nullable=False)

     customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
     customer: Mapped["Customer"] = relationship(back_populates="contact_info")

     customer = relationship("Customer")
class User_payment(Base):
    
     __tablename__ = "user_payment"
     id: Mapped[int] =  mapped_column(nullable=False, primary_key=True)
     payment_type: Mapped[str] = mapped_column(String(10), nullable=False)
     provider: Mapped[str] = mapped_column(String(20), nullable=False)
     account_no: Mapped[str] = mapped_column(String(16), nullable=False)
     cvv: Mapped[str] = mapped_column(String(3), nullable=False)
     expiry: Mapped[str] = mapped_column(String(10), nullable=False)
     customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
     customer: Mapped["Customer"] = relationship(back_populates="payment")

class Product(Base):
     __tablename__ = "products"

     id: Mapped[int] =  mapped_column(nullable=False, primary_key=True)
     name: Mapped[str] = mapped_column(String(100), nullable=False)
     description: Mapped[str] = mapped_column(Text, nullable=False) 
     SKU: Mapped[str] = mapped_column(String(100), nullable=False)
     unit_price: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)
     tax: Mapped[int] =  mapped_column(Integer, nullable=False)
     discontinued: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

     supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False)
     supplier: Mapped["Suppliers"] = relationship(lazy="joined", innerjoin=True, back_populates="product")

     category_id: Mapped[int] = mapped_column(ForeignKey("product_category.id", ondelete="CASCADE"), nullable=False)
     category: Mapped["ProductCategory"] = relationship(lazy="joined", innerjoin=True, back_populates="product")

     # discount_id: Mapped[int] = mapped_column(ForeignKey("product_discount.id", ondelete="CASCADE"), nullable=False)
     # discount: Mapped["ProductDiscount"] = relationship(back_populates="product")

     order_items: Mapped["OrderItems"] = relationship(back_populates="product")
     inventory: Mapped["ProductInventory"] = relationship(back_populates="product")


class ProductInventory(Base):
     __tablename__ = "product_inventory"
     id: Mapped[int] =  mapped_column(nullable=False, primary_key=True)
     units_in_stock: Mapped[int] =  mapped_column(Integer, nullable=False)
     qty_per_unit: Mapped[int] =  mapped_column(Integer, nullable=False)

     product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), unique=True, nullable=False)
     product: Mapped["Product"] = relationship(back_populates="inventory")


class Suppliers(Base):
     __tablename__ = "suppliers"
     id: Mapped[int] =  mapped_column(nullable=False, primary_key=True)
     name: Mapped[str] = mapped_column(String(100), nullable=False)
     address: Mapped[str] = mapped_column(String(100), nullable=False)
     supplier_id: Mapped[str] = mapped_column(String(30), nullable=False)
     city: Mapped[str] = mapped_column(String(100), nullable=False)
     postal_code: Mapped[str] = mapped_column(String(7), nullable=False)
     telephone: Mapped[str] = mapped_column(String(12), nullable=False)
     country: Mapped[str] = mapped_column(String(20), nullable=False)
     web_page: Mapped[str] = mapped_column(String(40), nullable=False)
     email: Mapped[str] = mapped_column(String(255), nullable=False)

     product: Mapped[List["Product"]] = relationship(back_populates="supplier")


class ProductCategory(Base):
     __tablename__ = "product_category"
     id: Mapped[int] =  mapped_column(nullable=False, primary_key=True)
     name: Mapped[str] = mapped_column(String(100), nullable=False)
     description: Mapped[str] = mapped_column(Text, nullable=False) 
     images: Mapped[str] = mapped_column(ARRAY(String), nullable=True) 

     product: Mapped[List["Product"]] = relationship(back_populates="category")


# class ProductDiscount(Base):
#      __tablename__ = "product_discount"
#      id: Mapped[int] =  mapped_column(nullable=False, primary_key=True)
#      active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
#      percent: Mapped[int] =  mapped_column(DECIMAL(2,0), nullable=False)

#      product: Mapped[List["Product"]] = relationship(back_populates="discount")


class Order(Base):
     __tablename__ = "orders"
     id: Mapped[int] =  mapped_column(nullable=False, primary_key=True)
     total: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)
     status: Mapped[str] = mapped_column(String(20), nullable=False)
     order_items: Mapped[List["OrderItems"]] = relationship(back_populates="order")
     
     customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
     customer: Mapped["Customer"] = relationship(back_populates="order")

class OrderItems(Base):
     __tablename__ = "order_items"
     id: Mapped[int] =  mapped_column(nullable=False, primary_key=True)
     qty: Mapped[int] =  mapped_column(Integer, nullable=False)
     price: Mapped[float] = mapped_column(DECIMAL(12, 2), nullable=False)

     product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
     product: Mapped["Product"] = relationship(lazy="joined", innerjoin=True, back_populates="order_items")

     order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
     order: Mapped["Order"] = relationship(back_populates="order_items")