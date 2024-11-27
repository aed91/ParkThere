import cv2
import pickle
import os

from screen_util import fit_to_screen

# Define parking spot dimensions
PARKING_SPOT_WIDTH = 25
PARKING_SPOT_HEIGHT = 10

# Paths relative to the src folder
BASE_DIR = os.path.dirname(__file__)  # src directory
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
IMAGES_DIR = os.path.join(BASE_DIR, "..", "images")
VIDEOS_DIR = os.path.join(BASE_DIR, "..", "videos")

# Ensure necessary directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

def load_parking_spots(filename):
    # Load parking spots from a file, return an empty list if the file doesn't exist or is empty.
    try:
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        else:
            print(f"File {filename} not found or empty. Starting with an empty list.")
            return []
    except Exception as e:
        print(f"Failed to load parking spots due to an error: {e}")
        return []


def save_parking_spots(filename, spots):
    # Save parking spots to a file.
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'wb') as f:
        pickle.dump(spots, f)
    print(f"Saved {len(spots)} parking spots to {filename}.")


def click(event, x, y, flags, param):
    pList, scale = param["pList"], param["scale"]

    # Handle mouse clicks to add or remove parking spots.
    if event == cv2.EVENT_LBUTTONDOWN:
        # Map resized coordinates to original
        original_x = int(x / scale)
        original_y = int(y / scale)
        pList.append((original_x, original_y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        # Map resized coordinates to original and check for removal
        original_x = int(x / scale)
        original_y = int(y / scale)
        for i, pos in enumerate(pList):
            x1, y1 = pos
            if x1 < original_x < x1 + PARKING_SPOT_WIDTH and y1 < original_y < y1 + PARKING_SPOT_HEIGHT:
                pList.pop(i)
                break


def main():
    config_path = os.path.join(DATA_DIR, 'config.txt')

    # Check if the config file exists, if not create it
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            video_name = config_file.read().strip()

            # Ask user about video source
            use_existing = input(f"Current input source is '{video_name}'. Use this? (y/n):").lower()
            if use_existing != 'y':
                video_name = input("Enter new input file name: ")
                with open(config_path, 'w') as config_file:
                    config_file.write(video_name)

    else:
        video_name = input("Enter input: ")
        with open(config_path, 'w') as config_file:
            config_file.write(video_name)

    # Debug: Print the resolved video path
    video_path = os.path.join(VIDEOS_DIR, video_name)
    print(f"Trying to load video from: {video_path}")

    filename = 'carparkspots'
    pList = load_parking_spots(filename)

    # Capture first frame of video
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    cap.release()

    if not success:
        print("Error: Could not load frame")
        return

    # Save the captured frame as a static image for reference in other scripts
    parking_image_path = os.path.join(IMAGES_DIR, "parkinglot_image.png")
    cv2.imwrite(parking_image_path, frame)
    print(f"Saved first frame as {parking_image_path}")

    while True:
        img_copy = frame.copy()

        # Draw rectangles for all selected parking spots
        for pos in pList:
            cv2.rectangle(img_copy, pos, (pos[0] + PARKING_SPOT_WIDTH, pos[1] + PARKING_SPOT_HEIGHT), (255, 0, 255), 2)

        # Dynamically resize image for display
        img_resized, scale = fit_to_screen("Parking Lot Editor", img_copy)

        cv2.setMouseCallback("Parking Lot Editor", click, param={"pList": pList, "scale": scale})
        cv2.imshow('Parking Lot Editor', img_resized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Save the selected parking spots
    save_parking_spots(filename, pList)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
