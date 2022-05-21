import datetime
import enum
from typing import Optional

from pydantic import BaseModel


class Region(enum.Enum):
    Europa = 'Europa'
    Americas = 'Americas'
    Asia = 'Asia'


class Gender(enum.Enum):
    F = 'F'
    M = 'M'


# Shared properties
class StateBase(BaseModel):
    age: int = None
    gender: str = None
    client_since: str = None
    region: str = None
    last_offer: str = None


# Properties to receive on Episode creation
class StateCreate(StateBase):
    pass


# Properties to receive on Episode update
class StateUpdate(StateBase):
    pass


# Properties shared by models stored in DB
class StateInDBBase(StateBase):
    age: int = None
    gender: Gender = None
    client_since: str = None
    region: Region = None
    last_offer: str = None

    class Config:
        orm_mode = True


# Properties to return to client
class State(StateInDBBase):
    pass


# Properties properties stored in DB
class StateInDB(StateInDBBase):
    pass
