import cv2
import pickle
import os

from screen_util import fit_to_screen

# Define parking spot dimensions
PARKING_SPOT_WIDTH = 25
PARKING_SPOT_HEIGHT = 10

def load_parking_spots():
    # Load parking spots from a file, return an empty list if the file doesn't exist or is empty.
    try:
        with open('carparkspots', 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Failed to load parking spots due to an error: {e}")
        return []

def save_parking_spots(spots):
    # Save parking spots to a file.
    try:
        with open('carparkspots', 'wb') as f:
            pickle.dump(spots, f)
        print(f"Saved {len(spots)} parking spots.")
    except Exception as e:
        print(f"Error: {e}")

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

    pList = load_parking_spots()

    # Load the video and capture the first frame
    cap = cv2.VideoCapture(video_name)
    success, frame = cap.read()
    cap.release()

    if not success:
        print("Error: Could not load frame")
        return

    # Save the first frame as a reference image
    cv2.imwrite("parkinglot_image.png", frame)
    print("Saved first frame as parkinglot_image.png")

    while True:
        img_copy = frame.copy()

        # Draw rectangles over parking spots
        for pos in pList:
            cv2.rectangle(img_copy, pos, (pos[0] + PARKING_SPOT_WIDTH, pos[1] + PARKING_SPOT_HEIGHT), (255, 0, 255), 2)

        img_resized, scale = fit_to_screen("Parking Lot Editor", img_copy)

        # Set callback to add/remove parking spots
        cv2.setMouseCallback("Parking Lot Editor", click, param={"pList": pList, "scale": scale})
        cv2.imshow('Parking Lot Editor', img_resized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Save updated parking spots
    save_parking_spots(pList)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

