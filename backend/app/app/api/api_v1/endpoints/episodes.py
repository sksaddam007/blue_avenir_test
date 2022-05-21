from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Episode])
def read_episodes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
   
) -> Any:
    """
    Retrieve episodes.
    """
    episodes = crud.episode.get_multi(db, skip=skip, limit=limit)
    return episodes


@router.post("/", response_model=schemas.Episode)
def create_episode(
    *,
    db: Session = Depends(deps.get_db),
    episode_in: schemas.EpisodeCreate,
   
) -> Any:
    """
    Create new episode.
    """
    episode = crud.episode.create(db=db, obj_in=episode_in)
    return episode


@router.put("/{id}", response_model=schemas.Episode)
def update_episode(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    episode_in: schemas.EpisodeUpdate,
   
) -> Any:
    """
    Update an episode.
    """
    episode = crud.episode.get(db=db, id=id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    episode = crud.episode.update(db=db, db_obj=episode, obj_in=episode_in)
    return episode


@router.get("/{id}", response_model=schemas.Episode)
def read_episode(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
   
) -> Any:
    """
    Get episode by ID.
    """
    episode = crud.episode.get(db=db, id=id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    return episode


@router.delete("/{id}", response_model=schemas.Episode)
def delete_episode(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
   
) -> Any:
    """
    Delete an episode.
    """
    episode = crud.episode.get(db=db, id=id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    episode = crud.episode.remove(db=db, id=id)
    return episode
