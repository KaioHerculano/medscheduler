from typing import List, Sequence
from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.api.v1.dependencies import get_medication_service
from app.schemas.medication import MedicationCreate, MedicationRead
from app.schemas.rotation_group import RotationGroupCreate, RotationGroupRead
from app.services.medication_service import MedicationService

router = APIRouter()


@router.get("/", response_model=List[MedicationRead])
async def list_medications(
    service: MedicationService = Depends(get_medication_service),
) -> Sequence[MedicationRead]:
    return await service.list_medications()


@router.post("/", response_model=MedicationRead, status_code=status.HTTP_201_CREATED)
async def create_medication(
    payload: MedicationCreate,
    service: MedicationService = Depends(get_medication_service),
) -> MedicationRead:
    return await service.create_medication(payload)


@router.get("/{medication_id}", response_model=MedicationRead)
async def get_medication(
    medication_id: UUID,
    service: MedicationService = Depends(get_medication_service),
) -> MedicationRead:
    return await service.get_medication_by_id(medication_id)


@router.get("/groups/rotation", response_model=List[RotationGroupRead])
async def list_rotation_groups(
    service: MedicationService = Depends(get_medication_service),
) -> Sequence[RotationGroupRead]:
    return await service.list_rotation_groups()


@router.post("/groups/rotation", response_model=RotationGroupRead, status_code=status.HTTP_201_CREATED)
async def create_rotation_group(
    payload: RotationGroupCreate,
    service: MedicationService = Depends(get_medication_service),
) -> RotationGroupRead:
    return await service.create_rotation_group(payload)
