import time
import cv2
import os

"""
Periodically reads an image and saves it to a new 
file in the specified directory.

Used for updating the image sent to the webpage.
"""

def save_image_timely(interval=10):
    # Base folder is the project root
    src_folder = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(src_folder, ".."))
    images_folder = os.path.join(project_root, "images")

    # Define input and output file paths
    input_image_path = os.path.join(images_folder, "parkinglot_image.png")
    output_image_path = os.path.join(images_folder, "update.png")

    while True:
        img = cv2.imread("parkinglot_image.png")
        print(f"Attempting to read image from: {input_image_path}")

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