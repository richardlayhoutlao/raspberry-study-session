from sqlalchemy.orm import Session
from models.study_log import Studylog
from datetime import datetime

class StudylogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Studylog).all()

    def get_by_id(self, id: str):
        return self.db.query(Studylog).filter(Studylog.id == id).first()

    def create(self, studylog: Studylog):
        self.db.add(studylog)
        self.db.commit()
        self.db.refresh(studylog)
        return studylog

    def update(self, id: str, updated_data: dict):
        studylog = self.get_by_id(id)
        if studylog:
            for field, value in updated_data.items():
                setattr(studylog, field, value)
            self.db.commit()
            self.db.refresh(studylog)
            return studylog
        return None

    def delete(self, id: str):
        studylog = self.get_by_id(id)
        if studylog:
            self.db.delete(studylog)
            self.db.commit()
            return True
        return False