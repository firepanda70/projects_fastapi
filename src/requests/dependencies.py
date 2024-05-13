import logging

from fastapi import Depends
from pydantic import PositiveInt

from src.core.exceptions import ServerError
from src.projects.models import Project
from src.projects.dependencies import valid_project
from src.partisipants.dependencies import check_not_partisipant
from .enums import RequestStatus
from .exceptions import (
    AlreadyRequested, PartRequestNotFound, NotNewPartRequest
)
from .service import PartReqService
from .models import PartisipationRequest

logger = logging.getLogger(__name__)


async def existing_part_request(
    part_request_id: PositiveInt,
    project: Project = Depends(valid_project),
    part_request_service: PartReqService = Depends(PartReqService)
) -> PartisipationRequest:
    objs = await part_request_service.filter(project, id=part_request_id)
    if not objs:
        raise PartRequestNotFound
    if len(objs) != 1:
        logger.critical('More than one partisipation request '
                        f'found on filter id: {part_request_id}; '
                        f'project id: {project.id}')
        raise ServerError
    return objs[0]

async def valid_partisipation_request(
    user_id: int = Depends(check_not_partisipant),
    project: Project = Depends(valid_project),
    part_req_service: PartReqService = Depends(PartReqService)
) -> Project:
    if await part_req_service.filter(project, user_id, RequestStatus.NEW):
        raise AlreadyRequested
    return project

async def valid_part_request_edit(
    request: PartisipationRequest = Depends(existing_part_request)
) -> PartisipationRequest:
    if request.status != RequestStatus.NEW:
        raise NotNewPartRequest
    return request
