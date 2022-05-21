from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(String, index=True)
    product_name = Column(String, index=True)
