from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app import models
from app.api import deps
from app.service.github_service import git_actions

router = APIRouter()


@router.post("/", response_model=schemas.RepoInDB)
def create_clone(
    repo_in: schemas.RepoCreate
    ) -> Any:
    """
    Create new item.
    """
    model, urls = git_actions(users=repo_in.users, organizations=repo_in.organizations, echo_urls=repo_in.echoUrls, use_threading=repo_in.useThread, use_process=repo_in.useProcess)
    response = schemas.RepoInDB(model=model, urlList=urls)
    return response

