from enum import StrEnum, auto


class EnrollmentStatus(StrEnum):
    ACTIVE = auto()
    COMPLETED = auto()
    DROPPED = auto()
