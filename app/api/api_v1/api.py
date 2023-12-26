from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users # noqa: E501, E261
from app.api.api_v1.endpoints import post # noqa: E501, E261

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(post.router, prefix="/post", tags=["post"])