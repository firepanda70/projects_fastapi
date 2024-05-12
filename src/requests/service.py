from typing import Sequence

from sqlalchemy import select, update

from src.core.service import BaseService
from src.users.models import User
from .enums import RequestStatus
from .models import Project, PartisipationRequest


class PartReqService(BaseService[PartisipationRequest]):
    model = PartisipationRequest

    async def filter(
        self, project: Project, user_from_id: int = None,
        status: RequestStatus | None = None, id: int | None = None 
    ) -> Sequence[PartisipationRequest]:
        expr = select(PartisipationRequest).where(
            PartisipationRequest.project_id == project.id
        )
        if user_from_id:
            expr = expr.where(PartisipationRequest.user_from_id == user_from_id)
        if status:
            expr = expr.where(PartisipationRequest.status == status)
        if id:
            expr = expr.where(PartisipationRequest.id == id)
        return (await self.session.execute(expr)).scalars().all()

    async def create(self, project: Project, user_id: int) -> PartisipationRequest:
        request = PartisipationRequest(
            project_id=project.id, user_from_id=user_id
        )
        self.session.add(request)
        await self.session.flush()
        return request

    async def accept(
        self, request: PartisipationRequest, user_id: int
    ) -> PartisipationRequest:
        expr = update(PartisipationRequest
            ).where(PartisipationRequest.id == request.id
            ).values(
                processed_by_id=user_id, status=RequestStatus.ACCEPTED
            )
        await self.session.execute(expr)
        await self.session.flush()
        return request
    
    async def deny(
        self, request: PartisipationRequest, user_id: int
    ) -> PartisipationRequest:
        expr = update(PartisipationRequest
            ).where(PartisipationRequest.id == request.id
            ).values(
                processed_by_id=user_id, status=RequestStatus.DENIED
            )
        await self.session.execute(expr)
        await self.session.flush()
        return request
