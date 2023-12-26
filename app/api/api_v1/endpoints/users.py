from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime, timedelta

from app.db import repositories, models, schemas
from app.api import deps
from app.core.config import settings

from app.utils import (
    generate_password_reset_token,
    verify_password_reset_token,
    send_confirmation,
)

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    _: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = await repositories.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    _: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = await repositories.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await repositories.user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=schemas.User)
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    password: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if email is not None:
        user_in.email = email
    user = await repositories.user.update(db, db_obj=current_user,
                                          obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
async def read_user_me(
    _: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """

    current_user = await repositories.user.can_post(_, user=current_user)

    return current_user


@router.post("/open", response_model=schemas.User)
async def create_user_open(
    *,
    db: AsyncSession = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
) -> Any:
    
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = await repositories.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this username already exists in the system",
        )
    gprt = generate_password_reset_token(email=email)
    send_confirmation(email, gprt)

    user_in = schemas.UserCreate(password=password, email=email)
    user = await repositories.user.create(db, obj_in=user_in)

    return user


@router.post("/resend-confirmation", response_model=schemas.User)
async def resend_confirmation(
    db: AsyncSession = Depends(deps.get_db),
    email: Any = Body(...),
) -> Any:
    
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = await repositories.user.get_by_email(db, email=email['email'])
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username was not found in the system",
        )
    print(jsonable_encoder(user))
    gprt = generate_password_reset_token(email=email['email'])
    send_confirmation(email['email'], gprt)

    return user


@router.post("/confirm", response_model=schemas.User)
async def confirm_account(
    token: Any = Body(...),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Confirm email
    """
    email = verify_password_reset_token(token['token'])
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await repositories.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )

    sql = f'UPDATE "user" SET is_active = true WHERE "id" = \'{user.id}\''

    await db.execute(sql)
    await db.commit()
    await db.refresh(user)

    return user


@router.get("/{user_id}", response_model=schemas.User)
async def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = await repositories.user.get(db, id=user_id)
    if user == current_user:
        return user
    return user


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    _: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = await repositories.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = await repositories.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.post("/permission", response_model=schemas.User)
async def permission(
    *,
    db: AsyncSession = Depends(deps.get_db),
    name: str = Body(...),
    description: EmailStr = Body(...),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )

    user_in = schemas.PermissionSchema(name='password', description='email')
    user = await repositories.permission.create(db, obj_in=user_in)
    return user


@router.post("/open/email")
async def read_user_email(
    db: AsyncSession = Depends(deps.get_db),
    email: dict = Body(""),
) -> Any:
    user_in = await repositories.user.get_by_email(db, email=email["email"])
    user = jsonable_encoder(user_in)
    if user == None:
        return 0
    return 1
