import cv2
import pickle
import os

# Define parking spot dimensions
PARKING_SPOT_WIDTH = 125
PARKING_SPOT_HEIGHT = 50

# Dimensions for the display
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600


def load_parking_spots(filename):
    # Load parking spots from a file, return an empty list if the file doesn't exist or is empty.
    try:
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        else:
            print(f"File {filename} not found or empty. Starting with an empty list.")
            return []
    except Exception as e:
        print(f"Failed to load parking spots due to an error: {e}")
        return []


def save_parking_spots(filename, spots):
    # Save parking spots to a file.
    with open(filename, 'wb') as f:
        pickle.dump(spots, f)
    print(f"Saved {len(spots)} parking spots to {filename}.")


def click(event, x, y, flags, pList):
    # Handle mouse clicks to add or remove parking spots.
    if event == cv2.EVENT_LBUTTONDOWN:
        pList.append((x, y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(pList):
            x1, y1 = pos
            if x1 < x < x1 + PARKING_SPOT_WIDTH and y1 < y < y1 + PARKING_SPOT_HEIGHT:
                pList.pop(i)
                break


def main():
    filename = 'carparkspots'
    pList = load_parking_spots(filename)
    video_path = 'parking_lot_video full.avi'

    # Capture first frame of video
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    cap.release()

    if not success:
        print("Error: Could not load frame")
        return

    # Save the captured frame as a static image for reference in other scripts
    cv2.imwrite("parkinglot_image.png", frame)

    # Display frame for spot selection
    cv2.namedWindow('Parking Lot Editor')
    cv2.setMouseCallback('Parking Lot Editor', click, pList)

    while True:
        img_copy = frame.copy()

        # Draw rectangles for all selected parking spots
        for pos in pList:
            cv2.rectangle(img_copy, pos, (pos[0] + PARKING_SPOT_WIDTH, pos[1] + PARKING_SPOT_HEIGHT), (255, 0, 255), 2)

        cv2.imshow('Parking Lot Editor', img_copy)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Save the selected parking spots
    save_parking_spots(filename, pList)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
