from pydantic import Field

from src.core.schemas import CustomSchema, CustomSchemaDB


class UserCreate(CustomSchema):
    username: str = Field(min_length=4, max_length=16)
    password: str = Field(min_length=8, max_length=16)


class TokenResponse(CustomSchema):
    token: str


class UserLogin(UserCreate):
    pass


class UserDB(CustomSchemaDB):
    username: str = Field(min_length=4, max_length=16)
