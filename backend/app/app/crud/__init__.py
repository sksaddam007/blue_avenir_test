from .crud_item import item
from .crud_user import user
from .crud_agent import agent
from .crud_episode import episode
from .crud_reward import reward
from .crud_product import product

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
