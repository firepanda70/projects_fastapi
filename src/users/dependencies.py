from fastapi import Depends, Header

from .exceptions import InvalidCredentials, UsernameTaken, NotAuthorized
from .service import UserService
from .schemas import UserLogin, UserCreate
from .models import User
from .utils import verify_password


async def valid_credentials(
    data: UserLogin,
    service: UserService = Depends(UserService)
) -> User:
    user = await service.get_by_username(data.username)
    if not user or not verify_password(data.password, user.hashed_password):
        raise InvalidCredentials
    return user

async def valid_username(
    data: UserCreate,
    service: UserService = Depends(UserService)
) -> UserCreate:
    user = await service.get_by_username(data.username)
    if user:
        raise UsernameTaken
    return data

async def valid_token(
    token: str = Header(),
    service: UserService = Depends(UserService)
) -> int:
    id = await service.get_id_by_token(token)
    if id is None:
        raise NotAuthorized
    return id
