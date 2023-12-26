from typing import List, Optional # noqa: F401, E261
from datetime import datetime
from pydantic import UUID4, BaseModel, EmailStr
from typing import Optional


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = False
    last_post: Optional[datetime] = None


class UserCreateNot(UserBase):
    is_active : bool = False


# Properties to receive via API on creation
class UserCreate(UserCreateNot):
    email: EmailStr
    password: str


class UserConfirm(BaseModel):
    email: EmailStr
    password: Optional[str] = None


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: UUID4
    # created_at: datetime
    # updated_at: datetime
    class Config:
        orm_mode = True

class UserPassReset(BaseModel):
    reset_code: str

# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


class UserLogin(BaseModel):
    username: EmailStr
    password: str
