from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from starlette.responses import Response, JSONResponse

router = APIRouter()


@router.get("/", response_model=List[schemas.Agent])
def read_agents(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve agents.
    """
    agents = crud.agent.get_multi(db, skip=skip, limit=limit)
    return agents


@router.post("/", response_model=schemas.Agent)
def create_agent(
        *,
        db: Session = Depends(deps.get_db),
        agent_in: schemas.AgentCreate,

) -> Any:
    """
    Create new agent.
    """
    agent = crud.agent.create(db=db, obj_in=agent_in)
    return agent


@router.put("/{id}", response_model=schemas.Agent)
def update_agent(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        agent_in: schemas.AgentUpdate,

) -> Any:
    """
    Update an agent.
    """
    agent = crud.agent.get(db=db, id=id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = crud.agent.update(db=db, db_obj=agent, obj_in=agent_in)
    return agent


@router.get("/{id}", response_model=schemas.Agent)
def read_agent(
        *,
        db: Session = Depends(deps.get_db),
        id: int,

) -> Any:
    """
    Get agent by ID.
    """
    agent = crud.agent.get(db=db, id=id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent


@router.get("/is-alive/")
async def read_agent_alive(
        *,
        db: Session = Depends(deps.get_db),
        version: Union[List[str], None] = Query(default=None)
) -> Any:
    """
    Get agent by q.
    """
    response = {"status": "I’m alive and running", "agent-version": "1.0.0-API"}
    if version:
        agent = crud.agent.get_by_key(db=db, column_name='version', value=version.pop())
        if agent:
            response = {"status": "I’m alive and running", "agent-version": f"{agent.version}-API"}
    return JSONResponse(content=response)


@router.delete("/{id}", response_model=schemas.Agent)
def delete_agent(
        *,
        db: Session = Depends(deps.get_db),
        id: int,

) -> Any:
    """
    Delete an agent.
    """
    agent = crud.agent.get(db=db, id=id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = crud.agent.remove(db=db, id=id)
    return agent
