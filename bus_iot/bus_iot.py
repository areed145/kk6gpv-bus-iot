import paho.mqtt.client as mqtt
from datetime import datetime
import json


class BusIot:
    """Class that listens for new IoT observations"""

    def on_connect(self, client, userdata, flags, rc):
        """
        Subscribe to MQTT eventstream
        """
        print("Connected with result code" + str(rc))
        client.subscribe("eventstream/raw")

    def on_message(self, client, userdata, msg):
        """
        Parse MQTT message
        """
        message = msg.payload.decode("utf-8")
        message = json.loads(message)
        ins = message["event_data"]["new_state"]
        msg = {}
        msg["type"] = "iot"
        msg["timestamp"] = datetime.utcnow().isoformat()
        msg["sensor"] = ins["entity_id"]
        msg["state"] = ins["state"]
        msg["uom"] = ins["attributes"]["unit_of_measurement"]
        try:
            client.publish(
                "kk6gpv_bus/iot/" + str(msg["sensor"]),
                json.dumps(msg),
                retain=True,
            )
        except Exception:
            pass

    def run(self):
        self.client = mqtt.Client(
            client_id="kk6gpv-bus-iot", clean_session=False
        )
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("broker.mqttdashboard.com", 1883)
        self.client.loop_forever()


if __name__ == "__main__":
    bus = BusIot()
    bus.run()
