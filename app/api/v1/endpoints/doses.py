from typing import Dict, List
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, status
from app.api.v1.dependencies import get_dose_service
from app.schemas.dose import DoseCreate, DoseRead
from app.services.dose_service import DoseService

router = APIRouter()


@router.get("/timeline", response_model=Dict[str, List[DoseRead]])
async def get_doses_timeline(
    service: DoseService = Depends(get_dose_service),
) -> Dict[str, List[DoseRead]]:
    return await service.get_timeline_grouped_by_status()


@router.post("/", response_model=DoseRead, status_code=status.HTTP_201_CREATED)
async def schedule_dose(
    payload: DoseCreate,
    service: DoseService = Depends(get_dose_service),
) -> DoseRead:
    return await service.schedule_dose(payload)


@router.post("/{dose_id}/take", response_model=DoseRead)
async def mark_dose_taken(
    dose_id: UUID,
    service: DoseService = Depends(get_dose_service),
) -> DoseRead:
    return await service.mark_dose_as_taken(dose_id, datetime.utcnow())


@router.post("/{dose_id}/snooze", response_model=DoseRead)
async def snooze_dose(
    dose_id: UUID,
    delay_minutes: int = 15,
    service: DoseService = Depends(get_dose_service),
) -> DoseRead:
    return await service.snooze_dose(dose_id, delay_minutes)


@router.post("/{dose_id}/skip", response_model=DoseRead)
async def skip_dose(
    dose_id: UUID,
    service: DoseService = Depends(get_dose_service),
) -> DoseRead:
    return await service.skip_dose(dose_id)
