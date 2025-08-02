from pydantic import BaseModel, field_validator, computed_field
from typing import Dict
from statistics import mean

class Student(BaseModel):
    name: str
    subject_scores: Dict[str, float]

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Student name cannot be empty")
        return value.strip().title()

    @field_validator('subject_scores')
    @classmethod
    def validate_scores(cls, scores):
        if not scores:
            raise ValueError("At least one subject score is required")
        for subject, score in scores.items():
            if not 0 <= score <= 100:
                raise ValueError(f"Score for subject {subject} must be between 0 and 100")
        return scores

    @computed_field
    @property
    def average(self) -> float:
        return round(mean(self.subject_scores.values()), 2)

    @computed_field
    @property
    def grade(self) -> str:
        avg = self.average
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"