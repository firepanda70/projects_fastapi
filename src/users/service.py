import secrets

from sqlalchemy import select

from src.core.redis import redis_client, RedisData
from src.core.service import BaseService
from .models import User
from .schemas import UserCreate
from .utils import hash_password


class UserService(BaseService[User]):
    model = User
    async def gen_token(self, user: User) -> str:
        while True:
            token = secrets.token_urlsafe()
            if not await redis_client.get(token):
                await redis_client.set_data(
                    RedisData(key=f'token:{token}', value=str(user.id))
                )
                return token

    async def get_id_by_token(self, token: str) -> int | None:
        res = await redis_client.get(f'token:{token}')
        return res if res is None else int(res)

    async def get_by_username(self, username: str) -> User | None:
        expr = select(User).where(User.username == username)
        return (await self.session.execute(expr)).scalar_one_or_none()

    async def create(self, obj_in: UserCreate) -> User:
        user = User(
            username=obj_in.username,
            hashed_password=hash_password(obj_in.password)
        )
        self.session.add(user)
        await self.session.flush()
        return user
