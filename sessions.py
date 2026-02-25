from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException, Body
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class SessionMetrics:
    avg_noise: int
    avg_light: int
    focus_score: int

    def __init__(self, avg_noise, avg_light, focus_score):
        self.avg_noise = avg_noise
        self.avg_light = avg_light
        self.focus_score = focus_score


class Session:
    id: int
    datetime: str
    session_metrics: SessionMetrics

    def __init__(self, id, datetime, session_metrics):
        self.id = id
        self.datetime = datetime
        self.session_metrics = session_metrics
        
class SessionMetricsRequest(BaseModel):
    avg_noise: int = Field(ge=0, le=200)
    avg_light: int = Field(ge=0, le=1000)
    focus_score: int = Field(ge=0, le=100)


class SessionRequest(BaseModel):
    id: Optional[int] = Field(default=None)
    datetime: str = Field(description="ISO format datetime")
    session_metrics: SessionMetricsRequest

    model_config = {
        "json_schema_extra": {
            "example": {
                "datetime": "2026-02-25T08:12:00",
                "session_metrics": {
                    "avg_noise": 64,
                    "avg_light": 180,
                    "focus_score": 72
                }
            }
        }
    }
    
    
SESSIONS_METRICS = [
    Session(
        id=1,
        datetime="2026-02-25T08:12:00",
        session_metrics=SessionMetrics(64, 180, 72)
    ),
    Session(
        id=2,
        datetime="2026-02-25T09:45:00",
        session_metrics=SessionMetrics(78, 120, 58)
    ),
    Session(
        id=3,
        datetime="2026-02-25T10:30:00",
        session_metrics=SessionMetrics(55, 200, 80)
    ),
    Session(
        id=4,
        datetime="2026-02-25T11:15:00",
        session_metrics=SessionMetrics(82, 90, 50)
    ),
    Session(
        id=5,
        datetime="2026-02-25T12:50:00",
        session_metrics=SessionMetrics(69, 140, 66)
    ),
    Session(
        id=6,
        datetime="2026-02-25T13:25:00",
        session_metrics=SessionMetrics(73, 160, 62)
    ),
    Session(
        id=7,
        datetime="2026-02-25T14:40:00",
        session_metrics=SessionMetrics(60, 210, 78)
    ),
    Session(
        id=8,
        datetime="2026-02-25T15:55:00",
        session_metrics=SessionMetrics(85, 110, 54)
    ),
    Session(
        id=9,
        datetime="2026-02-25T16:20:00",
        session_metrics=SessionMetrics(67, 170, 70)
    ),
    Session(
        id=10,
        datetime="2026-02-25T17:35:00",
        session_metrics=SessionMetrics(74, 130, 63)
    )
]


@app.get("/sessions", status_code=status.HTTP_200_OK)
async def read_all_sessions():
    return SESSIONS_METRICS


@app.get("/sessions/{session_id}", status_code=status.HTTP_200_OK)
async def read_session(session_id: int = Path(gt=0)):
    for session in SESSIONS_METRICS:
        if session.id == session_id:
            return session
    raise HTTPException(status_code=404, detail='Session not found')


@app.post("/sessions/create_session", status_code=status.HTTP_201_CREATED)
async def create_session(session_request: SessionRequest):
    new_session = Session(**session_request.model_dump())
    SESSIONS_METRICS.append(new_session)
    
   
@app.put("/sessions/update_session", status_code=status.HTTP_204_NO_CONTENT)
async def update_session(session: SessionRequest):
    session_changed = False
    for i in range(len(SESSIONS_METRICS)):
        if SESSIONS_METRICS[i].id == session.id:
            SESSIONS_METRICS[i] = session
            session_changed = True
    if not session_changed:
        raise HTTPException(status_code=404, detail='Session not found')


@app.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: int = Path(gt=0)):
    session_changed = False
    for i in range(len(SESSIONS_METRICS)):
        if SESSIONS_METRICS[i].id == session_id:
            SESSIONS_METRICS.pop(i)
            session_changed = True
            break
    if not session_changed:
        raise HTTPException(status_code=404, detail='Session not found')
