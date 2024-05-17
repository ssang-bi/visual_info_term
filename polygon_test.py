import numpy as np
import cv2
import math

drawing = False
ix, iy = -1, -1
color = (0, 0, 0)
count = 0
pt = list()
imgCount = 0

def polygonCapture(img, pt, imgCount):
    mask = np.zeros_like(img)
    pt_array = np.array(pt)
    pt_array = pt_array.reshape((-1, 1, 2))
    cv2.fillConvexPoly(mask, np.int32(pt_array), (255, 255, 255))
    result = cv2.bitwise_and(img, mask)
    cv2.imwrite(f"ksb{imgCount:04d}.jpg", result)

def onMouse(event, x, y, flags, param): # 최적화 필요함 
    global ix, iy, drawing, count, pt, imgCount
    
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 좌클릭 이벤트
        if drawing: # polygon 그리기 시작
            if count > 1:   # (3 + a)번쨰 점
                if checkRad(pt[count - 2], pt[count - 1], (x, y)) and checkRad((x, y), (ix, iy), pt[1]):    # 좌표들 각도 유효한지 확인
                    if calcLen(x, y, ix, iy) <= 20:     # 시작 좌표 랑 이전 좌표 연결
                        cv2.line(param, pt[count - 1], pt[0], color)
                        imgCount += 1
                        polygonCapture(param, pt, imgCount)
                        count = -1
                        pt.clear()
                        drawing = False     # polygon 완성
                    else:       # 좌표 찍기
                        pt.append((x, y))
                        cv2.circle(param, (x, y), 1, color)
                        cv2.line(param, pt[count - 1], pt[count], color)
                else:   # 유효하지 않은 좌표
                    count -= 1
            else:
                pt.append((x, y))
                cv2.circle(param, (x, y), 1, color)
                cv2.line(param, pt[count - 1], pt[count], color)
        else:   # polygon 첫 좌표 찍기
            ix, iy = x, y
            pt.append((ix, iy))
            cv2.circle(param, (ix, iy), 1, color)
            drawing = True
        
        count += 1
        print(imgCount, count)    # 테스트 용
        print(pt)
        cv2.imshow("paint", param)
    
def calcLen(x1, y1, x2, y2):
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
    #img = np.full((480, 640), 255, np.uint8)
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