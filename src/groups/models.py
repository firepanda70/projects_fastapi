from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import BaseDBModel, TimeStampMixin
from src.partisipants.models import Partisipant
from src.projects.models import Project


class Group(BaseDBModel, TimeStampMixin):
    name: Mapped[str]
    project_id: Mapped[int] = mapped_column(ForeignKey(Project.id, ondelete='CASCADE'))
    frozen_group: Mapped[bool] = mapped_column(default=False)

    proj_edit: Mapped[bool] = mapped_column(default=False)
    proj_delete: Mapped[bool] = mapped_column(default=False)
    group_read: Mapped[bool] = mapped_column(default=False)
    group_create: Mapped[bool] = mapped_column(default=False)
    group_edit: Mapped[bool] = mapped_column(default=False)
    group_delete: Mapped[bool] = mapped_column(default=False)
    group_grant: Mapped[bool] = mapped_column(default=False)
    group_revoke: Mapped[bool] = mapped_column(default=False)
    request_read: Mapped[bool] = mapped_column(default=False)
    request_edit: Mapped[bool] = mapped_column(default=False)
    partis_delete: Mapped[bool] = mapped_column(default=False)

    project: Mapped[Project] = relationship(back_populates='groups')
    part_assotiations: Mapped[list['GroupToPartisipant']] = relationship(
        back_populates='group', cascade='all,delete'
    )
    partisipants: Mapped[list[Partisipant]] = relationship(
        secondary='group_to_partisipant', back_populates='groups',
        overlaps='groups_assotiations'
    )

    __table_args__ = (
        UniqueConstraint('name', 'project_id'),
    )


class GroupToPartisipant(BaseDBModel):
    group_id: Mapped[int] = mapped_column(ForeignKey(Group.id))
    partisipant_id: Mapped[int] = mapped_column(ForeignKey(Partisipant.id))
    group: Mapped[Group] = relationship(
        back_populates='part_assotiations',
        overlaps='groups,partisipants'
    )
    partisipant: Mapped[Partisipant] = relationship(
        back_populates='groups_assotiations',
        overlaps='groups,partisipants'
    )
