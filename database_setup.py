import sqlite3
from datetime import datetime
import pickle

# Connect to or create the SQLite database
conn = sqlite3.connect(r'C:\Users\YourUsername\Desktop\project_folder\parking_data.db')
cursor = conn.cursor()

# Create the ParkingSpots table if it doesn’t exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ParkingSpots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        spot_number INTEGER,
        status TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# Load parking spots from the pickle file created by main.py
with open('carparkspots', 'rb') as f:
    pList = pickle.load(f)

# Function to insert parking spot data into the database
def insert_parking_data(spot_number, status):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO ParkingSpots (spot_number, status, timestamp)
        VALUES (?, ?, ?)
    ''', (spot_number, status, timestamp))
    conn.commit()

# Example Usage: Loop through loaded parking spots and set status to 'Unknown'
# (Replace 'Unknown' with real statuses if available)
for index, _ in enumerate(pList):
    insert_parking_data(index + 1, 'Unknown')  # Replace 'Unknown' as needed

# Close the database connection
conn.close()
