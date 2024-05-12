from pydantic import Field, field_validator, ValidationInfo

from src.core.schemas import CustomSchema, CustomSchemaDB
from src.groups.schemas import GroupDB
from .enums import ProjectStage


class ProjectCreate(CustomSchema):
    name: str = Field(min_length=1, max_length=64)
    description: str | None = Field(None, min_length=1, max_length=128)


class ProjectUpdate(CustomSchema):
    name: str | None = Field(None, min_length=1, max_length=64)
    description: str | None = Field(None, min_length=1, max_length=128)
    stage: ProjectStage | None = None


class ProjectDB(ProjectCreate, CustomSchemaDB):
    owner_id: int
    stage: ProjectStage


class ProjectDBCount(ProjectDB):
    partisipant_count: int = Field(-1, validate_default=True)

    @field_validator('partisipant_count', mode='before')
    @classmethod
    def validate_partisipant_count(cls, value: int, info: ValidationInfo) -> int:
        if (
            value < 0 and (
            not info.context or (
            info.context.get('partisipant_count', None) is None
        ))):
            raise ValueError('valid partisipant_count not provided')
        if value >= 0:
            return value
        return info.context['partisipant_count']
