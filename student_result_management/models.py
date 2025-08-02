from pydantic import BaseModel, validator
from typing import Dict
from statistics import mean

class Student(BaseModel):
    name: str
    subject_score: Dict[str, float]
    average: float = None
    grade: str = None

    @validator('name')
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Student name cannot be empty")
        return value

    @validator('subject_score')
    def validate_scores(cls, scores):
        if not scores:
            raise ValueError("At least one subject score is required")
        for subject, score in scores.items():
            if not 0 <= score <= 100:
                raise ValueError(f"Score for subject {subject} must be between 0 and 100")
        return scores

    @validator('average', pre=True, always=True)
    def calculate_average(cls, v, values):
        if 'subject_scores' in values:
            return mean(values['subject_scores'].values())
        return v

    @validator('grade', pre=True, always=True)
    def calculate_grade(cls, v, values):
        if 'average' in values and values['average'] is not None:
            avg = values['average']
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
        return v