import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import AsyncTransaction, get_async_session
from src.projects.models import Project
from src.projects.dependencies import valid_project
from src.partisipants.models import Partisipant
from src.partisipants.service import PartisipantService
from src.partisipants.schemas import PartisipantDBFull
from src.partisipants.dependencies import check_partisipant
from .models import Group
from .services import GroupService, GroupToPartService
from .schemas import GroupDB, GroupCreate, GroupUpdate
from .dependencies import (
    check_group_read_right, check_group_create_right,
    valid_group_create, check_group_edit_right,
    valid_group_edit, valid_group,
    check_group_grant_right, valid_group_grant_partisipant,
    check_group_revoke_right, valid_group_revoke_partisipant,
    check_group_delete_right
)

logger = logging.getLogger(__name__)
group_router = APIRouter()

@group_router.get(
    '/{project_id}/groups', status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_group_read_right)]
)
async def get_groups(
    project: Project = Depends(valid_project),
    group_service: GroupService = Depends(GroupService)
) -> list[GroupDB]:
    return await group_service.filter(project)


@group_router.get(
    '/{project_id}/groups/mine', status_code=status.HTTP_200_OK
)
async def get_mine_groups(
    partisipant: Partisipant = Depends(check_partisipant),
    project: Project = Depends(valid_project),
    group_service: GroupService = Depends(GroupService)
) -> list[GroupDB]:
    return await group_service.filter(project, partisipant=partisipant)


@group_router.post(
    '/{project_id}/groups', status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_group_create_right)]
)
async def create_group(
    group_data: GroupCreate = Depends(valid_group_create),
    project: Project = Depends(valid_project),
    group_service: GroupService = Depends(GroupService),
    transanction: AsyncTransaction = Depends(AsyncTransaction),
    session: AsyncSession = Depends(get_async_session)
) -> GroupDB:
    async with transanction as id:
        group = await group_service.create(group_data, project)
        logger.info(f'group created, id: {group.id}; transanction: {id}')
    await session.refresh(group)
    return group

@group_router.patch(
    '/{project_id}/groups/{group_name}',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_group_edit_right)]
)
async def update_group(
    update_data: GroupUpdate,
    group: Group = Depends(valid_group_edit),
    group_service: GroupService = Depends(GroupService),
    transanction: AsyncTransaction = Depends(AsyncTransaction),
    session: AsyncSession = Depends(get_async_session)
) -> GroupDB:
    async with transanction as id:
        group = await group_service.update(group, update_data)
        logger.info(f'group updated, id: {group.id}; transanction: {id}')
    await session.refresh(group)
    return group

@group_router.delete(
    '/{project_id}/groups/{group_name}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_group_delete_right)]
)
async def delete_group(
    group: Group = Depends(valid_group_edit),
    group_service: GroupService = Depends(GroupService),
    transanction: AsyncTransaction = Depends(AsyncTransaction)
) -> None:
    async with transanction as id:
        logger.info(f'deleting group, id: {group.id}; transanction: {id}')
        await group_service.delete(group)
        logger.info(f'group deleted, transanction: {id}')
    return

@group_router.post(
    '/{project_id}/groups/{group_name}/grant',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_group_grant_right)],
    name='Grant group to partisipant'
)
async def grant_group(
    partisipant: Partisipant = Depends(valid_group_grant_partisipant),
    group: Group = Depends(valid_group),
    partisipant_service: PartisipantService = Depends(PartisipantService),
    group_to_part_serice: GroupToPartService = Depends(GroupToPartService),
    transanction: AsyncTransaction = Depends(AsyncTransaction),
) -> PartisipantDBFull:
    partisipnat_id = partisipant.id
    async with transanction as id:
        grant = await group_to_part_serice.grant(group, partisipant)
        logger.info((f'group {group.id} granted to partisipant {partisipant.id}, '
                     f'id {grant.id}, transanction: {id}'))
    return await partisipant_service.get_full(partisipnat_id)

@group_router.post(
    '/{project_id}/groups/{group_name}/revoke',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_group_revoke_right)],
    name='Revoke group from partisipant'
)
async def revoke_group(
    partisipant: Partisipant = Depends(valid_group_revoke_partisipant),
    group: Group = Depends(valid_group),
    partisipant_service: PartisipantService = Depends(PartisipantService),
    group_to_part_serice: GroupToPartService = Depends(GroupToPartService),
    transanction: AsyncTransaction = Depends(AsyncTransaction)
) -> PartisipantDBFull:
    partisipnat_id = partisipant.id
    async with transanction as id:
        await group_to_part_serice.revoke(group, partisipant)
        logger.info((f'group {group.id} revoked from partisipant {partisipant.id}, '
                     f'transanction: {id}'))
    return await partisipant_service.get_full(partisipnat_id)
