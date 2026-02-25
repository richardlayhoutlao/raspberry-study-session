from fastapi import status
from repository.study_log_repository import StudylogRepository
from models.study_log import Studylog
from datetime import datetime
import pytz


class StudylogService:
    def __init__(self, repository: StudylogRepository):
        self.repository = repository
        self.timezone = pytz.timezone('America/New_York')

    def get_all_studylogs(self):
        return self.repository.get_all()

    def get_studylog_by_id(self, studylog_id: str):
        return self.repository.get_by_id(studylog_id)

    def create_studylog(self, studylog_data: dict):
        studylog = Studylog(**studylog_data)
        current_time = datetime.now(self.timezone)
        studylog.created = current_time
        studylog.modified = current_time
        return self.repository.create(studylog)

    def update_studylog(self, studylog_id: str, updated_data: dict):
        updated_data['modified'] = datetime.now(self.timezone)
        return self.repository.update(studylog_id, updated_data)

    def delete_studylog(self, studylog_id: str):
        return self.repository.delete(studylog_id)