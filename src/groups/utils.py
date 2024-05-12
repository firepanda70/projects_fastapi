from src.partisipants.models import Partisipant
from src.projects.models import Project
from .exceptions import Forbidden
from .schemas import RightsFilter


async def rights_check(
    filter: RightsFilter, project: Project, partisipant: Partisipant
) -> Partisipant:
    filters = filter.model_dump(exclude_none=True)
    if len(filters) == 0:
        raise ValueError('Invalid filter init')
    for group in project.groups:
        if all([getattr(group, name) == value for name, value in filters.items()]):
            if any([el.id == partisipant.id for el in group.partisipants]):
                return partisipant
    raise Forbidden
