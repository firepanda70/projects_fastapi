from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CustomSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')


class CustomSchemaDB(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    created_at: datetime
    updated_at: datetime
