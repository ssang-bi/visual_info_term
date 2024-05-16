import numpy as np
import cv2
import math

drawing = False
ix, iy = (-1, -1)
color = (0, 0, 0)
count = 0
pt = list()

def onMouse(event, x, y, flags, param):
    global ix, iy, drawing, count, pt
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing:
            if count > 2:
                if calcLen(x, y, ix, iy) <= 20:
                    cv2.line(param, pt[count - 1], pt[0], color)
                    count = -1
                    pt.clear()
                    drawing = False
                else: 
                    pt.append((x, y))
                    cv2.circle(param, (x, y), 1, color)
                    cv2.line(param, pt[count - 1], pt[count], color)
            else:
                pt.append((x, y))
                cv2.circle(param, (x, y), 1, color)
                cv2.line(param, pt[count - 1], pt[count], color)
        else:
            ix, iy = x, y
            pt.append((ix, iy))
            # cv2.circle(white_canvas, (centerX, centerY), r, black)
            cv2.circle(param, (ix, iy), 1, color)
            drawing = True
        
        count += 1
        print(count)
        print(drawing)
        cv2.imshow("paint", param)
    
def calcLen(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    result = math.sqrt(pow(dx,2) + pow(dy, 2))
    return result

def calcRad(x, y, count):
    vx1, vy1 = ix - pt[count - 1][0], iy - pt[count - 1][1]
    vx2, vy2 = x - pt[count - 1][0], y - pt[count - 1][1]
    vx3, vy3 = x - ix, y - iy

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