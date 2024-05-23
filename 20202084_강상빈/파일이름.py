import numpy as np
import cv2
import math

def setMode(key, nullImg, ellipseImg, polygonImg):      # MODE(NULL, Ellipse, Polygon) 설정 함수
    global MODE, ACTIVE_IMG, BASE_IMG, DRAWING, VCOUNT  # ACTIVE_IMG : 활성된 모드 텍스트 출력 이미지, BASE_IMG : 원본 이미지, DRAWING : Ellipse mode에서 사용(타원 그리기 시작 유무), VCOUNT : Polygom mode에서 사용(찍은 점 개수)
    
    if key == ord('1'):
        PT.clear()                  # 좌표 리스트 초기화
        VCOUNT, DRAWING = 0, False                  # mode 전환할 경우 VCOUNT, DRAWING 초기화
        if MODE == "Ellipse":       # 이미 Ellipse MODE인 경우 NULL MODE로 전환
            MODE = "NULL"
            ACTIVE_IMG = nullImg
        else:
            MODE = "Ellipse"    # Ellipse MODE가 아닌 경우 Ellipse MODE로 전환
            ACTIVE_IMG = ellipseImg
        cv2.setMouseCallback("Extract ROI", drawing, ACTIVE_IMG)      ############
        cv2.imshow("Extract ROI", ACTIVE_IMG)                         # if 문 안에 넣은 이유 : while문이 반복 될 때 마다 불필요한 작업 방지
        
    elif key == ord('2'):
        PT.clear()              # 좌표 리스트 초기화
        VCOUNT, DRAWING = 0, False                  # mode 전환할 경우 VCOUNT, DRAWING 초기화
        if MODE == "Polygon":   # 이미 Polygon MODE인 경우 NULL MODE로 전환
            MODE = "NULL"
            ACTIVE_IMG = nullImg
        else:
            MODE = "Polygon"    # Polygon MODE가 아닌 경우 Polygon MODE로 전환
            ACTIVE_IMG = polygonImg
        cv2.setMouseCallback("Extract ROI", drawing, ACTIVE_IMG)      ############
        cv2.imshow("Extract ROI", ACTIVE_IMG)                         # if 문 안에 넣은 이유 : while문이 반복 될 때 마다 불필요한 작업 방지
    
def drawing(event, x, y, flags, param):   # 도형 그리는 함수
    global PT, COLOR        # PT : 좌표 저장 리스트, COLOR : 색상 값
    
    if MODE == "Ellipse" : drawEllipse(event, x, y)
    elif MODE == "Polygon": drawPolygon(event, x, y)
    
