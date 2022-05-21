import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class AgentBase(BaseModel):
    version: str = None


# Properties to receive on item creation
class AgentCreate(AgentBase):
    pass


# Properties to receive on item update
class AgentUpdate(AgentBase):
    pass


# Properties shared by models stored in DB
class AgentInDBBase(AgentBase):
    id: int
    version: str

    class Config:
        orm_mode = True


# Properties to return to client
class Agent(AgentInDBBase):
    pass


# Properties properties stored in DB
class AgentInDB(AgentInDBBase):
    pass
