from typing import Any, List
from fastapi_health import health

from fastapi import APIRouter, Depends, HTTPException

from app.api import deps

router = APIRouter()


def get_session():
    return True


def is_database_online(session: bool = Depends(get_session)):
    return session



@router.get("/")
def health_check(
) -> Any:
    """
    Create new prediction.
    """
    return { "status":"UP"}


@router.get("/hello_world")
def hello_world_check(
) -> Any:
    """
    Create new prediction.
    """
    return { "status":"UP=checking"}