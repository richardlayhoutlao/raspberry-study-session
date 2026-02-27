import paho.mqtt.client as mqtt

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

    def start(self):
        self.client.connect(self.broker)
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()


mqtt_subscriber = MQTTSubscriber()
