from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import BaseDBModel, TimeStampMixin


class User(BaseDBModel, TimeStampMixin):
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    projects_owned = relationship(
        'Project', back_populates='owner', cascade='all,delete'
    )
    part_assotiations = relationship(
        'Partisipant', back_populates='user', cascade='all,delete'
    )
    partisipations = relationship(
        'Project', secondary='partisipant', viewonly=True,
        back_populates='user_partisipants', cascade='all,delete'
    )
    requests = relationship(
        'PartisipationRequest', back_populates='user_from',
        primaryjoin='User.id == PartisipationRequest.user_from_id',
        cascade='all,delete'
    )
