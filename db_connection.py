import sqlite3

# SQLite database configuration
database_file = 'images.db'
table_name = 'images'
conn = sqlite3.connect(database_file)
c = conn.cursor()
c.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, image BLOB)')

def insert_image(image_data):
    # Insert image data into SQLite database
    c.execute(f'INSERT INTO {table_name} (image) VALUES (?)', (sqlite3.Binary(image_data),))
    conn.commit()
