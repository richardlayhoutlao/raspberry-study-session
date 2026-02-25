from fastapi import Body, FastAPI

app = FastAPI()

SESSIONS_METRICS = [
  {
    "id": 1,
    "datetime": "2026-02-25T08:12:00",
    "sessionMetrics": {
      "avg_noise": 64,
      "avg_light": 180,
      "focus_score": 72
    }
  },
  {
    "id": 2,
    "datetime": "2026-02-25T09:45:00",
    "sessionMetrics": {
      "avg_noise": 78,
      "avg_light": 120,
      "focus_score": 58
    }
  },
  {
    "id": 3,
    "datetime": "2026-02-25T10:30:00",
    "sessionMetrics": {
      "avg_noise": 55,
      "avg_light": 200,
      "focus_score": 80
    }
  },
  {
    "id": 4,
    "datetime": "2026-02-25T11:15:00",
    "sessionMetrics": {
      "avg_noise": 82,
      "avg_light": 90,
      "focus_score": 50
    }
  },
  {
    "id": 5,
    "datetime": "2026-02-25T12:50:00",
    "sessionMetrics": {
      "avg_noise": 69,
      "avg_light": 140,
      "focus_score": 66
    }
  },
  {
    "id": 6,
    "datetime": "2026-02-25T13:25:00",
    "sessionMetrics": {
      "avg_noise": 73,
      "avg_light": 160,
      "focus_score": 62
    }
  },
  {
    "id": 7,
    "datetime": "2026-02-25T14:40:00",
    "sessionMetrics": {
      "avg_noise": 60,
      "avg_light": 210,
      "focus_score": 78
    }
  },
  {
    "id": 8,
    "datetime": "2026-02-25T15:55:00",
    "sessionMetrics": {
      "avg_noise": 85,
      "avg_light": 110,
      "focus_score": 54
    }
  },
  {
    "id": 9,
    "datetime": "2026-02-25T16:20:00",
    "sessionMetrics": {
      "avg_noise": 67,
      "avg_light": 170,
      "focus_score": 70
    }
  },
  {
    "id": 10,
    "datetime": "2026-02-25T17:35:00",
    "sessionMetrics": {
      "avg_noise": 74,
      "avg_light": 130,
      "focus_score": 63
    }
  }
]


@app.get("/sessions")
async def read_all_sessions():
    return SESSIONS_METRICS


@app.get("/sessions/{session_id}")
async def read_session(session_id: int):
    for session in SESSIONS_METRICS:
        if session.get('id') == session_id:
            return session

@app.post("/sessions/create_session")
async def create_session(new_session=Body()):
    SESSIONS_METRICS.append(new_session)


@app.put("/sessions/update_session")
async def update_session(updated_session=Body()):
    for i in range(len(SESSIONS_METRICS)):
        if SESSIONS_METRICS[i].get('id') == updated_session.get('id'):
            SESSIONS_METRICS[i] = updated_session


@app.delete("/session/delete_session/{session_id}")
async def delete_session(session_id: int):
    for i in range(len(SESSIONS_METRICS)):
        if SESSIONS_METRICS[i].get('id') == session_id:
            SESSIONS_METRICS.pop(i)
            break