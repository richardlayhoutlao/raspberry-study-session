from pydantic import BaseModel, Field
from datetime import datetime

class StudylogRequest(BaseModel):
    date_time: datetime
    noise_score: int
    light_score: int
    temperature_score: int
    focus_score: int
