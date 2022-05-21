from pydantic import BaseModel

# Shared properties
from app.schemas.state import State


class PredictBase(BaseModel):
    customer_id: str = None


# Properties to receive on Episode creation
class PredictCreate(PredictBase):
    timestamp: str = None
    states: State = None
    offers: dict = None
    pass


# Properties to receive on Episode update
class PredictUpdate(PredictBase):
    pass


# Properties shared by models stored in DB
class PredictInDBBase(PredictBase):
    response_date: str = None
    best_offers: dict = None

    class Config:
        orm_mode = False


# Properties to return to client
class Predict(PredictInDBBase):
    pass


# Properties properties stored in DB
class PredictInDB(PredictInDBBase):
    pass
