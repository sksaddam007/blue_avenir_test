from fastapi import APIRouter

from app.api.api_v1.endpoints import agents, episodes, rewards
from app.api.api_v1.endpoints import items, login, utils, predict, products, users, github

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(episodes.router, prefix="/episodes", tags=["episodes"])
api_router.include_router(predict.router, prefix="/predict", tags=["predict"])
api_router.include_router(rewards.router, prefix="/rewards", tags=["rewards"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(github.router, prefix="/github", tags=["github"])

