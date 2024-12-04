import sqlite3
import csv
import os
from datetime import datetime
import cv2
import numpy as np
import pickle
import cvzone
import time

# Constants for parking spot dimensions
PARKING_SPOT_WIDTH = 50
PARKING_SPOT_HEIGHT = 30

# Database file paths
MAIN_DB_PATH = "main_database.db"
API_DB_PATH = "api_database.db"
API_CSV_PATH = "api_data_export.csv"
MAIN_CSV_PATH = "main_data_export.csv"

# Create and initialize databases
def initialize_databases():
    # Main database
    conn = sqlite3.connect(MAIN_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS main_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            free_spots INTEGER,
            occupied_spots INTEGER,
            last_updated TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Main database initialized.")

    # API database (only one row of data)
    conn = sqlite3.connect(API_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_data (
            id INTEGER PRIMARY KEY,
            total_spots INTEGER,
            free_spots INTEGER,
            occupied_spots INTEGER,
            last_updated TEXT
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO api_data (id, total_spots, free_spots, occupied_spots, last_updated)
        VALUES (1, 0, 0, 0, ?)
    ''', (datetime.now().isoformat(),))
    conn.commit()
    conn.close()
    print("API database initialized.")

# Export API database to CSV
def export_api_to_csv():
    try:
        conn = sqlite3.connect(API_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM api_data")
        rows = cursor.fetchall()
        conn.close()

        # Overwrite the CSV file
        with open(API_CSV_PATH, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'total_spots', 'free_spots', 'occupied_spots', 'last_updated'])  # Header row
            writer.writerows(rows)
        print(f"API database successfully exported to {API_CSV_PATH}")
    except PermissionError:
        print(f"Error: CSV file {API_CSV_PATH} is open in another program. Please close it and try again.")
    except Exception as e:
        print(f"Error exporting API database to CSV: {e}")

# Export Main database to CSV
def export_main_to_csv():
    try:
        conn = sqlite3.connect(MAIN_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM main_data")
        rows = cursor.fetchall()
        conn.close()

        # Overwrite the CSV file
        with open(MAIN_CSV_PATH, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'free_spots', 'occupied_spots', 'last_updated'])  # Header row
            writer.writerows(rows)
        print(f"Main database successfully exported to {MAIN_CSV_PATH}")
    except PermissionError:
        print(f"Error: CSV file {MAIN_CSV_PATH} is open in another program. Please close it and try again.")
    except Exception as e:
        print(f"Error exporting Main database to CSV: {e}")

# Update both databases every 10 seconds
def update_databases(pList, free_space, occupied_space):
    print(f"Attempting to update databases at {datetime.now()}...")

    # Update Main Database (log history)
    try:
        conn_main = sqlite3.connect(MAIN_DB_PATH)
        cursor_main = conn_main.cursor()
        cursor_main.execute('''
            INSERT INTO main_data (free_spots, occupied_spots, last_updated)
            VALUES (?, ?, ?)
        ''', (free_space, occupied_space, datetime.now().isoformat()))
        conn_main.commit()
        conn_main.close()
        print(f"Main database updated: Free={free_space}, Occupied={occupied_space}")
    except Exception as e:
        print(f"Error updating main database: {e}")

    # Update API Database (overwrite single row with id=1)
    try:
        conn_api = sqlite3.connect(API_DB_PATH)
        cursor_api = conn_api.cursor()
        cursor_api.execute('''
            UPDATE api_data
            SET total_spots = ?,
                free_spots = ?,
                occupied_spots = ?,
                last_updated = ?
            WHERE id = 1
        ''', (len(pList), free_space, occupied_space, datetime.now().isoformat()))
        conn_api.commit()

        # Verify the update
        cursor_api.execute("SELECT * FROM api_data WHERE id = 1")
        updated_row = cursor_api.fetchone()
        conn_api.close()
        print(f"API database updated successfully: {updated_row}")
    except Exception as e:
        print(f"Error updating API database: {e}")

    # Export both databases to CSV files
    export_main_to_csv()
    export_api_to_csv()

# Process parking lot video feed
def process_parking_feed(video_name):
    # Load parking spots
    try:
        with open('carparkspots', 'rb') as f:
            pList = pickle.load(f)
    except FileNotFoundError:
        print("Error: Parking spots file not found at 'carparkspots'")
        return

    # Load static image
    static_img = cv2.imread('parkinglot_image.png')
    if static_img is None:
        print("Error: Parking lot image missing.")
        return

    # Load video feed
    cap = cv2.VideoCapture(video_name)
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_name}'")
        return

    last_update_time = time.time()

    def parkspace(img_pro):
        img_updated = static_img.copy()
        free_space = 0
        occupied_space = 0

        for pos in pList:
            x, y = pos
            img_crop = img_pro[y:y + PARKING_SPOT_HEIGHT, x:x + PARKING_SPOT_WIDTH]
            count = cv2.countNonZero(img_crop)

            if count < 100:
                color = (0, 255, 0)  # Green
                letter = "O"
                free_space += 1
            else:
                color = (0, 0, 255)  # Red
                letter = "X"
                occupied_space += 1

            cv2.rectangle(img_updated, (x, y), (x + PARKING_SPOT_WIDTH, y + PARKING_SPOT_HEIGHT), color, -1)
            cv2.putText(img_updated, letter, (x + 3, y + PARKING_SPOT_HEIGHT - 1),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cvzone.putTextRect(img_updated, f'Free: {free_space}/{len(pList)}', (50, 25), scale=3,
                           thickness=4, offset=10, colorR=(0, 200, 0))
        return img_updated, free_space, occupied_space

    try:
        while True:
            success, img = cap.read()
            if not success:
                break

            # Process parking spots
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
            img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
            img_median = cv2.medianBlur(img_threshold, 5)
            kernel = np.ones((3, 3), np.uint8)
            img_dilate = cv2.dilate(img_median, kernel, iterations=1)

            img_updated, free_space, occupied_space = parkspace(img_dilate)

            # Update databases and CSVs every 10 seconds
            current_time = time.time()
            if current_time - last_update_time >= 10:  # 10-second interval
                print(f"Updating databases and CSVs at {datetime.now()}...")
                update_databases(pList, free_space, occupied_space)
                last_update_time = current_time

            cv2.imshow("Updated Parking Lot", img_updated)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

# Main execution
if __name__ == "__main__":
    initialize_databases()

    # Ensure CSV files are created at startup
    export_api_to_csv()
    export_main_to_csv()

    # Prompt for video file input
    video_name = input("Enter input video file name: ").strip()
    process_parking_feed(video_name)
