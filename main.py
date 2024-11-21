
import cv2
import numpy as np
import pickle
import subprocess
from database_setup import insert_parking_data
from ParkingSpace import PARKING_SPOT_HEIGHT, PARKING_SPOT_WIDTH

# Start necessary processes
subprocess.Popen(['python', 'database_setup.py'])
subprocess.Popen(['python', 'api.py'])

# Load video path from configuration file
with open('config.txt', 'r') as config_file:
    video_path = config_file.read().strip()

# Check if the video path is not empty
if not video_path:
    print("Video path is not set.")
    exit()

# Load parking spots
with open('carparkspots', 'rb') as f:
    pList = pickle.load(f)

# Load static image
static_img = cv2.imread('parkinglot_image.png')
if static_img is None:
    print("Error: Parking lot image missing.")
    exit()

# Resize static image for display
display_img = cv2.resize(static_img, (800, 600))

# Load video feed
cap = cv2.VideoCapture(video_path)

def parkspace(img_pro):
    img_updated = static_img.copy()
    free_space = 0

    # Loop for each parking spot
    for index, pos in enumerate(pList):
        x, y = pos
        img_crop = img_pro[y:y + PARKING_SPOT_HEIGHT, x:x + PARKING_SPOT_WIDTH]
        count = cv2.countNonZero(img_crop)

        if count < 750:
            color = (0, 255, 0)  # green for free
            status = "free"
            free_space += 1
        else:
            color = (0, 0, 255)  # red for occupied
            status = "occupied"

        # Update parking spot data in the database
        spot_id = index + 1  # Spot ID based on index
        insert_parking_data(spot_id, status)

        cv2.rectangle(img_updated, (x, y), (x + PARKING_SPOT_WIDTH, y + PARKING_SPOT_HEIGHT), color, -1)

    cv2.putText(img_updated, f'Free: {free_space}/{len(pList)}', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return img_updated

try:
    while True:
        success, img = cap.read()

        if not success:
            break

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
        img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        img_median = cv2.medianBlur(img_threshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        img_dilate = cv2.dilate(img_median, kernel, iterations=1)

        img_updated = parkspace(img_dilate)
        cv2.imshow("Updated Parking Lot", img_updated)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
