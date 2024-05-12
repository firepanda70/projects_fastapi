import logging

from fastapi import APIRouter, Depends, status

from src.core.database import AsyncTransaction
from src.groups.dependencies import (
    check_partisipant_delete_right, check_group_read_right
)
from src.groups.schemas import GroupRightsFilter
from src.partisipants.models import Partisipant
from src.projects.models import Project
from src.projects.dependencies import valid_project
from .service import PartisipantService
from .schemas import PartisipantDB, PartisipantDBFull
from .dependencies import (
    check_partisipant, valid_delete_partisipant
)

logger = logging.getLogger(__name__)
partisipant_router = APIRouter()


@partisipant_router.get(
    '/{project_id}/partisipants',
    dependencies=[Depends(check_partisipant)],
    status_code=status.HTTP_200_OK
)
async def get_partisipants(
    partisipant_service: PartisipantService = Depends(PartisipantService)
) -> list[PartisipantDB]:
    return await partisipant_service.get_many()

@partisipant_router.post(
    '/{project_id}/partisipants/filter',
    dependencies=[Depends(check_group_read_right)],
    status_code=status.HTTP_200_OK
)
async def filter_partisipants(
    filter: GroupRightsFilter,
    project: Project = Depends(valid_project),
    partisipant_service: PartisipantService = Depends(PartisipantService)
) -> list[PartisipantDBFull]:
    return await partisipant_service.rights_filter(project, filter)

@partisipant_router.delete(
    '/{project_id}/partisipants/{partisipant_id}',
    dependencies=[Depends(check_partisipant_delete_right)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_partisipant(
    partisipant: Partisipant = Depends(valid_delete_partisipant),
    partisipant_service: PartisipantService = Depends(PartisipantService),
    transaction: AsyncTransaction = Depends(AsyncTransaction),
) -> None:
    async with transaction as id:
        logger.info(f'deleting partisipant {partisipant.id}; transanction {id}')
        await partisipant_service.delete(partisipant)
        logger.info(f'partisipant deleted, transanction {id}')
    return
