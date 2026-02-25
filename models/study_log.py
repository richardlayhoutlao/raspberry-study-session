import uuid
from config.database import Base
from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, Boolean


class Studylog(Base):
    __tablename__ = 'studylog'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    date_time = Column(DateTime, nullable=False)
    avg_noise = Column(Integer, nullable=False)
    avg_light = Column(Integer, nullable=False)
    focus_score = Column(Integer, nullable=False)