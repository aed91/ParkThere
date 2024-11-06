import sqlite3
from datetime import datetime

# Initialize or connect to SQLite database
def init_db():
    conn = sqlite3.connect("parkthere.db")
    cursor = conn.cursor()

    # Table for individual spot data
    cursor.execute('''CREATE TABLE IF NOT EXISTS SpotStatus (
                        spot_id INTEGER PRIMARY KEY,
                        x INTEGER NOT NULL,
                        y INTEGER NOT NULL,
                        status TEXT DEFAULT "free",
                        timestamp TEXT
                      )''')

    # Table for summary data
    cursor.execute('''CREATE TABLE IF NOT EXISTS SummaryStatus (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        available_count INTEGER DEFAULT 0,
                        unavailable_count INTEGER DEFAULT 0,
                        timestamp TEXT
                      )''')
    conn.commit()
    conn.close()

# Update spot-level data
def update_spot_status(spot_id, x, y, status):
    conn = sqlite3.connect("parkthere.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT OR REPLACE INTO SpotStatus (spot_id, x, y, status, timestamp)
                      VALUES (?, ?, ?, ?, ?)''', (spot_id, x, y, status, timestamp))
    conn.commit()
    conn.close()

# Update summary-level data
def update_summary_status(available, unavailable):
    conn = sqlite3.connect("parkthere.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO SummaryStatus (available_count, unavailable_count, timestamp) VALUES (?, ?, ?)",
                   (available, unavailable, timestamp))
    conn.commit()
    conn.close()

# Export data to a .txt file
def export_to_txt():
    conn = sqlite3.connect("parkthere.db")
    cursor = conn.cursor()

    # Fetch all spot-level data
    cursor.execute("SELECT * FROM SpotStatus")
    spot_data = cursor.fetchall()

    # Fetch summary-level data
    cursor.execute("SELECT * FROM SummaryStatus")
    summary_data = cursor.fetchall()

    conn.close()

    # Write data to a .txt file
    with open("parking_data.txt", "w") as file:
        file.write("Spot-Level Data:\n")
        file.write("spot_id\tx\ty\tstatus\ttimestamp\n")
        for row in spot_data:
            file.write("\t".join(map(str, row)) + "\n")

        file.write("\nSummary-Level Data:\n")
        file.write("id\tavailable_count\tunavailable_count\ttimestamp\n")
        for row in summary_data:
            file.write("\t".join(map(str, row)) + "\n")

    print("Data exported to parking_data.txt")
