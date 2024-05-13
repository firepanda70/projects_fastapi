from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import BaseDBModel, TimeStampMixin
from src.users.models import User
from src.projects.models import Project


class Partisipant(BaseDBModel, TimeStampMixin):
    project_id: Mapped[int] = mapped_column(ForeignKey(Project.id))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))

    project: Mapped[Project] = relationship(
        back_populates='partisipations',
        overlaps='partisipations'
    )
    user: Mapped[User] = relationship(
        back_populates='part_assotiations',
        overlaps='part_assotiations',
        lazy='joined'
    )
    groups_assotiations = relationship(
        'GroupToPartisipant', back_populates='partisipant',
        cascade='all,delete'
    )
    groups = relationship(
        'Group', secondary='group_to_partisipant',
        back_populates='partisipants', viewonly=True
    )
