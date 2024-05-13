import logging
import string
import random
import calendar
from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from .config import config

logger = logging.getLogger(__name__)

engine = create_async_engine(str(config.db_url))
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


class AsyncTransaction:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session
        self.id = (
            '-'.join((
                str(calendar.timegm(datetime.now().utctimetuple())),
                ''.join(random.choices(string.ascii_uppercase, k=3)),
            ))
        )

    async def __aenter__(self):
        logger.info(f'Transanction {self.id} iniciated')
        return self.id

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            await self.session.rollback()
            logger.error(f'Transanction {self.id} rollback')
            return False
        await self.session.commit()
        logger.info(f'Transanction {self.id} commit')
        return True
