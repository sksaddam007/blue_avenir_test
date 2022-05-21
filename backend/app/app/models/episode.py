import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Episode(Base):
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, nullable=False, index=True)
    states = Column(String, nullable=False, index=True)
    predicted_offer_1 = Column(String, nullable=False, index=True)
    predicted_offer_2 = Column(String, index=True)
    predicted_offer_3 = Column(String, index=True)
    last_update = Column(DateTime, onupdate=datetime.datetime.now(), index=True)
    up_to_date = Column(DateTime, onupdate=datetime.datetime.now(), index=True)
