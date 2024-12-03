import cv2
import numpy as np
import pickle
import cvzone
import subprocess
import os

"""Detect whether an object is in a designated spot"""

from ParkingSpace import PARKING_SPOT_HEIGHT, PARKING_SPOT_WIDTH
from screen_util import fit_to_screen

# Start image_save.py as a background process
image_save = subprocess.Popen(['python', 'image_save.py'])

# Check if config file exists to get the last used video file
last_used_video = None
if os.path.exists('config.txt'):
    with open('config.txt', 'r') as config_file:
        last_used_video = config_file.read().strip()

# Prompt the user to reuse the last video file or input a new one
if last_used_video:
    use_last = input(f"Do you want to use the last video file '{last_used_video}'? (y/n): ").strip().lower()
    if use_last == 'y':
        video_name = last_used_video
    else:
        video_name = input("Enter input file name: ").strip()
else:
    video_name = input("Enter input file name: ").strip()

# Save the chosen video file name to config.txt for future use
with open('config.txt', 'w') as config_file:
    config_file.write(video_name)

# Load parking spots
try:
    with open('carparkspots', 'rb') as f:
        pList = pickle.load(f)
except FileNotFoundError:
    print("Error: Parking spots file not found at 'carparkspots'")
    exit()

# Load static image
static_img = cv2.imread('parkinglot_image.png')
if static_img is None:
    print("Error: Parking lot image missing.")
    exit()

# Load video feed
cap = cv2.VideoCapture(video_name)
if not cap.isOpened():
    print(f"Error: Could not open video file '{video_name}'")
    exit()

def parkspace(img_pro):
    img_updated = static_img.copy()
    free_space = 0
    occupied_space = 0

    # Loop for each parking spot
    for pos in pList:
        x, y = pos
        img_crop = img_pro[y:y + PARKING_SPOT_HEIGHT, x:x + PARKING_SPOT_WIDTH]
        count = cv2.countNonZero(img_crop)

        if count < 100:
            color = (0, 255, 0)  # Green
            letter = "o"         # "O" for free spots
            free_space += 1
        else:
            color = (0, 0, 255)  # Red
            letter = "x"         # "X" for occupied
            occupied_space += 1

        # Draw the rectangle with the respective color
        cv2.rectangle(img_updated, (x, y), (x + PARKING_SPOT_WIDTH, y + PARKING_SPOT_HEIGHT), color, -1)

        # Place the letter inside the rectangle
        cv2.putText(img_updated, letter, (x + 3, y + PARKING_SPOT_HEIGHT - 1),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Increase the font size for free space count display
    cvzone.putTextRect(img_updated, f'Free: {free_space}/{len(pList)}', (50, 25), scale=3,
                       thickness=4, offset=10, colorR=(0, 200, 0))

    return img_updated, free_space, occupied_space

# Main loop to process video
try:
    while True:
        success, img = cap.read()

        if not success:
            break

        # Image processing steps
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
        img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        img_median = cv2.medianBlur(img_threshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        img_dilate = cv2.dilate(img_median, kernel, iterations=1)

        img_updated, free_space, occupied_space = parkspace(img_dilate)

        # Save the updated image
        cv2.imwrite("processed_image.png", img_updated)

        # Resize for display and show the updated parking lot image
        image_resized, scale = fit_to_screen("Updated Parking Lot", img_updated)
        cv2.imshow("Updated Parking Lot", image_resized)

        # Press 'q' to exit
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

finally:
    # Stop all processes
    image_save.terminate()
    cap.release()
    cv2.destroyAllWindows()
