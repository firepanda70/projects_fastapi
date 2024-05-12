from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from src.core.service import BaseService
from src.projects.models import Project
from src.groups.models import Group
from src.groups.schemas import GroupRightsFilter
from .models import Partisipant


class PartisipantService(BaseService[Partisipant]):
    model = Partisipant
    async def create(self, project: Project, user_id: int) -> Partisipant:
        partisipation = Partisipant(
            project_id=project.id, user_id=user_id
        )
        self.session.add(partisipation)
        await self.session.flush()
        return partisipation

    async def filter(
        self, project: Project | None = None,
        user_id: int | None = None,
        id: int | None = None
    ) -> Sequence[Partisipant]:
        expr = select(Partisipant)
        if project:
            expr = expr.where(Partisipant.project_id == project.id)
        if user_id:
            expr = expr.where(Partisipant.user_id == user_id)
        if id:
            expr = expr.where(Partisipant.id == id)
        return (await self.session.execute(expr)).scalars().all()

    async def rights_filter(
        self, project: Project, filter: GroupRightsFilter
    ) -> Sequence[Partisipant]:
        expr = select(Partisipant
            ).join(Partisipant.groups
            ).where(Partisipant.project_id==project.id)
        if filter.group_names:
            expr = expr.where(Group.name.in_(filter.group_names))
        if filter.rigts_filter:
            for name, value in filter.rigts_filter.model_dump(exclude_none=True).items():
               expr = expr.where(getattr(Group, name)==value)
        expr = expr.options(contains_eager(Partisipant.groups))
        return (await self.session.execute(expr)).unique().scalars().all()
