import uuid
from config.database import Base
from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, Boolean


class Studylog(Base):
    __tablename__ = 'studylog'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    date_time = Column(DateTime, nullable=False)
    sound_score = Column(Integer, nullable=False)
    light_score = Column(Integer, nullable=False)
    temperature_score = Column(Integer, nullable=False)
    focus_score = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False) 
    is_uncomfortable = Column(Boolean, nullable=False)
    reasons = Column(JSON, nullable=False)