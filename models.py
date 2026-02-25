from database import Base
from sqlalchemy import Column, Integer, DateTime

class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    avg_noise = Column(Integer, nullable=False)
    avg_light = Column(Integer, nullable=False)
    focus_score = Column(Integer, nullable=False)
