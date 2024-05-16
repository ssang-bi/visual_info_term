import numpy as np
import cv2

nullImg = np.full((480, 640, 3), 255, np.uint8)
ellipseImg = np.full((480, 640, 3), 255, np.uint8)
polygonImg = np.full((480, 640, 3), 255, np.uint8)

cv2.putText(nullImg, "NULL", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
cv2.putText(ellipseImg, "Ellipse", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
cv2.putText(polygonImg, "Polygon", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

def setMode(key):
    global mode
    
    if key == ord('1'):
        if mode == "Ellipse":
            mode = "NULL"
            cv2.imshow("paint", nullImg)
        else:
            mode = "Ellipse"
            cv2.imshow("paint", ellipseImg)
    elif key == ord('2'):
        if mode == "Polygon":
            mode = "NULL"
            cv2.imshow("paint", nullImg)
        else:
            mode = "Polygon"
            cv2.imshow("paint", polygonImg)
            
            
mode = "NULL"    
cv2.imshow("paint", nullImg)

while True:
    key = cv2.waitKeyEx(100)
    if key == 27: break
    
    setMode(key)
    
cv2.destroyAllWindows()