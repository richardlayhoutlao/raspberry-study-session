from typing import Annotated
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Sessions
from database import SessionLocal

router = APIRouter()

SESSION_NOT_FOUND = 'session not found.'

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class sessionRequest(BaseModel):
    date_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    avg_noise: int = Field(ge=0, le=200)
    avg_light: int = Field(ge=0)
    focus_score: int = Field(ge=0, le=100)


@router.get("/session", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Sessions).all()


@router.get("/session/{session_id}", status_code=status.HTTP_200_OK)
async def read_session(db: db_dependency, session_id: int = Path(gt=0)):
    session_model = db.query(Sessions).filter(Sessions.id == session_id).first()
    if session_model is not None:
        return session_model
    raise HTTPException(status_code=404, detail=SESSION_NOT_FOUND)


@router.post("/session", status_code=status.HTTP_201_CREATED)
async def create_session(db: db_dependency,
                      session_request: sessionRequest):
    session_model = Sessions(**session_request.model_dump())
    db.add(session_model)
    db.commit()
    db.refresh(session_model)
    return session_model

    
@router.put("/session/{session_id}", status_code=status.HTTP_200_OK)
async def update_session(db: db_dependency,
                      session_request: sessionRequest,
                      session_id: int = Path(gt=0)):
    session_model = db.query(Sessions).filter(Sessions.id == session_id).first()
    if session_model is None:
        raise HTTPException(status_code=404, detail=SESSION_NOT_FOUND)

    session_model.date_time = session_request.date_time
    session_model.avg_noise = session_request.avg_noise
    session_model.avg_light = session_request.avg_light
    session_model.focus_score = session_request.focus_score

    db.add(session_model)
    db.commit()
    db.refresh(session_model)
    return session_model


@router.delete("/session/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(db: db_dependency, session_id: int = Path(gt=0)):
    session_model = db.query(Sessions).filter(Sessions.id == session_id).first()
    if session_model is None:
        raise HTTPException(status_code=404, detail='session not found.')
    db.query(Sessions).filter(Sessions.id == session_id).delete()
    db.commit()












