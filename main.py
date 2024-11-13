import cv2
import numpy as np
import pickle
import cvzone
import subprocess
from ParkingSpace import PARKING_SPOT_HEIGHT,PARKING_SPOT_WIDTH

# Start image_save.py as a background process
image_save = subprocess.Popen(['python', 'image_save.py'])

# Load video path from configuration file
with open('config.txt', 'r') as config_file:
    video_path = config_file.read().strip()

# Check if the video path is not empty
if not video_path:
    print("Video path is not set.")
    exit()

#Load parkingspots
with open('carparkspots', 'rb') as f:
    pList = pickle.load(f)

width, height = 50, 25

#Load static image
static_img = cv2.imread('parkinglot_image.png')
if static_img is None:
    print("Error: Parking lot image missing.")
    exit()

# Resize static image if needed
display_img = cv2.resize(static_img, (800, 600))

#Load video feed
cap = cv2.VideoCapture(video_path)

def parkspace(img_pro):
    img_updated = static_img.copy()
    free_space = 0

    #Loop for each parking spot
    for pos in pList:
        x, y = pos
        img_crop = img_pro[y:y + PARKING_SPOT_HEIGHT, x:x + PARKING_SPOT_WIDTH]
        #cv2.rectangle(static_img, (x, y), (x + width, y + height), (0, 255, 0), 2)  # Draw green rectangle
        #cv2.imshow("Parking Spots", static_img)
        count = cv2.countNonZero(img_crop)


        if count < 750:
            color = (0, 255, 0) #green
            letter = "O"        # "O" for free spots
            free_space += 1
        else:
            color = (0, 0, 255) #red
            letter = "X"        # "X" for occupied

        # color = (255, 255, 0) #yellow

        # Draw the rectangle with the respective color
        cv2.rectangle(img_updated, (x, y), (x + PARKING_SPOT_WIDTH, y + PARKING_SPOT_HEIGHT), color, -1)

        # Place the letter inside the rectangle
        cv2.putText(img_updated, letter, (x + 10, y + PARKING_SPOT_HEIGHT - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Increase the font size for free space count display
    cvzone.putTextRect(img_updated, f'Free: {free_space}/{len(pList)}', (50, 25), scale=3,
                   thickness=4, offset=10, colorR=(0, 200, 0))

    return img_updated

#Main loop to process video
try:
    while True:
        success, img = cap.read()

        if not success:
            break

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
        img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        #_, img_threshold = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)
        img_median = cv2.medianBlur(img_threshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        img_dilate = cv2.dilate(img_median, kernel, iterations=1)

        # Debugging display for each step
        #cv2.imshow("Thresholded Image", img_threshold)
        #cv2.imshow("Dilated Image", img_dilate)  # Display the dilated image

        # Set windows as resizeable
        # cv2.namedWindow("Thresholded Image with Highlight Box", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Updated Parking Lot", cv2.WINDOW_NORMAL)

        # Resize images for display only
        img_threshold_resized = cv2.resize(img_threshold, (800, 600))
        img_updated = parkspace(img_dilate)
        img_updated_resized = cv2.resize(img_updated, (800, 600))

        #cv2.imshow("Thresholded Image with Highlight Box", img_threshold_resized)
        cv2.imshow("Updated Parking Lot", img_updated_resized)


        #cv2.rectangle(img_threshold, (x, y), (x + width, y + height), (0, 255, 0), 2)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

finally:
    #stop all processes
    image_save.terminate()
    cap.release()
    cv2.destroyAllWindows()