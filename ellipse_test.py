import numpy as np
import cv2
import math

# 타원 소스
drawing = False
ix, iy = (-1, -1)
color = (0, 0, 0)

def onMouse(event, x, y, flags, param):
    global ix, iy, drawing
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            center = ((ix + x) // 2, (iy + y) // 2)
            axis = (abs((ix - x) // 2), abs((iy - y) // 2))
            tmpimg = param.copy()
            cv2.ellipse(tmpimg, center, axis, 0, 0, 360, color, 2)
            cv2.imshow("paint", tmpimg)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        center = ((ix + x) // 2, (iy + y) // 2)
        axis = (abs((ix - x) // 2), abs((iy - y) // 2))
        cv2.ellipse(param, center, axis, 0, 0, 360, color, 2)
        cv2.imshow("paint", param)
        
def Brush():
    img = np.full((480, 640), 255, np.uint8)
    cv2.namedWindow("paint")
    cv2.setMouseCallback("paint", onMouse, param=img)
    cv2.imshow("paint", img)
    
    while True:
        
        key = cv2.waitKey(100)
        if key == 27:
            break
        
    cv2.destroyAllWindows()
    
    
Brush()