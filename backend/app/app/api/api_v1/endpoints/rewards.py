from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Reward])
def read_rewards(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
   
) -> Any:
    """
    Retrieve rewards.
    """
    rewards = crud.reward.get_multi(db, skip=skip, limit=limit)
    return rewards


@router.post("/", response_model=schemas.Reward)
def create_reward(
    *,
    db: Session = Depends(deps.get_db),
    reward_in: schemas.RewardCreate,
   
) -> Any:
    """
    Create new reward.
    """
    reward = crud.reward.create(db=db, obj_in=reward_in)
    return reward


@router.put("/{id}", response_model=schemas.Reward)
def update_reward(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    reward_in: schemas.RewardUpdate,
   
) -> Any:
    """
    Update an reward.
    """
    reward = crud.reward.get(db=db, id=id)
    if not reward:
        raise HTTPException(status_code=404, detail="reward not found")
    
    reward = crud.reward.update(db=db, db_obj=reward, obj_in=reward_in)
    return reward


@router.get("/{id}", response_model=schemas.Reward)
def read_reward(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
   
) -> Any:
    """
    Get reward by ID.
    """
    reward = crud.reward.get(db=db, id=id)
    if not reward:
        raise HTTPException(status_code=404, detail="reward not found")
    
    return reward


@router.delete("/{id}", response_model=schemas.Reward)
def delete_reward(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
   
) -> Any:
    """
    Delete an reward.
    """
    reward = crud.reward.get(db=db, id=id)
    if not reward:
        raise HTTPException(status_code=404, detail="reward not found")
    
    reward = crud.reward.remove(db=db, id=id)
    return reward
