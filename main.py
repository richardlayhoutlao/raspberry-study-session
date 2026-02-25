from fastapi import FastAPI
import models
from database import engine
from routers import sessions

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(sessions.router)