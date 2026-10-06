import asyncio
from app.core.database import async_session_factory
from app.models.enums import MedicationCategory
from app.repositories.medication_repository import MedicationRepository
from app.repositories.rotation_group_repository import RotationGroupRepository
from app.schemas.medication import MedicationCreate
from app.schemas.rotation_group import RotationGroupCreate
from app.services.medication_service import MedicationService


async def populate_initial_medications() -> None:
    async with async_session_factory() as session:
        medication_repo = MedicationRepository(session)
        rotation_group_repo = RotationGroupRepository(session)
        service = MedicationService(medication_repo, rotation_group_repo)

        existing_group = await rotation_group_repo.get_by_name("Analgesia Rotativa Pos-Op")
        if existing_group:
            return

        rotation_group = await service.create_rotation_group(
            RotationGroupCreate(
                name="Analgesia Rotativa Pos-Op",
                spacing_hours=2,
            )
        )

        medications = [
            MedicationCreate(
                name="Toragesic",
                category=MedicationCategory.ANALGESIC,
                min_interval_hours=6,
                is_as_needed=False,
                notes="Sublingual (dissolver sob a lingua)",
                rotation_group_id=rotation_group.id,
            ),
            MedicationCreate(
                name="Paco",
                category=MedicationCategory.ANALGESIC,
                min_interval_hours=6,
                is_as_needed=False,
                notes="Paracetamol + Fosfato de Codeina",
                rotation_group_id=rotation_group.id,
            ),
            MedicationCreate(
                name="Dipirona",
                category=MedicationCategory.ANALGESIC,
                min_interval_hours=6,
                is_as_needed=False,
                notes="1g com agua",
                rotation_group_id=rotation_group.id,
            ),
            MedicationCreate(
                name="Cefadroxila",
                category=MedicationCategory.ANTIBIOTIC,
                min_interval_hours=12,
                is_as_needed=False,
                notes="Antibiotico a cada 12 horas",
            ),
            MedicationCreate(
                name="Ciclobenzaprina",
                category=MedicationCategory.MUSCLE_RELAXANT,
                min_interval_hours=8,
                is_as_needed=False,
                notes="Relaxante muscular",
            ),
            MedicationCreate(
                name="Omeprazol",
                category=MedicationCategory.GASTRIC_PROTECTION,
                min_interval_hours=24,
                is_as_needed=False,
                notes="Tomar pela manha em jejum",
            ),
            MedicationCreate(
                name="Vonau",
                category=MedicationCategory.ANTIEMETIC,
                min_interval_hours=8,
                is_as_needed=True,
                notes="Medicamento de resgate para nauseas e vomitos",
            ),
        ]

        for med in medications:
            await service.create_medication(med)


if __name__ == "__main__":
    asyncio.run(populate_initial_medications())
