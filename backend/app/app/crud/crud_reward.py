from app.crud.base import CRUDBase
from app.models.reward import Reward
from app.schemas.reward import RewardCreate, RewardUpdate


class CRUDReward(CRUDBase[Reward, RewardCreate, RewardUpdate]):
    pass


reward = CRUDReward(Reward)
