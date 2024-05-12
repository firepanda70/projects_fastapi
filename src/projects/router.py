import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import AsyncTransaction, get_async_session
from src.users.dependencies import valid_token
from src.partisipants.service import PartisipantService
from src.groups.services import GroupService, GroupToPartService
from src.groups.schemas import GroupCreate
from src.groups.dependencies import (
    check_project_edit_right, check_project_delete_right
)
from .dependencies import valid_project
from .services import ProjectService
from .models import Project
from .schemas import (
    ProjectCreate, ProjectDB, ProjectUpdate, ProjectDBCount
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
project_router = APIRouter()


@project_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate, user_id: int = Depends(valid_token),
    project_service: ProjectService = Depends(ProjectService),
    partisipant_service: PartisipantService = Depends(PartisipantService),
    group_service: GroupService = Depends(GroupService),
    group_to_part_service: GroupToPartService = Depends(GroupToPartService),
    transaction: AsyncTransaction = Depends(AsyncTransaction),
    session: AsyncSession = Depends(get_async_session)
) -> ProjectDB:
    async with transaction as id:
        project = await project_service.create(data, user_id)
        logger.info(f'created project, id: {project.id}; transanction: {id}')
        partisipant = await partisipant_service.create(project, user_id)
        logger.info(f'created partisipant, id: {partisipant.id}; transanction: {id}')
        supergroup = await group_service.create(
            GroupCreate.get_supergroup(), project, frozen=True
        )
        logger.info(f'created group, id: {partisipant.id}; transanction: {id}')
        await group_to_part_service.grant(supergroup, partisipant)
        logger.info((f'granted group {supergroup.id}, to partisipant {partisipant.id};'
                     f' transanction: {id}'))
    await session.refresh(project)
    return project


@project_router.get(
    '/', dependencies=[Depends(valid_token)],
    status_code=status.HTTP_200_OK
)
async def get_projects(
    project_service: ProjectService = Depends(ProjectService)
) -> list[ProjectDBCount]:
    results = await project_service.get_many()
    return [
        ProjectDBCount.model_validate(
            obj, context={'partisipant_count': count}
        ) for obj, count in results
    ]

@project_router.get(
    '/patisipating', status_code=status.HTTP_200_OK,
    name='Get list partispating projects'
)
async def get_partisipating(
    user_id: int = Depends(valid_token),
    project_service: ProjectService = Depends(ProjectService)
) -> list[ProjectDB]:
    return await project_service.filter(user_id)
    

@project_router.get(
    '/{project_id}', dependencies=[Depends(valid_token)],
    status_code=status.HTTP_200_OK
)
async def get_project(
    project: Project = Depends(valid_project)
) -> ProjectDB:
    return project


@project_router.patch(
    '/{project_id}', dependencies=[Depends(check_project_edit_right)],
    status_code=status.HTTP_200_OK
)
async def update_project(
    update_data: ProjectUpdate,
    project: Project = Depends(valid_project),
    project_service: ProjectService = Depends(ProjectService),
    transaction: AsyncTransaction = Depends(AsyncTransaction),
    session: AsyncSession = Depends(get_async_session)
) -> ProjectDB:
    async with transaction as id:
        project = await project_service.update(update_data, project)
        logger.info(f'created project {project.id}, transanction: {id}')
    await session.refresh(project)
    return project


@project_router.delete(
    '/{project_id}', dependencies=[Depends(check_project_delete_right)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_project(
    project: Project = Depends(valid_project),
    project_service: ProjectService = Depends(ProjectService),
    transaction: AsyncTransaction = Depends(AsyncTransaction)
) -> None:
    async with transaction as id:
        logger.info(f'deleting project {project.id}, transanction: {id}')
        await project_service.delete(project)
        logger.info(f'Project deleted transanction: {id}')
    return
