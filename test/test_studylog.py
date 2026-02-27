from main import app
from config.database import get_db
from fastapi import status
from utils.stats_summary import *
from models.study_log import Studylog

app.dependency_overrides[get_db] = override_get_db

studylog_1 = {
    "id": "97983be2-98b7-11e7-90cf-082e5f28d836",
    "date_time": "2021-01-10T13:37:17",
    "sound_score": 45,
    "light_score": 300,
    "temperature_score": 22,
    "focus_score": 85,
    "score": 85,
    "is_uncomfortable": False,
    "reasons": []
}

studylog_2 = {
    "id": "88888be2-98b7-11e7-90cf-082e5f28d444",
    "date_time": "2024-05-01T08:30:00",
    "sound_score": 30,
    "light_score": 450,
    "temperature_score": 24,
    "focus_score": 92,
    "score": 92,
    "is_uncomfortable": False,
    "reasons": []
}

request_data = {
    "date_time": "2021-01-20T13:37:17",
    "sound_score": 50,
    "light_score": 350,
    "temperature_score": 23,
    "focus_score": 80,
    "score": 80,
    "is_uncomfortable": False,
    "reasons": []
}

updated_request_data = {
    "date_time": "2021-01-20T15:00:00",
    "sound_score": 40,
    "light_score": 400,
    "temperature_score": 25,
    "focus_score": 88,
    "score": 88,
    "is_uncomfortable": False,
    "reasons": []
}


def test_read_all_studylogs():
    response = client.get("/studylogs")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [studylog_1, studylog_2]


def test_read_studylog_1():
    response = client.get(f"/studylog/{studylog_1['id']}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == studylog_1


def test_read_studylog_2():
    response = client.get(f"/studylog/{studylog_2['id']}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == studylog_2


def test_read_one_studylog_not_found():
    response = client.get("/studylog/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Studylog not found.'}


def test_create_studylog():
    response = client.post('/studylog', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    data_created: Studylog = db.query(Studylog).filter(
        Studylog.sound_score == request_data["sound_score"],
        Studylog.light_score == request_data["light_score"],
        Studylog.temperature_score == request_data["temperature_score"],
        Studylog.focus_score == request_data["focus_score"]
    ).first()
    assert len(db.query(Studylog).all()) == 3
    assert data_created.sound_score == request_data["sound_score"]
    assert data_created.light_score == request_data["light_score"]
    assert data_created.temperature_score == request_data["temperature_score"]
    client.delete(f'/studylog/{data_created.id}')


def test_update_studylog():
    client.post('/studylog', json=request_data)
    db = TestingSessionLocal()
    data_created: Studylog = db.query(Studylog).filter(
        Studylog.sound_score == request_data["sound_score"],
        Studylog.light_score == request_data["light_score"],
        Studylog.temperature_score == request_data["temperature_score"],
        Studylog.focus_score == request_data["focus_score"]
    ).first()

    update_response = client.put(f'/studylog/{data_created.id}', json=updated_request_data)
    db.close()
    
    # Create a new session to see the committed changes
    db = TestingSessionLocal()
    data_updated: Studylog = db.query(Studylog).filter(Studylog.id == data_created.id).first()
    assert update_response.status_code == 204
    assert data_updated.sound_score == updated_request_data["sound_score"]
    assert data_updated.light_score == updated_request_data["light_score"]
    assert data_updated.temperature_score == updated_request_data["temperature_score"]
    assert data_updated.focus_score == updated_request_data["focus_score"]
    client.delete(f'/studylog/{data_created.id}')


def test_update_studylog_not_found():
    response = client.put('/studylog/999', json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Studylog not found.'}


def test_delete_studylog():
    client.post('/studylog', json=request_data)
    db = TestingSessionLocal()

    data_created: Studylog = db.query(Studylog).filter(
        Studylog.sound_score == request_data["sound_score"],
        Studylog.light_score == request_data["light_score"],
        Studylog.temperature_score == request_data["temperature_score"],
        Studylog.focus_score == request_data["focus_score"]
    ).first()
    assert len(db.query(Studylog).all()) == 3
    delete_response = client.delete(f'/studylog/{data_created.id}')
    assert delete_response.status_code == 204

    deleted_data = db.query(Studylog).filter(Studylog.id == data_created.id).first()
    assert deleted_data is None


def test_delete_studylog_not_found():
    response = client.delete('/studylog/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Studylog not found.'}
