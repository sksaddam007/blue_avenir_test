import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Reward(Base):
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, nullable=False, index=True)
    accepted_offer = Column(Boolean, index=True)
    last_update = Column(DateTime, onupdate=datetime.datetime.now(), index=True)
    up_to_date = Column(DateTime, onupdate=datetime.datetime.now(), index=True)
