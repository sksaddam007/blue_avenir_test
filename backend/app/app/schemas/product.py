import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class ProductBase(BaseModel):
    offer_id: str = None
    product_name: str = None


# Properties to receive on Episode creation
class ProductCreate(ProductBase):
    pass


# Properties to receive on Episode update
class ProductUpdate(ProductBase):
    pass


# Properties shared by models stored in DB
class ProductInDBBase(ProductBase):
    offer_id: str = None
    product_name: str = None

    class Config:
        orm_mode = True


# Properties to return to client
class Product(ProductInDBBase):
    pass


# Properties properties stored in DB
class ProductInDB(ProductInDBBase):
    pass
