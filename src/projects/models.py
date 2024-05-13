from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import BaseDBModel, TimeStampMixin
from src.users.models import User
from .enums import ProjectStage


class Project(BaseDBModel, TimeStampMixin):
    name: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    stage: Mapped[ProjectStage] = mapped_column(default=ProjectStage.INIT)
    description: Mapped[str | None]

    owner: Mapped[User] = relationship(
        back_populates='projects_owned', overlaps='projects_owned'
    )
    groups = relationship('Group', back_populates='project', cascade='all,delete')
    partisipations = relationship('Partisipant', back_populates='project', cascade='all,delete')
    user_partisipants: Mapped[list[User]] = relationship(
        secondary='partisipant', back_populates='partisipations',
        viewonly=True
    )
    part_req_assotiations = relationship(
        'PartisipationRequest', back_populates='project', cascade='all,delete'
    )
