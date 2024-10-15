import cv2
import pickle


try:
    with open('carparkspots', 'rb') as f:
        pList = pickle.load(f)
except FileNotFoundError:
    pList = []

width, height = 100, 50

# add AI for parking spot detection

# Mouse clicks
def click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        pList.append((x,y))

    if event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(pList):
            x1,y1 = pos
            if x1<x<x1+width and y1<y<y1+height:
                pList.pop(i)
                break

    # Save updated parking spots to file
    with open('carparkspots', 'wb') as f:
        pickle.dump(pList, f)

while True:
    img = cv2.imread('parkinglot.png')

    if img is None:
        print("Error: Image not found!")
        break

    # Draw rectangle for each parking spot
    for pos in pList:
        cv2.rectangle(img, pos, (pos[0]+width,pos[1]+height), (255, 0, 255), 1)

    cv2.imshow('img', img)
    cv2.setMouseCallback('img', click)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()