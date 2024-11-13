import time
import cv2

def save_image_timely():
    while True:
        img = cv2.imread("parkinglot_image.png")

        if img is not None:
            filename = "update.png"
            cv2.imwrite(filename, img)
            print(f"Saved {filename}")
        else:
            print("Error: Unable to load image.")

        #Save again in seconds
        time.sleep(10)

# Start the save process
save_image_timely()