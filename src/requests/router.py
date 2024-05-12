import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import AsyncTransaction, get_async_session
from src.users.models import User
from src.users.dependencies import valid_token
from src.partisipants.service import PartisipantService
from src.partisipants.schemas import PartisipantDB
from src.partisipants.models import Partisipant
from src.groups.dependencies import (
    check_request_read_right, check_request_edit_right,
)
from .enums import RequestStatus
from .dependencies import (
    valid_project, valid_partisipation_request,
    valid_part_request_edit
)
from .service import PartReqService
from .models import User, Project, PartisipationRequest
from .schemas import PartRequestDB

logger = logging.getLogger(__name__)
part_request_router = APIRouter()


@part_request_router.post(
    '/{project_id}/partisipation_requests',
    dependencies=[Depends(valid_partisipation_request)],
    name='Request partisipation',
    status_code=status.HTTP_201_CREATED
)
async def create_part_request(
    project: Project = Depends(valid_project),
    user_id: int = Depends(valid_token),
    part_req_service: PartReqService = Depends(PartReqService),
    transaction: AsyncTransaction = Depends(AsyncTransaction),
    session: AsyncSession = Depends(get_async_session)
) -> PartRequestDB:
    async with transaction as id:
        request = await part_req_service.create(project, user_id)
        logger.info(f'partisipation request created, id: {request.id}; transanction {id}')
    await session.refresh(request)
    return request


@part_request_router.get(
    '/{project_id}/partisipation_requests',
    name='Get partisipation requests',
    dependencies=[Depends(check_request_read_right)],
    status_code=status.HTTP_200_OK
)
async def get_part_requests(
    status: RequestStatus = RequestStatus.NEW,
    project: Project = Depends(valid_project),
    part_req_service: PartReqService = Depends(PartReqService),
) -> list[PartRequestDB]:
    return await part_req_service.filter(project, status=status)


@part_request_router.patch(
    '/{project_id}/partisipation_requests/{part_request_id}/accept',
    name='Accept partisipation request',
    status_code=status.HTTP_200_OK
)
async def accept_part_request(
    partisipant: Partisipant = Depends(check_request_edit_right),
    request: PartisipationRequest = Depends(valid_part_request_edit),
    project: Project = Depends(valid_project),
    part_req_service: PartReqService = Depends(PartReqService),
    partisipant_service: PartisipantService = Depends(PartisipantService),
    transaction: AsyncTransaction = Depends(AsyncTransaction),
    session: AsyncSession = Depends(get_async_session)
) -> PartisipantDB:
    async with transaction as id:
        request = await part_req_service.accept(request, partisipant.user_id)
        partisipant = await partisipant_service.create(
            project, request.user_from_id
        )
        logger.info(f'partisipant created, id: {partisipant.id}; transanction {id}')
    await session.refresh(partisipant)
    return partisipant


@part_request_router.patch(
    '/{project_id}/partisipation_requests/{part_request_id}/deny',
    name='Deny partisipation request',
    status_code=status.HTTP_200_OK
)
async def deny_part_request(
    partisipant: Partisipant = Depends(check_request_edit_right),
    request: PartisipationRequest = Depends(valid_part_request_edit),
    part_req_service: PartReqService = Depends(PartReqService),
    transaction: AsyncTransaction = Depends(AsyncTransaction),
    session: AsyncSession = Depends(get_async_session)
) -> PartRequestDB:
    async with transaction as id:
        request = await part_req_service.deny(request, partisipant.user_id)
        logger.info(f'partisipation request denied, id: {request.id}; transanction {id}')
    await session.refresh(request)
    return request
