import sqlite3
import base64

# SQLite database configuration
database_file = 'parklever.db'
table_name = 'logs'

conn = sqlite3.connect(database_file)
c = conn.cursor()

# Drop table if exists
c.execute(f"DROP TABLE IF EXISTS {table_name}")
# Create table if not exists
c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT NOT NULL, image BLOB NOT NULL, plate_num TEXT)")

def insert_log(topic, image_base64, plate_num=None):
    # Encode image data as base64

    # Insert record into SQLite database
    c.execute(f"INSERT INTO {table_name} (topic, image, plate_num) VALUES (?, ?, ?)", (topic, image_base64, plate_num))
    conn.commit()

def select_last_log():
    # Select last record from SQLite database
    c.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1")
    return c.fetchone()
