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
c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT NOT NULL, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, image BLOB NOT NULL, plate_num TEXT)")

def insert_log(topic, image_base64, plate_num):
    # Encode image data as base64

    # Insert record into SQLite database
    c.execute(f"INSERT INTO {table_name} (topic, timestamp, image, plate_num) VALUES (?, CURRENT_TIMESTAMP, ?, ?)", (topic, image_base64, plate_num))
    conn.commit()

def select_last_log():
    # Select last record from SQLite database
    c.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1")
    return c.fetchone()


def get_parking_status():
    # Display number of cars parking currently, number of cars parked (came and left) in total
    c.execute(f"SELECT plate_num, COUNT(*) FROM {table_name} WHERE plate_num IS NOT NULL GROUP BY plate_num")
    log_counts = c.fetchall()
    num_currently_parking = sum(1 for count in log_counts if count[1] % 2 == 1)
    num_total_parked = sum(1 for count in log_counts if count[1] % 2 == 0)

    return f"Parking: {num_currently_parking} Total finished parkings: {num_total_parked}"

