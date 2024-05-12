from typing import Sequence

from sqlalchemy import select, update, func, and_
from sqlalchemy.orm import selectinload, contains_eager

from src.core.service import BaseService
from src.groups.models import Group, GroupToPartisipant
from src.partisipants.models import Partisipant
from .models import Project
from .schemas import ProjectCreate, ProjectUpdate


class ProjectService(BaseService[Project]):
    model = Project
    async def get_full(self, id: int) -> Project | None: 
        expr = select(Project
            ).where(Project.id == id
            ).options(
                selectinload(Project.user_partisipants),
                selectinload(Project.partisipations),
                selectinload(Project.groups),
                selectinload(Project.groups, Group.partisipants),
            )
        return (await self.session.execute(expr)).scalar_one_or_none()

    async def get_many(self) -> Sequence[tuple[Project, int]]:
        expr = select(
            Project, func.count(Partisipant.id).label('partisipant_count')
            ).join(Partisipant
            ).group_by(Project.id)
        res = await self.session.execute(expr)
        return res.tuples().all()

    async def create(self, obj_in: ProjectCreate, user_id: int) -> Project:
        project = Project(
            name=obj_in.name, owner_id=user_id,
            description=obj_in.description
        )
        self.session.add(project)
        await self.session.flush()
        return project
    
    async def update(self, update_data: ProjectUpdate, project: Project) -> Project:
        expr = update(Project
            ).where(Project.id == project.id
            ).values(
                **update_data.model_dump(exclude_none=True)
            )
        await self.session.execute(expr)
        await self.session.flush()
        return project

    async def filter(
        self, partisipan_user_id: int
    ) -> Sequence[Project]:
        expr = select(Project
            ).join(Project.partisipations,
            ).where(
                Partisipant.id == partisipan_user_id,
            )
        return (await self.session.execute(expr)).scalars().all()
