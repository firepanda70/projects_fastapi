from datetime import datetime

import re

from sqlalchemy import MetaData, func
from sqlalchemy.orm import (
    declared_attr, DeclarativeBase, Mapped,
    mapped_column
)

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class BaseDBModel(DeclarativeBase):
    metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def __tablename__(cls):
        names = re.split("(?=[A-Z])", cls.__name__)
        return "_".join([x.lower() for x in names if x])


class TimeStampMixin(object):
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
