import paho.mqtt.client as mqtt
import base64

# MQTT client configuration
mqtt_broker = 'localhost'
mqtt_port = 1883
mqtt_topic = 'image_topic'
mqtt_qos = 0


def on_message(client, userdata, msg):
    # Decode Base64-encoded image from MQTT message payload
    image_data = base64.b64decode(msg.payload)
    #Save image / recognize blabla


client = mqtt.Client()
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port)
client.subscribe(mqtt_topic, mqtt_qos)

while True:
    client.loop()