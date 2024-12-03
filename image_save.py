import time
import cv2
import os

"""
Periodically reads an image and saves it to a new 
file in the specified directory.

Used for updating the image sent to the webpage.
"""

def save_image_timely(interval=10):
    while True:
        img = cv2.imread("parkinglot_image.png")
        if img is not None:
            filename = "update.png"
            cv2.imwrite(filename, img)
            print(f"Saved {filename}")
        else:
            print("Error: Unable to load image.")

        #Save again in seconds
        time.sleep(interval)

# Start the save process
if __name__ == "__main__":
    save_image_timely(interval=10)