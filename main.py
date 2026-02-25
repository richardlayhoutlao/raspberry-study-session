from fastapi import FastAPI
from models.study_log import Studylog
from config.database import engine
from router import study_log

app = FastAPI()

Studylog.metadata.create_all(bind=engine)

app.include_router(study_log.router)