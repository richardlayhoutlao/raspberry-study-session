from pydantic import BaseModel, Field
from datetime import datetime

class StudylogRequest(BaseModel):
    date_time: datetime
    avg_noise: int
    avg_light: int
    focus_score: int
