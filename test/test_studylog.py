from main import app
from config.database import get_db
from fastapi import status
from utils import *
from models.study_log import Studylog

app.dependency_overrides[get_db] = override_get_db

studylog_1 = {
    "id": "97983be2-98b7-11e7-90cf-082e5f28d836",
    "date_time": "2021-01-10T13:37:17",
    "avg_noise": 45,
    "avg_light": 300,
    "focus_score": 85
}

studylog_2 = {
    "id": "88888be2-98b7-11e7-90cf-082e5f28d444",
    "date_time": "2024-05-01T08:30:00",
    "avg_noise": 30,
    "avg_light": 450,
    "focus_score": 92
}

request_data = {
    "date_time": "2021-01-20T13:37:17",
    "avg_noise": 50,
    "avg_light": 350,
    "focus_score": 80
}

updated_request_data = {
    "date_time": "2021-01-20T15:00:00",
    "avg_noise": 40,
    "avg_light": 400,
    "focus_score": 88
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
        Studylog.avg_noise == request_data["avg_noise"],
        Studylog.avg_light == request_data["avg_light"],
        Studylog.focus_score == request_data["focus_score"]
    ).first()
    assert len(db.query(Studylog).all()) == 3
    assert data_created.avg_noise == request_data["avg_noise"]
    assert data_created.avg_light == request_data["avg_light"]
    assert data_created.focus_score == request_data["focus_score"]
    client.delete(f'/studylog/{data_created.id}')


def test_update_studylog():
    client.post('/studylog', json=request_data)
    db = TestingSessionLocal()
    data_created: Studylog = db.query(Studylog).filter(
        Studylog.avg_noise == request_data["avg_noise"],
        Studylog.avg_light == request_data["avg_light"],
        Studylog.focus_score == request_data["focus_score"]
    ).first()

    update_response = client.put(f'/studylog/{data_created.id}', json=updated_request_data)
    db.close()
    
    # Create a new session to see the committed changes
    db = TestingSessionLocal()
    data_updated: Studylog = db.query(Studylog).filter(Studylog.id == data_created.id).first()
    assert update_response.status_code == 204
    assert data_updated.avg_noise == updated_request_data["avg_noise"]
    assert data_updated.avg_light == updated_request_data["avg_light"]
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
        Studylog.avg_noise == request_data["avg_noise"],
        Studylog.avg_light == request_data["avg_light"],
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
