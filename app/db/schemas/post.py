from optparse import Option
from typing import List, Optional # noqa: F401, E261
# from datetime import datetime
from pydantic import UUID4, BaseModel, EmailStr


# Shared properties
class PostBase(BaseModel):
    content: Optional[str] = None
    title: Optional[str] = None
    user_id: Optional[UUID4] = None


# Properties to receive via API on creation
class PostCreate(PostBase):
    content: str

# Properties to receive via API on update
class PostUpdate(PostBase):
    content: str


# Properties to return via API
class PostInDBBase(PostBase):
    id: UUID4

    class Config:
        orm_mode = True


# Additional properties to return via API
class Post(PostInDBBase):
    pass


# Additional properties stored in DB
class PostInDB(PostInDBBase):
    pass