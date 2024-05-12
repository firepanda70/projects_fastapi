from typing_extensions import Annotated

from pydantic import Field, StringConstraints

from src.core.schemas import CustomSchema, CustomSchemaDB
from .constants import SUPERGROUP_INIT

Slug = Annotated[str, StringConstraints(pattern=r'^[a-zA-Z0-9_-]*$')]


class RightsBase(CustomSchema):
    proj_edit: bool | None = None
    proj_delete: bool | None = None
    group_read: bool | None = None
    group_create: bool | None = None
    group_edit: bool | None = None
    group_delete: bool | None = None
    group_grant: bool | None = None
    group_revoke: bool | None = None
    request_read: bool | None = None
    request_edit: bool | None = None
    partis_delete: bool | None = None


class RightsFilter(RightsBase):
    pass


class GroupRightsFilter(CustomSchema):
    group_names: list[str] | None = None
    rigts_filter: RightsFilter | None = None


class GroupCreate(CustomSchema):
    name: Slug = Field(min_length=1, max_length=32)

    proj_edit: bool = False
    proj_delete: bool = False
    group_read: bool = False
    group_create: bool = False
    group_edit: bool = False
    group_delete: bool = False
    group_grant: bool = False
    group_revoke: bool = False
    request_read: bool = False
    request_edit: bool = False
    partis_delete: bool = False

    @classmethod
    def get_supergroup(cls):
        return cls(**SUPERGROUP_INIT)


class GroupUpdate(RightsBase):
    pass


class GroupDB(GroupCreate, CustomSchemaDB):
    project_id: int
    frozen_group: bool
