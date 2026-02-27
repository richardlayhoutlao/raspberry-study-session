from pydantic import BaseModel, Field
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class StudylogRequest(BaseModel):
    date_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sound_score: int = 0
    light_score: int = 0
    temperature_score: float = 0
    score: int = 0
    is_uncomfortable: bool = False
    reasons: list[str] = Field(default_factory=list)