from fastapi import APIRouter

from src.users.router import user_router
from src.projects.router import project_router
from src.requests.router import part_request_router
from src.partisipants.router import partisipant_router
from src.groups.router import group_router


v1_router = APIRouter()
v1_router.include_router(user_router, prefix='/users', tags=['Users'])
v1_router.include_router(project_router, prefix='/projects', tags=['Projects'])
v1_router.include_router(
    part_request_router, prefix='/projects', tags=['Partisipation requests']
)
v1_router.include_router(
    partisipant_router, prefix='/projects', tags=['Partisipants']
)
v1_router.include_router(
    group_router, prefix='/projects', tags=['Groups']
)
