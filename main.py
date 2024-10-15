import cv2
import numpy as np
import pickle
import cvzone

#Load parkingspots
with open('carparkspots', 'rb') as f:
    pList = pickle.load(f)

width, height = 100, 50

#Load static image
static_img = cv2.imread('ParkingLot.png')

if static_img is None:
    print("Error: Parking lot image missing.")
    exit()

#Load video feed
cap = cv2.VideoCapture('ParkingLot.mp4')

def parkspace(img_pro):
    img_updated = static_img.copy()
    free_space = 0

    #Loop for each parking spot
    for pos in pList:
        x, y = pos
        img_crop = img_pro[y:y + height, x:x + width]
        count = cv2.countNonZero(img_crop)

        if count < 900:
            color = (0, 255, 0) #green
            free_space += 1
        else:
            color = (0, 0, 255) #red

        # color = (255, 255, 0) #yellow

        cv2.rectangle(img_updated, (x, y), (x + width, y + height), color, -1)

    cvzone.putTextRect(img_updated, f'Free: {free_space}/{len(pList)}', (50, 50), scale=2,
                   thickness=3, offset=10, colorR=(0, 200, 0))

    return img_updated

#Main loop to process video
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

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


