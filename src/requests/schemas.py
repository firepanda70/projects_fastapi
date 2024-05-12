from src.core.schemas import CustomSchemaDB
from src.users.schemas import UserDB
from .enums import RequestStatus


class PartRequestDB(CustomSchemaDB):
    project_id: int
    user_from_id: int
    processed_by_id: int | None
    status: RequestStatus
    user_from: UserDB
    processed_by: UserDB | None
