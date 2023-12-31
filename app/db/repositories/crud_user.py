import time
from typing import Any, Dict, Optional, Union
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash, verify_password
from app.db.repositories.base import CRUDBase
from app.db.models.user import User
from app.db.schemas.user import UserCreate, UserUpdate, UserCreateNot


class CRUDUser(CRUDBase[User, UserCreateNot, UserUpdate]):

    async def get_by_email(self, db: AsyncSession, *,
                           email: str) -> Optional[User]:
        stmt = select(self.model).where(self.model.email == email)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_active=False
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: User,
                     obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *,
                           email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active


    async def can_post(self, db: AsyncSession, *, user: User) -> bool:
        if not user.last_post:
            return user

        if user.last_post + timedelta(hours=10) < datetime.utcnow():
            db_obj = user
            db_obj.can_post = True
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        
        return user
            

user = CRUDUser(User)
