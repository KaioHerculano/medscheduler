from enum import Enum


class MedicationCategory(str, Enum):
    ANALGESIC = 'ANALGESIC'
    ANTIBIOTIC = 'ANTIBIOTIC'
    GASTRIC_PROTECTION = 'GASTRIC_PROTECTION'
    MUSCLE_RELAXANT = 'MUSCLE_RELAXANT'
    ANTIEMETIC = 'ANTIEMETIC'


class DoseStatus(str, Enum):
    PENDING = 'PENDING'
    TAKEN = 'TAKEN'
    SNOOZED = 'SNOOZED'
    SKIPPED = 'SKIPPED'
