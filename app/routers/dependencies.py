from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_database_session
from app.repositories.dose_repository import DoseRepository
from app.repositories.medication_repository import MedicationRepository
from app.repositories.rotation_group_repository import (
    RotationGroupRepository,
)
from app.services.dose_service import DoseService
from app.services.medication_service import MedicationService


def get_medication_service(
    session: AsyncSession = Depends(get_database_session),
) -> MedicationService:
    medication_repository = MedicationRepository(session)
    rotation_group_repository = RotationGroupRepository(session)
    return MedicationService(medication_repository, rotation_group_repository)


def get_dose_service(
    session: AsyncSession = Depends(get_database_session),
) -> DoseService:
    dose_repository = DoseRepository(session)
    medication_repository = MedicationRepository(session)
    return DoseService(dose_repository, medication_repository)
