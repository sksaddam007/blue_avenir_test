import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class EpisodeBase(BaseModel):
    customer_id: str = None
    states: str = None
    predicted_offer_1: str = None
    predicted_offer_2: str = None
    predicted_offer_3: str = None
    last_update: str = None


# Properties to receive on Episode creation
class EpisodeCreate(EpisodeBase):
    pass


# Properties to receive on Episode update
class EpisodeUpdate(EpisodeBase):
    pass


# Properties shared by models stored in DB
class EpisodeInDBBase(EpisodeBase):
    id: int
    customer_id: str = None
    states: str = None
    predicted_offer_1: str = None
    predicted_offer_2: str = None
    predicted_offer_3: str = None
    last_update: str = None

    class Config:
        orm_mode = True


# Properties to return to client
class Episode(EpisodeInDBBase):
    pass


# Properties properties stored in DB
class EpisodeInDB(EpisodeInDBBase):
    pass
