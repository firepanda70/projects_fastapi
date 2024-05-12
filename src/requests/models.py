from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import BaseDBModel, TimeStampMixin
from src.users.models import User
from src.projects.models import Project
from .enums import RequestStatus


class PartisipationRequest(BaseDBModel, TimeStampMixin):
    project_id: Mapped[int] = mapped_column(ForeignKey(Project.id))
    user_from_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    processed_by_id: Mapped[int | None] = mapped_column(ForeignKey(User.id))
    status: Mapped[RequestStatus] = mapped_column(default=RequestStatus.NEW)

    project: Mapped[Project] = relationship(back_populates='part_req_assotiations')
    user_from: Mapped[User] = relationship(
        back_populates='requests',
        foreign_keys=[user_from_id],
        lazy='joined'
    )
    processed_by: Mapped[User | None] = relationship(
        foreign_keys=[processed_by_id],
        lazy='joined'
    )
