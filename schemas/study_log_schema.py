from pydantic import BaseModel, Field
from datetime import datetime

class StudylogRequest(BaseModel):
    date_time: datetime
    sound_score: int
    light_score: int
    temperature_score: int
    score: int
    is_uncomfortable: bool
    focus_score: int
    reasons: list[str]
