import numpy as np
import cv2

drawing = False
ix, iy = (-1, -1)
color = (255, 0, 0)

def onMouse(event, x, y, flags, param):
    global ix, iy, drawing
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            center = ((ix + x) // 2, (iy + y) // 2)
            axis = ((x - ix) // 2, (y - iy) // 2)
            cv2.ellipse(param, center, axis, 0, 0, 360, color)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        center = ((ix + x) // 2, (iy + y) // 2)
        axis = ((x - ix) // 2, (y - iy) // 2)
        cv2.ellipse(param, center, axis, 0, 0, 360, color, 2)
        
def Brush():
    img = np.full((640, 480), 255, np.uint8)
    cv2.namedWindow("paint")
    cv2.setMouseCallback("paint", onMouse, param=img)
    
    while True:
        cv2.imshow("paint", img)
        
        key = cv2.waitKey(100)
        if key == 27:
            break
        
    cv2.destroyAllWindows()
    
    
Brush()