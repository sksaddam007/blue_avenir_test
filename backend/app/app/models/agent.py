import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Agent(Base):
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, nullable=False, index=True)
    last_update = Column(DateTime, onupdate=datetime.datetime.now(), index=True)
