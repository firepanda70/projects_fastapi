from fastapi import Depends
from pydantic import PositiveInt

from .exceptions import ProjectNotFound
from .services import ProjectService
from .models import Project


async def valid_project(
    project_id: PositiveInt, project_service: ProjectService = Depends(ProjectService)
) -> Project:
    obj = await project_service.get_full(project_id)
    if not obj:
        raise ProjectNotFound
    return obj
