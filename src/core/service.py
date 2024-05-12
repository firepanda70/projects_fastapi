from typing import TypeVar, Generic, Sequence, Type

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_async_session
from .models import BaseDBModel

DB_MODEL = TypeVar('DB_MODEL', bound=BaseDBModel)


class BaseService(Generic[DB_MODEL]):
    model: Type[DB_MODEL]
    def __init__(
        self, session: AsyncSession = Depends(get_async_session)
    ) -> None:
        self.session = session

    async def get(self, id: int) -> Type[DB_MODEL] | None:
        expr = select(self.model).where(self.model.id == id)
        return (await self.session.execute(expr)).scalar_one_or_none()

    async def get_many(self) -> Sequence[DB_MODEL]:
        return (await self.session.execute(select(self.model))).scalars().all()
    
    async def delete(self, obj: DB_MODEL):
        await self.session.delete(obj)
        await self.session.flush()
        return True