def drawEllipse(event, x, y):   # 타원 그리는 함수
    global DRAWING                                      # DRAWING : 타원 그리기 시작 유무
    
    if event == cv2.EVENT_LBUTTONDOWN:
        DRAWING = True                                  # 타원 그리기 시작
        PT.append((x, y))                               # 시작 좌표 저장
        
    elif DRAWING and event == cv2.EVENT_MOUSEMOVE:      # 좌클릭 한 상태에서 움직일 때만 이벤트 발생하게 함
        center = ((x + PT[0][0]) // 2, (y + PT[0][1]) // 2)                 # 중심 좌표 실시간 계산
        axes = (abs((x - PT[0][0]) // 2), abs((y - PT[0][1]) // 2))         # 장축, 단축 실시간 계산, 음수 값 되는 경우 방지 : 절댓값 처리
        TMP_IMG = ACTIVE_IMG.copy()                              ####     
        cv2.ellipse(TMP_IMG, center, axes, 0, 0, 360, COLOR, 2)  # ACTIVE_IMG의 복사본에 실시간으로 타원 그려지는 모습 보이게 출력
        cv2.imshow("Extract ROI", TMP_IMG)                             ####
        
    elif event == cv2.EVENT_LBUTTONUP:
        DRAWING = False                                 # 타원 그리기 끝
        PT.append((x, y))                               # 마지막 좌표 저장
        saveImg(BASE_IMG)                               # 이미지만 저장되게 하는 함수
        cv2.imshow("Extract ROI", ACTIVE_IMG)                 # 도형 제외한 이미지 출력

def drawPolygon(event, x, y):   # 다각형 그리는 함수
    global VCOUNT, TMP_IMG                              # VCOUNT : 찍은 좌표 개수, TMP_IMG : 1개의 다각형만 그려지는 이미지
    
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 좌클릭 이벤트
        if VCOUNT == 0:                                 # 다각형 그리기 시작
            PT.clear()                                  # 좌표 리스트 초기화
            TMP_IMG = np.zeros_like(ACTIVE_IMG)         ####
            TMP_IMG = ACTIVE_IMG.copy()                 # 다각형 하나 그릴 때 마다 TMP_IMG에 ACTIVE_IMG 복사
            
        if VCOUNT < 2:                                                          # 1번째, 2번째 경우
            PT.append((x, y))                                                   # 점 찍을 때 마다 좌표 저장
            cv2.circle(TMP_IMG, (x, y), 1, COLOR)                               # 찍은 위치에 점 표시
            if VCOUNT == 1 : cv2.line(TMP_IMG, PT[0], PT[1], COLOR, 2)          # 시작 점과 두번째 점 선으로 잇기
            VCOUNT += 1                                                         # 좌표 횟수 증가
            cv2.imshow("Extract ROI", TMP_IMG)                                        # 진행상황 출력
        
        else:   # 0 < 이전 2개의 좌표와 현재 찍은 좌표 각도 & 1,2 번째 좌표랑 현재 찍은 좌표 각도 < 180 : 충족한 경우에만 현재 좌표 유효
            if checkRad(PT[VCOUNT - 2], PT[VCOUNT - 1], (x, y)) and checkRad((x, y), PT[0], PT[1]):
                if calcLen(x, y, PT[0][0], PT[0][1]) <= 20:                     # 현재 찍은 좌표가 시작점과의 거리가 20미만
                    cv2.line(TMP_IMG, PT[VCOUNT - 1], PT[0], COLOR, 2)          # 직전 좌표에 시작 좌표 잇기
                    saveImg(BASE_IMG)                                           # 그려진 다각형 크기만큼 원본 이미지 잘라 저장
                    VCOUNT = 0                                                  # 좌표 개수 초기화
                    cv2.imshow("Extract ROI", ACTIVE_IMG)                             # mode 텍스트와 원본 이미지만 출력                    
                else:
                    if checkRad(PT[VCOUNT - 1], (x, y), PT[0]):     # 달팽이 형태로 말려 들어가는 현상 방지
                        PT.append((x, y))                                           # 찍은 좌표 저장
                        cv2.circle(TMP_IMG, (x, y), 1, COLOR)                       # 찍은 좌표 점 표시
                        cv2.line(TMP_IMG, PT[VCOUNT - 1], PT[VCOUNT], COLOR, 2)     # 직전 좌표와 찍은 좌표 선으로 잇기
                        VCOUNT += 1                                                 # 좌표 횟수 증가
                        cv2.imshow("Extract ROI", TMP_IMG)                                # 진행상황 출력
                    
def checkRad(pt1, pt2, pt3):    # 3개의 좌표 사이에 각도 계산 함수
    v1 = (pt1[0] - pt2[0], pt1[1]- pt2[1])  # 벡터 pt2 -> pt1
    v2 = (pt3[0] - pt2[0], pt3[1] -pt2[1])  # 벡터 pt2 -> pt3
    
    result = (v1[0] * v2[1]) - (v2[0] * v1[1])  # v1, v2 외적값
    
    # 좌표를 pt1, pt2, pt3 순서대로 찍히면 v1 과 v2를 외적한 값이 0이하면 180도 이상이다
    if result > 0: return True      # 180도 이내
    else: return False              # 180도 이상

def calcLen(x1, y1, x2, y2):    # 두 점 사이 거리 반환
    dx, dy = x2 - x1, y2 - y1
    result = math.sqrt(pow(dx,2) + pow(dy, 2))
    return result

def saveImg(param):             # 이미지 저장 함수
    global IMGCOUNT             # 현재 저장된 이미지 개수
    mask = np.zeros_like(param) # 현재 출력된 이미지 크기 만큼 검은 이미지 생성
    
    if MODE == "Ellipse" : result = captureEllipse(param, mask)         # 타원 이미지 저장
    elif MODE == "Polygon": result = capturePolygon(param, mask)        # 다각형 이미지 저장

    IMGCOUNT += 1                                       # 저장된 이미지 개수 증가
    cv2.imwrite(f"ksb{IMGCOUNT:04d}.jpg", result)       # 이미지 저장
    PT.clear()                                          # 저장된 좌표 초기화
          
def captureEllipse(param, mask):    # 타원 이미지 저장 함수
    center = ((PT[1][0] + PT[0][0]) // 2, (PT[1][1] + PT[0][1]) // 2)   # 최종 중심 좌표 계산
    axes = (abs((PT[1][0] - PT[0][0]) // 2), abs((PT[1][1] - PT[0][1]) // 2))     # 최종 장축, 단축 길이 계산, 음수 값 되는 경우 방지 : 절댓값 처리
    
    cv2.ellipse(mask, center, axes, 0, 0, 360, (255, 255, 255), -1)     # mask에 최종 타원 형태로 마스크 생성 (타원 : 1, 배경 : 0)
    result = cv2.bitwise_and(param, mask)                               # 원본 이미지와 mask 이미지 and 연산

    return result       # 생성된 타원 이미지 반환
    
def capturePolygon(param, mask):    # 다각형 이미지 저장
    pt_array = np.array(PT)         # PT 리스트에 저장된 좌표 array 형태로 저장
    cv2.fillConvexPoly(mask, np.int32(pt_array), (255, 255, 255))   # mask에 최종 다각형 형태로 마스크 생성 (다각형 : 1, 배경 : 0)
    result = cv2.bitwise_and(param, mask)                           # 원본 이미지와 mask 이미지 and 연산

    return result       # 생성된 다각형 이미지 반환

MODE = "NULL"               # 초기 Mode : NULL
PT = list()                 # 좌표 리스트 생성
IMGCOUNT = 0                # 저장된 이미지 개수 
COLOR = (0, 127, 255)       # mode text 및 도형 색상
VCOUNT = 0                  # 다각형 꼭짓점 개수
DRAWING = False             # 타원 그리기 시작 유무

BASE_IMG = cv2.imread("input.jpg")                  # input.jpg 파일 읽어오기
BASE_IMG = cv2.resize(BASE_IMG, (640, 480))         # 해상도 640 x 480 으로 조정

nullImg = BASE_IMG.copy()       #######
ellipseImg = BASE_IMG.copy()    # 이미지 파일 및 크기 자체는 BASE_IMG와 같음
polygonImg = BASE_IMG.copy()    #######

cv2.putText(nullImg, "NULL", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR, 2)         #####
cv2.putText(ellipseImg, "Ellipse", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR, 2)   # 각각의 MODE를 좌측 상단에 출력
cv2.putText(polygonImg, "Polygon", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR, 2)   #####
    
ACTIVE_IMG = nullImg    # 초기 활성 이미지 : nullImg
TMP_IMG = None          # NULL mode에서는 활성화X

cv2.imshow("Extract ROI", ACTIVE_IMG)     # 시작 화면
    
while True:
    key = cv2.waitKeyEx(100)        # keyboard event 대기 (0.1s)
    if key == 27: break             # esc 입력 받으면 종료
        
    setMode(key, nullImg, ellipseImg, polygonImg)   # 입력 받은 키에 따라 mode 변경
        
cv2.destroyAllWindows()             # 생성된 모든 윈도우 종료