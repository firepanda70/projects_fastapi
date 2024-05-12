from src.core.schemas import CustomSchemaDB
from src.users.schemas import UserDB
from src.groups.schemas import GroupDB


class PartisipantDB(CustomSchemaDB):
    project_id: int
    user_id: int
    user: UserDB


class PartisipantDBFull(PartisipantDB):
    groups: list[GroupDB]
