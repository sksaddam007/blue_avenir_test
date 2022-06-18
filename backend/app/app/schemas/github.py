from typing import Optional, List

from pydantic import BaseModel


# Shared properties
class RepoBase(BaseModel):
    users: List = None
    organizations: List = None
    echoUrls: bool = False
    useThread: bool = False
    useProcess: bool = False


# Properties to receive on item creation
class RepoCreate(RepoBase):
    pass

# Properties to receive on Repo update
class RepoUpdate(RepoBase):
    pass


# Properties shared by models stored in DB
class RepoInDBBase(BaseModel):
    urlList: List[str] = []
    model: str = None

    class Config:
        orm_mode = True


# Properties to return to client
class Repo(RepoInDBBase):
    pass


# Properties properties stored in DB
class RepoInDB(RepoInDBBase):
    pass
