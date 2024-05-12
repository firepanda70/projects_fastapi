from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import selectinload

from src.core.service import BaseService
from src.projects.models import Project
from src.partisipants.models import Partisipant
from .models import Group, GroupToPartisipant
from .schemas import GroupCreate, GroupUpdate


class GroupService(BaseService[Group]):
    model = Group
    async def create(
        self, obj_in: GroupCreate, project: Project, frozen: bool = False
    ) -> Group:
        group = Group(
            project_id=project.id, frozen_group=frozen,
            **obj_in.model_dump(exclude_none=True)
        )
        self.session.add(group)
        await self.session.flush()
        return group
    
    async def get_by_name(self, name: str) -> Group | None:
        expr = select(Group).where(Group.name == name)
        return (await self.session.execute(expr)).scalar_one_or_none()
    
    async def filter(
        self, project: Project | None = None,
        name: str | None = None, id: int | None = None,
        partisipant: Partisipant | None = None
    ):
        expr = select(Group)
        if project:
            expr = expr.where(Group.project_id == project.id)
        if name:
            expr = expr.where(Group.name == name)
        if id:
            expr = expr.where(Group.id == id)
        if partisipant:
            expr = expr.join(Group.partisipants
                ).where(Partisipant.id == partisipant.id)
        return (await self.session.execute(expr)).scalars().all()
    
    async def update(self, group: Group, update_data: GroupUpdate) -> Group:
        expr = update(Group
            ).where(Group.id == group.id
            ).values(
                **update_data.model_dump(exclude_none=True)
            )
        await self.session.execute(expr)
        await self.session.flush()
        return group


class GroupToPartService(BaseService[GroupToPartisipant]):
    model = GroupToPartisipant
    async def grant(
        self, group: Group, partisipant: Partisipant
    ) -> GroupToPartisipant:
        obj = GroupToPartisipant(
            group_id=group.id, partisipant_id=partisipant.id
        )
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def revoke(
        self, group: Group, partisipant: Partisipant
    ) -> bool:
        expr = delete(GroupToPartisipant
            ).where(
                and_(
                    GroupToPartisipant.group_id == group.id,
                    GroupToPartisipant.partisipant_id == partisipant.id
                )
            )
        await self.session.execute(expr)
        await self.session.flush()
        return True
