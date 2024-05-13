import logging

from fastapi import Depends
from pydantic import PositiveInt

from src.core.exceptions import ServerError
from src.users.dependencies import valid_token
from src.projects.models import Project
from src.projects.dependencies import valid_project
from .models import Partisipant
from .service import PartisipantService
from .exceptions import (
    AlreadyPartisipant, NotPartisipant,
    PartisipantNotFound, PartisipantIsOwner
)

logger = logging.getLogger(__name__)

async def valid_project_partisipant(
    partisipant_id: PositiveInt,
    project: Project = Depends(valid_project),
    partisipant_service: PartisipantService = Depends(PartisipantService)
) -> Partisipant:
    objs = await partisipant_service.filter(project, id=partisipant_id)
    if not objs:
        raise PartisipantNotFound
    if len(objs) != 1:
        logger.critical(f'More than one partisipan on filter id: {partisipant_id}; '
                        f'project id: {project.id}')
        raise ServerError
    return objs[0]

async def check_not_partisipant(
    user_id: int = Depends(valid_token),
    project: Project = Depends(valid_project),
) -> int:
    if user_id in [el.user_id for el in project.partisipations]:
        raise AlreadyPartisipant
    return user_id

async def check_partisipant(
    user_id: int = Depends(valid_token),
    project: Project = Depends(valid_project),
) -> Partisipant:
    for partisipant in project.partisipations:
        if user_id == partisipant.user_id:
            return partisipant
    raise NotPartisipant

async def valid_delete_partisipant(
    partisipant: Partisipant = Depends(valid_project_partisipant),
    project: Project = Depends(valid_project)
) -> Partisipant:
    if project.owner_id == partisipant.user_id:
        raise PartisipantIsOwner
    return partisipant
