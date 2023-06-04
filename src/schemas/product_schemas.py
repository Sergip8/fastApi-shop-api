
from typing import List, Optional, Sequence
from pydantic import BaseModel, EmailStr, HttpUrl



class Supplier(BaseModel):
    name: str
    address: str
    city: str
    postal_code: str
    supplier_id: str
    telephone: str
    country: str
    web_page: str
    email: EmailStr
    class Config:
        orm_mode = True

class SupplierCreate(Supplier):
    pass

class SupplierUpdate(Supplier):
    id: int

class Category(BaseModel):
    name: str
    description: str
    images: List[str]
    class Config:
        orm_mode = True

class CategoryCreate(Category):
    pass

class CategoryUpdate(Category):
    id: int
    pass

class ProductResponse(BaseModel):
    name: str
    description: str
    SKU: str
    unit_price: float
    tax: int
   
    class Config:
        orm_mode = True

class ProductCreate(ProductResponse):
    discontinued: bool
    supplier_id: int
    category_id: int


class ProductUpdate(ProductCreate):
    id: int
    pass

class ProductResponseWithSupplierAndCategory(ProductResponse):
    supplier: Supplier
    category: Category
    class Config:
        orm_mode = True

class Inventory(BaseModel):
     
    units_in_stock: int
    qty_per_unit: int
    product_id: int
    class Config:
        orm_mode = True

class InventoryCreate(Inventory):
    pass

class InventoryUpdate(Inventory):
    id: int
    

