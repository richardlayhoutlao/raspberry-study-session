import paho.mqtt.client as mqtt
from pydantic import ValidationError
from config.database import SessionLocal
from models.study_log import Studylog
from repository.study_log_repository import StudylogRepository
from schemas.study_log_schema import StudylogRequest
import time
import ast

from utils.ai_environment_feedback import evaluate_batch

BROKER = "test.mosquitto.org"
TOPIC = "Studylog-Richard"


class MQTTSubscriber:
    def __init__(self, broker: str = BROKER, topic: str = TOPIC):
        self.broker = broker
        self.topic = topic
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self._last_2min_print = 0.0

    def _print_ai_feedback(self, db):
        now = time.time()
        if now - self._last_2min_print < 2 * 60:
            return

        last_30_studylogs = (
            db.query(Studylog)
            .order_by(Studylog.id.desc())
            .limit(30)
            .all()
        )

        logs_list = [
            {c.name: getattr(row, c.name) for c in row.__table__.columns}
            for row in last_30_studylogs
        ]

        if logs_list:
            try:
                feedback = evaluate_batch(logs_list)
                print("-------------- AI Feedback --------------")
                print(feedback)
                print("-------------- AI Feedback --------------")
            except Exception as exc:
                print(f"Failed to generate AI feedback: {exc}")

        self._last_2min_print = now

    def _save_payload_studylog(self, db, message):
        payload = message.payload.decode("utf-8", errors="replace")
        print(f"{payload}")

        try:
            payload_data = StudylogRequest.model_validate_json(payload)
        except ValidationError as exc:
            if "json_invalid" not in str(exc):
                raise

            parsed_payload = ast.literal_eval(payload)
            if not isinstance(parsed_payload, dict):
                raise
            payload_data = StudylogRequest.model_validate(parsed_payload)

        repository = StudylogRepository(db)
        studylog = Studylog(**payload_data.model_dump())
        repository.create(studylog)

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            print(f"Connected to MQTT broker: {self.broker}")
            client.subscribe(self.topic)
            print(f"Subscribed to topic: {self.topic}")
        else:
            print(f"MQTT connection failed with reason code: {reason_code}")

    def _on_message(self, client, userdata, message):
        db = SessionLocal()
        try:
            self._print_ai_feedback(db)
            self._save_payload_studylog(db, message)

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
