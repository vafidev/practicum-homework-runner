from enum import StrEnum, auto


class SubmissionStatus(StrEnum):
    SUBMITTED = auto()
    IN_REVIEW = auto()
    GRADED = auto()
    REJECTED = auto()
