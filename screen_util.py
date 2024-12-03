import cv2
import screeninfo

""" Adjust the program size to fit on screen."""

def fit_to_screen(window_name, image, margin=50):
    # Get screen dimensions
    screen = screeninfo.get_monitors()[0]
    screen_width, screen_height = screen.width, screen.height

    # Account for margin
    screen_width -= margin
    screen_height -= margin

    # Get image dimensions
    img_height, img_width = image.shape[:2]

    # Scale image to fit screen if needed
    scale_width = screen_width / img_width
    scale_height = screen_height / img_height
    scale = min(scale_width, scale_height)

    new_width = int(img_width * scale)
    new_height = int(img_height * scale)

    resized_image = cv2.resize(image, (new_width, new_height))

    # Create a resizable OpenCV window
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, new_width, new_height)

    return resized_image, scale
