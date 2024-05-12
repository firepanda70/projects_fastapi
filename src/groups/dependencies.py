from fastapi import Depends

from src.core.exceptions import ServerError
from src.users.models import User
from src.projects.models import Project
from src.projects.dependencies import valid_project
from src.partisipants.models import Partisipant
from src.partisipants.dependencies import (
    check_partisipant, valid_project_partisipant
)
from .models import Group, GroupToPartisipant
from .exceptions import (
    GroupNameTaken, GroupNotFound, FrozenGroup,
    PartisipantAlreadyInGroup, PartisipantNotInGroup,
    OwnerPartisipantSupergroup
)
from .schemas import RightsFilter, GroupCreate, GroupUpdate
from .services import GroupService
from .utils import rights_check
from .constants import SUPERGROUP_INIT


async def valid_group(
    group_name: str,
    project: Project = Depends(valid_project),
    grop_service: GroupService = Depends(GroupService)
) -> Group:
    objs = await grop_service.filter(project, group_name)
    if not objs:
        raise GroupNotFound
    if len(objs) != 1:
        raise ServerError
    return objs[0]

async def valid_group_create(
    group_data: GroupCreate,
    group_service: GroupService = Depends(GroupService)
) -> GroupCreate:
    obj = await group_service.get_by_name(group_data.name)
    if obj:
        raise GroupNameTaken
    return group_data

async def valid_group_edit(
    group: Group = Depends(valid_group),
) -> GroupUpdate:
    if group.frozen_group:
        raise FrozenGroup
    return group

async def valid_group_grant_partisipant(
    partisipant: Partisipant = Depends(valid_project_partisipant),
    grop: Group = Depends(valid_group)
) -> Partisipant:
    if any([el.id == partisipant.id for el in grop.partisipants]):
        raise PartisipantAlreadyInGroup
    return partisipant

async def valid_group_revoke_partisipant(
    partisipant: Partisipant = Depends(valid_project_partisipant),
    project: Project = Depends(valid_project),
    grop: Group = Depends(valid_group)
) -> Partisipant:
    if all([el.id != partisipant.id for el in grop.partisipants]):
        raise PartisipantNotInGroup
    if (
        (grop.name == SUPERGROUP_INIT['name']) and 
        (partisipant.user_id == project.owner_id)
    ):
        raise OwnerPartisipantSupergroup
    return partisipant

async def check_request_read_right(
    project: Project = Depends(valid_project),
    user: Partisipant = Depends(check_partisipant)
) -> Partisipant:
    return await rights_check(RightsFilter(request_read=True), project, user)

async def check_request_edit_right(
    project: Project = Depends(valid_project),
    user: Partisipant = Depends(check_partisipant)
) -> Partisipant:
    return await rights_check(RightsFilter(request_edit=True), project, user)

async def check_project_edit_right(
    project: Project = Depends(valid_project),
    user: Partisipant = Depends(check_partisipant)
) -> Partisipant:
    return await rights_check(RightsFilter(proj_edit=True), project, user)

async def check_project_delete_right(
    project: Project = Depends(valid_project),
    user: Partisipant = Depends(check_partisipant)
) -> Partisipant:
    return await rights_check(RightsFilter(proj_delete=True), project, user)

async def check_partisipant_delete_right(
    project: Project = Depends(valid_project),
    user: Partisipant = Depends(check_partisipant)
) -> Partisipant:
    return await rights_check(RightsFilter(partis_delete=True), project, user)

async def check_group_read_right(
    project: Project = Depends(valid_project),
    user: Partisipant = Depends(check_partisipant)
) -> Partisipant:
    return await rights_check(RightsFilter(group_read=True), project, user)

async def check_group_create_right(
    project: Project = Depends(valid_project),
    user: Partisipant = Depends(check_partisipant)
) -> Partisipant:
    return await rights_check(RightsFilter(group_create=True), project, user)

async def check_group_edit_right(
    project: Project = Depends(valid_project),
    user: Partisipant = Depends(check_partisipant)
) -> Partisipant:
    return await rights_check(RightsFilter(group_edit=True), project, user)

async def check_group_grant_right(
    project: Project = Depends(valid_project),
    user: Partisipant = Depends(check_partisipant)
) -> Partisipant:
    return await rights_check(RightsFilter(group_grant=True), project, user)

async def check_group_revoke_right(
    project: Project = Depends(valid_project),
    user: Partisipant = Depends(check_partisipant)
) -> Partisipant:
    return await rights_check(RightsFilter(group_revoke=True), project, user)

async def check_group_delete_right(
    project: Project = Depends(valid_project),
    user: Partisipant = Depends(check_partisipant)
) -> Partisipant:
    return await rights_check(RightsFilter(group_delete=True), project, user)
