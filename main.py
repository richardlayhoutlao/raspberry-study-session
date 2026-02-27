from fastapi import FastAPI
from models.study_log import Studylog
from config.database import engine
from router import study_log
from contextlib import asynccontextmanager
from service.mqtt_service import mqtt_subscriber


@asynccontextmanager
async def lifespan(app: FastAPI):
	mqtt_subscriber.start()
	try:
		yield
	finally:
		mqtt_subscriber.stop()


app = FastAPI(lifespan=lifespan)

Studylog.metadata.create_all(bind=engine)

app.include_router(study_log.router)