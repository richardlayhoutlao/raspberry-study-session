from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from service.study_log_service import StudylogService
from repository.study_log_repository import StudylogRepository
from schemas.study_log_schema import StudylogRequest
from config.database import get_db

db_dependency = Annotated[Session, Depends(get_db)]
router = APIRouter(tags=["Studylog"])
STUDYLOG_NOT_FOUND = "Studylog not found."


def get_studylog_service(db: Session = Depends(get_db)):
    repository = StudylogRepository(db)
    return StudylogService(repository)


@router.get("/studylogs", status_code=status.HTTP_200_OK)
def get_all_studylogs(service: StudylogService = Depends(get_studylog_service)):
    return service.get_all_studylogs()


@router.get("/studylog/{studylog_id}", status_code=status.HTTP_200_OK)
def get_studylog(studylog_id: str, service: StudylogService = Depends(get_studylog_service)):
    studylog = service.get_studylog_by_id(studylog_id)
    if not studylog:
        raise HTTPException(status_code=404, detail=STUDYLOG_NOT_FOUND)
    return studylog


@router.post("/studylog", status_code=status.HTTP_201_CREATED)
def create_studylog(request: StudylogRequest, service: StudylogService = Depends(get_studylog_service)):
    return service.create_studylog(request.model_dump())


@router.put("/studylog/{studylog_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_studylog(studylog_id: str, request: StudylogRequest, service: StudylogService = Depends(get_studylog_service)):
    updated_studylog = service.update_studylog(studylog_id, request.model_dump())
    if not updated_studylog:
        raise HTTPException(status_code=404, detail=STUDYLOG_NOT_FOUND)


@router.delete("/studylog/{studylog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_studylog(studylog_id: str, service: StudylogService = Depends(get_studylog_service)):
    success = service.delete_studylog(studylog_id)
    if not success:
        raise HTTPException(status_code=404, detail=STUDYLOG_NOT_FOUND)


@router.get("/get_client_config/{studylog_id}", status_code=status.HTTP_200_OK)
async def get_client_config(studylog_id: str, service: StudylogService = Depends(get_studylog_service)):
    result = service.get_client_config(studylog_id)
    if isinstance(result, JSONResponse):
        return result
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
