from fastapi import Depends
from pydantic import PositiveInt

from src.core.exceptions import ServerError
from src.users.models import User
from src.users.dependencies import valid_token
from src.projects.models import Project
from src.projects.dependencies import valid_project
from .models import Partisipant
from .service import PartisipantService
from .exceptions import (
    AlreadyPartisipant, NotPartisipant,
    PartisipantNotFound, PartisipantIsOwner
)


async def valid_project_partisipant(
    partisipant_id: PositiveInt,
    project: Project = Depends(valid_project),
    partisipant_service: PartisipantService = Depends(PartisipantService)
) -> Partisipant:
    objs = await partisipant_service.filter(project, id=partisipant_id)
    if not objs:
        raise PartisipantNotFound
    if len(objs) != 1:
        raise ServerError
    return objs[0]

async def check_not_partisipant(
    project: Project = Depends(valid_project),
    user_id: int = Depends(valid_token),
) -> int:
    if user_id in [el.id for el in project.user_partisipants]:
        raise AlreadyPartisipant
    return user_id

async def check_partisipant(
    project: Project = Depends(valid_project),
    user_id: int = Depends(valid_token),
) -> Partisipant:
    for partisipant in project.partisipations:
        if user_id == partisipant.user_id:
            return partisipant
    raise NotPartisipant

async def valid_delete_partisipant(
    project: Project = Depends(valid_project_partisipant),
    partisipant: Partisipant = Depends(valid_project)
) -> Partisipant:
    if project.owner_id == partisipant.user_id:
        raise PartisipantIsOwner
    return partisipant
