from typing import Any, Optional
from pydantic import BaseModel
from app.db.schemas.user import User


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User
    expires: Any


class TokenPayload(BaseModel):
    sub: Optional[str] = None
