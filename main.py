import cv2
import numpy as np
import pickle
import cvzone
import time
from database import init_db, update_spot_status, update_summary_status, export_to_txt

# Load parkingspots
with open('carparkspots', 'rb') as f:
    pList = pickle.load(f)

width, height = 100, 50

# Load static image
static_img = cv2.imread('ParkingLot.png')

if static_img is None:
    print("Error: Parking lot image missing.")
    exit()

# Load video feed
cap = cv2.VideoCapture('ParkingLot.mp4')

# Initialize the database once at the start
init_db()

# Track the last time the export was performed
last_export_time = time.time()

def parkspace(img_pro):
    img_updated = static_img.copy()
    free_space = 0

    # Loop for each parking spot
    for index, pos in enumerate(pList):
        x, y = pos
        img_crop = img_pro[y:y + height, x:x + width]
        count = cv2.countNonZero(img_crop)
        
        # Assign status based on pixel count
        if count < 900:
            color = (0, 255, 0)  # green
            status = "free"
            free_space += 1
        else:
            color = (0, 0, 255)  # red
            status = "occupied"
        
        # Update the database with each spot's status
        spot_id = index + 1  # Spot ID based on index in pList
        update_spot_status(spot_id, x, y, status)

        cv2.rectangle(img_updated, (x, y), (x + width, y + height), color, -1)

    # Update summary status in the database
    total_spots = len(pList)
    unavailable_space = total_spots - free_space
    update_summary_status(free_space, unavailable_space)

    cvzone.putTextRect(img_updated, f'Free: {free_space}/{total_spots}', (50, 50), scale=2,
                       thickness=3, offset=10, colorR=(0, 200, 0))

    return img_updated

# Main loop to process video
while True:
    success, img = cap.read()

    if not success:
        break

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 25, 16)
    img_median = cv2.medianBlur(img_threshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

    img_updated = parkspace(img_dilate)
    cv2.imshow("Updated Parking Lot", img_updated)

    # Check if 5 seconds have passed for data export
    if time.time() - last_export_time >= 5:
        export_to_txt()
        last_export_time = time.time()  # Reset the timer

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Final export when the program completes/terminated
export_to_txt()
