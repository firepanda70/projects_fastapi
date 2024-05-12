import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import AsyncTransaction, get_async_session
from .dependencies import valid_credentials, valid_username, valid_token
from .service import UserService
from .models import User
from .schemas import UserDB, UserCreate, TokenResponse

logger = logging.getLogger(__name__)
user_router = APIRouter()


@user_router.post('/register')
async def register(
    user_data: UserCreate = Depends(valid_username),
    user_service: UserService = Depends(UserService),
    transaction: AsyncTransaction = Depends(AsyncTransaction),
    session: AsyncSession = Depends(get_async_session)
) -> UserDB:
    async with transaction as id:
        user = await user_service.create(user_data)
        logger.info(f'created user, id: {user.id}; transanction: {id}')
    await session.refresh(user)
    return user

@user_router.post('/login')
async def login(
    user: User = Depends(valid_credentials),
    user_service: UserService = Depends(UserService)
) -> TokenResponse:
    return TokenResponse(token=(await user_service.gen_token(user)))

@user_router.get('/me')
async def me(
    user_id: int = Depends(valid_token),
    user_service: UserService = Depends(UserService)
) -> UserDB:
    return await user_service.get(user_id)
