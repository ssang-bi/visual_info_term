import numpy as np
import cv2

def keyEvent(img):
    global mode
    
    key = cv2.waitKey(100)
    if key == ord('1'):
        cv2.destroyWindow("test")
        if mode == "Ellipse":
            mode = "NULL"
        else:
            mode = "Ellipse"
        cv2.imshow("test",img)
    if key == ord('2'):
        if mode == "Polygon":
            mode = "NULL"
        else:
            mode = "Polygon"
    
def showMode(img):
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 0, 0)
    cv2.putText(img, mode, (10, 40), font, 0.7, color, 2)
    cv2.imshow("test",img)


img = np.zeros((512, 512, 3), np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
position = (10, 450)
fontScale = 2
fontColor = (255, 255, 0)
cv2.putText(
    img, "Hello World!", position, font, fontScale, fontColor, 3, cv2.LINE_AA, True
)

while 

cv2.imshow("img", img)
cv2.waitKey(0)