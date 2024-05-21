import numpy as np
import cv2

nullImg = cv2.imread("input.jpg")
nullImg = cv2.resize(nullImg, (640, 480))
ellipseImg = nullImg.copy() # 이미지 파일 및 크기 자체는 NULL mode와 같음
polygonImg = nullImg.copy()

cv2.putText(nullImg, "NULL", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)     # 각각의 mode를 좌측 상단에 출력
cv2.putText(ellipseImg, "Ellipse", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
cv2.putText(polygonImg, "Polygon", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

def setMode(key):   # mode(NULL, Ellipse, Polygon) 설정 키
    global mode
    
    if key == ord('1'):
        if mode == "Ellipse":   # 이미 Ellipse mode인 경우 NULL mode로 전환
            mode = "NULL"
            cv2.imshow("paint", nullImg)
        else:
            mode = "Ellipse"    # Ellipse mode가 아닌 경우 Ellipse mode로 전환
            cv2.imshow("paint", ellipseImg)
    elif key == ord('2'):
        if mode == "Polygon":   # 이미 Polygon mode인 경우 NULL mode로 전환
            mode = "NULL"
            cv2.imshow("paint", nullImg)
        else:
            mode = "Polygon"    # Polygon mode가 아닌 경우 Polygon mode로 전환
            cv2.imshow("paint", polygonImg)
            
            
mode = "NULL"    
cv2.imshow("paint", nullImg)

while True:
    key = cv2.waitKeyEx(100)
    if key == 27: break
    
    setMode(key)
    
cv2.destroyAllWindows()