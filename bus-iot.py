import paho.mqtt.client as mqtt
from datetime import datetime
import json


def on_connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))
    client.subscribe("eventstream/raw")


def on_message(client, userdata, msg):
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


client = mqtt.Client(client_id="", clean_session=True, userdata=None)
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.mqttdashboard.com", 1883)

client.loop_forever()
