import paho.mqtt.client as mqtt
import base64
import sqlite3

# SQLite database configuration
database_file = 'images.db'
table_name = 'images'
conn = sqlite3.connect(database_file)
c = conn.cursor()
c.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, image BLOB)')

# MQTT client configuration
mqtt_broker = 'localhost'
mqtt_port = 1883
mqtt_topic = 'image_topic'
mqtt_qos = 0


def on_message(client, userdata, msg):
    # Decode Base64-encoded image from MQTT message payload
    image_data = base64.b64decode(msg.payload)
    #Save image / recognize blabla


    # Insert image data into SQLite database
    c.execute(f'INSERT INTO {table_name} (image) VALUES (?)', (sqlite3.Binary(image_data),))
    conn.commit()


client = mqtt.Client()
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port)
client.subscribe(mqtt_topic, mqtt_qos)

while True:
    client.loop()