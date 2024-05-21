import numpy as np
import cv2
import math

color = (0, 0, 0)
Vcount = 0
pt = list()
imgCount = 0

def polygonCapture(img, pt, imgCount):  # 폴리곤 도형 내부 이미지 캡처 후 저장
    mask = np.zeros_like(img)
    pt_array = np.array(pt)
    pt_array = pt_array.reshape((-1, 1, 2))
    cv2.fillConvexPoly(mask, np.int32(pt_array), (255, 255, 255))
    result = cv2.bitwise_and(img, mask)
    cv2.imwrite(f"ksb{imgCount:04d}.jpg", result)

def onMouse(event, x, y, flags, param): # 최적화 필요함 
    global Vcount, pt, imgCount
    
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 좌클릭 이벤트
        if Vcount < 2:
            pt.append((x, y))
            cv2.circle(param, (x, y), 1, color)
            if Vcount == 1 : cv2.line(param, pt[0], pt[1], color)
        else:
            if checkRad(pt[Vcount - 2], pt[Vcount - 1], (x, y)) and checkRad((x, y), pt[0], pt[1]):    # 좌표들 각도 유효한지 확인
                if calcLen(x, y, pt[0][0], pt[0][1]) <= 20:
                    cv2.line(param, pt[Vcount - 1], pt[0], color)
                    imgCount += 1
                    polygonCapture(param, pt, imgCount)
                    Vcount = 0
                    pt.clear()
                else:
                    pt.append((x, y))
                    cv2.circle(param, (x, y), 1, color)
                    cv2.line(param, pt[Vcount - 1], pt[Vcount], color)
            else: Vcount -= 1
        
        Vcount += 1
        print(imgCount, Vcount)    # 테스트 용
        print(pt)
        cv2.imshow("paint", param)
    
def calcLen(x1, y1, x2, y2):    # 두 점 사이 거리 반환
    dx, dy = x2 - x1, y2 - y1
    result = math.sqrt(pow(dx,2) + pow(dy, 2))
    return result

def checkRad(pt1, pt2, pt3):   # 좌표를 pt1, pt2, pt3 순서대로 찍히면 v1 과 v2를 외적한 값이 0이하면 180도 이상임
    vx1, vy1 = pt1[0], pt1[1]
    vx2, vy2 = pt2[0], pt2[1]
    vx3, vy3 = pt3[0], pt3[1]
    
    v1 = (vx1 - vx2, vy1- vy2)  # 벡터 pt2 -> pt1
    v2 = (vx3 - vx2, vy3 - vy2) # 벡터 pt2 -> pt3
    
    result = (v1[0] * v2[1]) - (v2[0] * v1[1])  # v1, v2 외적값
    
    if result > 0:      # 180도 이내
        return True
    else:               # 180도 이상
        return False
    

def Brush():
    img = cv2.imread("input.jpg")
    img = cv2.resize(img, (640, 480))
    cv2.namedWindow("paint")
    cv2.setMouseCallback("paint", onMouse, param=img)
    cv2.imshow("paint", img)
    
    while True:
        
        key = cv2.waitKey(100)
        if key == 27:
            break
        
    cv2.destroyAllWindows()
    
    
Brush()