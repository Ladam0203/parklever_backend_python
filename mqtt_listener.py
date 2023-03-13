import paho.mqtt.client as mqtt
import license_plate_recognition as lpr
import db_connection as db
import re

# MQTT client configuration
mqtt_broker = 'mqtt.flespi.io'
mqtt_port = 1883
mqtt_topic = 'parklever/1/1'
mqtt_qos = 0
token = "SwoZQpQ9og9iDXB4a6gcI6cZI9tYkiW2C9PioufAyfI107T0303AW3ns0HfbN11f"


def on_message(client, userdata, msg):
    topic = msg.topic

    base64_image = msg.payload
    print(base64_image)
    plate_num = lpr.recognize(base64_image)
    db.insert_log(topic, base64_image, plate_num)

    print(db.select_last_log())
    print(db.get_parking_status())
    if plate_num is not None:
        client.publish(topic + '/response', 1)
    else:
        client.publish(topic + '/response', 0)


client = mqtt.Client("parklever_backend_python")
client.username_pw_set(token, token)
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port)
client.subscribe(mqtt_topic, mqtt_qos)

print("Listening to MQTT messages...")

while True:
    client.loop()
