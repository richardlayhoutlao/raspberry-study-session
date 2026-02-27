import sys
from pathlib import Path
import pytest
from datetime import datetime

# Add parent directory to path so tests can import modules from root
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.study_log import Studylog
from utils import TestingSessionLocal


@pytest.fixture(autouse=True)
def seed_test_data():
    """Seed test data into the test database before each test."""
    db = TestingSessionLocal()
    
    # Clear existing data
    db.query(Studylog).delete()
    db.commit()
    
    # Create test records
    studylog_1 = Studylog(
        id="97983be2-98b7-11e7-90cf-082e5f28d836",
        date_time=datetime.fromisoformat("2021-01-10T13:37:17"),
        noise_score=45,
        light_score=300,
        temperature_score=22,
        focus_score=85
    )
    
    studylog_2 = Studylog(
        id="88888be2-98b7-11e7-90cf-082e5f28d444",
        date_time=datetime.fromisoformat("2024-05-01T08:30:00"),
        noise_score=30,
        light_score=450,
        temperature_score=24,
        focus_score=92
    )
    
    db.add(studylog_1)
    db.add(studylog_2)
    db.commit()
    
    yield
    
    # Cleanup after test
    db.query(Studylog).delete()
    db.commit()
    db.close()
