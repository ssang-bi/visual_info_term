import numpy as np
import cv2
import math

def setMode(key, nullImg, ellipseImg, polygonImg):   # MODE(NULL, Ellipse, Polygon) 설정 키
    global MODE, ACTIVE_IMG
    
    if key == ord('1'):
        if MODE == "Ellipse":   # 이미 Ellipse MODE인 경우 NULL MODE로 전환
            MODE = "NULL"
            ACTIVE_IMG = nullImg
            cv2.imshow("paint", nullImg)
        else:
            MODE = "Ellipse"    # Ellipse MODE가 아닌 경우 Ellipse MODE로 전환
            ACTIVE_IMG = ellipseImg
            cv2.imshow("paint", ellipseImg)
    elif key == ord('2'):
        if MODE == "Polygon":   # 이미 Polygon MODE인 경우 NULL MODE로 전환
            MODE = "NULL"
            ACTIVE_IMG = nullImg
            cv2.imshow("paint", nullImg)
        else:
            MODE = "Polygon"    # Polygon MODE가 아닌 경우 Polygon MODE로 전환
            ACTIVE_IMG = polygonImg
            cv2.imshow("paint", polygonImg)
  
def drawing(event, x, y, flags, param):
    global PT, COLOR
    
    if MODE == "Ellipse" : drawEllipse(event, x, y, flags, param)
    elif MODE == "Polygon": drawPolygon(event, x, y, flags, param)
    
def drawEllipse(event, x, y, flags, param): # 수정해야함
    global DRAWING
    
    if event == cv2.EVENT_LBUTTONDOWN and MODE == "Ellipse":
        DRAWING = True
        PT.append((x, y))
    elif event == cv2.EVENT_MOUSEMOVE:
        if DRAWING:
            center = ((x + PT[0][0]) // 2, (y + PT[0][1]) // 2)
            axes = (abs((x - PT[0][0]) // 2), abs((y - PT[0][1]) // 2))
            tmpimg = param.copy()
            cv2.ellipse(tmpimg, center, axes, 0, 0, 360, COLOR, 2)
            cv2.imshow("paint", tmpimg)
    elif event == cv2.EVENT_LBUTTONUP:
        DRAWING = False
        PT.append((x, y))
        saveImg(param)
        cv2.imshow("paint", param)

def drawPolygon(event, x, y, flags, param):
    global VCOUNT
    
    if event == cv2.EVENT_LBUTTONDOWN and MODE == "Polygon":  # 마우스 좌클릭 이벤트
        if VCOUNT < 2:
            PT.append((x, y))
            cv2.circle(param, (x, y), 1, COLOR)
            if VCOUNT == 1 : cv2.line(param, PT[0], PT[1], COLOR)
        else:
            if checkRad(PT[VCOUNT - 2], PT[VCOUNT - 1], (x, y)) and checkRad((x, y), PT[0], PT[1]):
                if calcLen(x, y, PT[0][0], PT[0][1]) <= 20:
                    cv2.line(param, PT[VCOUNT - 1], PT[0], COLOR)
                    saveImg(param)
                    VCOUNT = -1
                else:
                    PT.append((x, y))
                    cv2.circle(param, (x, y), 1, COLOR)
                    cv2.line(param, PT[VCOUNT - 1], PT[VCOUNT], COLOR)
            else: VCOUNT -= 1
        
        VCOUNT += 1
        cv2.imshow("paint", param)
                    
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

def calcLen(x1, y1, x2, y2):    # 두 점 사이 거리 반환
    dx, dy = x2 - x1, y2 - y1
    result = math.sqrt(pow(dx,2) + pow(dy, 2))
    return result

def saveImg(param):
    global IMGCOUNT
    mask = np.zeros_like(param)
    
    if MODE == "Ellipse" : result = captureEllipse(param, mask)
    elif MODE == "Polygon": result = capturePolygon(param, mask)
    
    IMGCOUNT += 1
    cv2.imwrite(f"ksb{IMGCOUNT:04d}.jpg", result)
    PT.clear()
          
def captureEllipse(param, mask):
    center = ((PT[1][0] + PT[0][0]) // 2, (PT[1][1] + PT[0][1]) // 2)
    axes = ((PT[1][0] - PT[0][0]) // 2, (PT[1][1] - PT[0][1]) // 2)
    
    cv2.ellipse(mask, center, axes, 0, 0, 360, (255, 255, 255), -1)
    result = cv2.bitwise_and(param, mask)

    return result
    
def capturePolygon(param, mask):
    pt_array = np.array(PT)
    pt_array = pt_array.reshape((-1, 1, 2))
    cv2.fillConvexPoly(mask, np.int32(pt_array), (255, 255, 255))
    result = cv2.bitwise_and(param, mask)
    
    return result

MODE = "NULL"
PT = list()
IMGCOUNT = 0
COLOR = (0, 0, 0)
VCOUNT = 0
DRAWING = False


BASE_IMG = cv2.imread("input.jpg")
BASE_IMG = cv2.resize(BASE_IMG, (640, 480))

nullImg = BASE_IMG.copy() # 이미지 파일 및 크기 자체는 NULL MODE와 같음
ellipseImg = BASE_IMG.copy()
polygonImg = BASE_IMG.copy()

cv2.putText(nullImg, "NULL", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)     # 각각의 MODE를 좌측 상단에 출력
cv2.putText(ellipseImg, "Ellipse", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
cv2.putText(polygonImg, "Polygon", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
ACTIVE_IMG = nullImg

cv2.namedWindow("paint")
cv2.setMouseCallback("paint", drawing, param=ACTIVE_IMG)
cv2.imshow("paint", ACTIVE_IMG)
    
while True:
    key = cv2.waitKeyEx(100)
    if key == 27: break
        
    setMode(key, nullImg, ellipseImg, polygonImg)
        
cv2.destroyAllWindows()