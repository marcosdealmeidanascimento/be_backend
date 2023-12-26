from typing import Any, Dict, Optional, Union, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.base import CRUDBase
from app.db.models.post import Post
from app.db.schemas.post import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):

    async def get_by_user_id(self, db: AsyncSession, *, user_id: str) -> List[Post]:
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalars().all()
    
    async def get_by_user_id_and_id(self, db: AsyncSession, *, user_id: str, id: str) -> Optional[Post]:
        stmt = select(self.model).where(self.model.user_id == user_id).where(self.model.id == id)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: PostCreate, user_id) -> Post:
        db_obj = Post(
            title=obj_in.content[:20],
            content=obj_in.content,
            user_id=user_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: Post,
                     obj_in: Union[PostUpdate, Dict[str, Any]]) -> Post:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)
    

    async def randomPost(self, db: AsyncSession) -> Post:
        stmt = select(self.model).order_by(func.random()).limit(1)
        result = await db.execute(stmt)
        return result.scalars().first()
    

post = CRUDPost(Post)