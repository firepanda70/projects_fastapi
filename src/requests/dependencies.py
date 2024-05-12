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


async def existing_part_request(
    part_request_id: PositiveInt,
    project: Project = Depends(valid_project),
    part_request_service: PartReqService = Depends(PartReqService)
) -> PartisipationRequest:
    objs = await part_request_service.filter(project, id=part_request_id)
    if not objs:
        raise PartRequestNotFound
    if len(objs) != 1:
        raise ServerError
    return objs[0]

async def valid_partisipation_request(
    project: Project = Depends(valid_project),
    user_id: int = Depends(check_not_partisipant),
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
