import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class RewardBase(BaseModel):
    customer_id: str = None
    accepted_offer: bool = None


# Properties to receive on Reward creation
class RewardCreate(RewardBase):
    pass


# Properties to receive on Reward update
class RewardUpdate(RewardBase):
    pass


# Properties shared by models stored in DB
class RewardInDBBase(RewardBase):
    id: int
    customer_id: str = None
    accepted_offer: bool = None
    last_update: datetime.datetime = None

    class Config:
        orm_mode = True


# Properties to return to client
class Reward(RewardInDBBase):
    pass


# Properties properties stored in DB
class RewardInDB(RewardInDBBase):
    pass
