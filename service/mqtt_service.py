import paho.mqtt.client as mqtt
import json
from datetime import datetime, timezone
from pydantic import ValidationError

from config.database import SessionLocal
from models.study_log import Studylog
from repository.study_log_repository import StudylogRepository
from schemas.study_log_schema import StudylogRequest

BROKER = "test.mosquitto.org"
TOPIC = "Studylog-Richard"

class MQTTSubscriber:
    def __init__(self, broker: str = BROKER, topic: str = TOPIC):
        self.broker = broker
        self.topic = topic
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            print(f"Connected to MQTT broker: {self.broker}")
            client.subscribe(self.topic)
            print(f"Subscribed to topic: {self.topic}")
        else:
            print(f"MQTT connection failed with reason code: {reason_code}")

    def _on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8", errors="replace")
        print(f"Received message on {message.topic}: {payload}")

        db = SessionLocal()
        try:
            payload_data = StudylogRequest.model_validate_json(payload)
            repository = StudylogRepository(db)
            studylog = Studylog(**payload_data.model_dump())
            created_studylog = repository.create(studylog)
            print(f"Saved studylog with id: {created_studylog.id}")
        except ValidationError as exc:
            print(f"Invalid payload for studylog: {exc}")
        except Exception as exc:
            print(f"Failed to save MQTT payload to DB: {exc}")
        finally:
            db.close()

    def start(self):
        self.client.connect(self.broker)
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()


mqtt_subscriber = MQTTSubscriber()
