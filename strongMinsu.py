import cv2
import numpy as np

def Ellipse_To_Image(image2, roi_ellipse_center, roi_ellipse_axes, count) : # roi_ellipse 영역을 이미지에서 추출
    mask = np.zeros_like(image2)
    cv2.ellipse(mask, roi_ellipse_center, roi_ellipse_axes, 0, 0, 360, (255, 255, 255), thickness=-1)
    result = cv2.bitwise_and(image2, mask)
    cv2.imwrite(f"kms{count:04d}.jpg", result)

"""
 def Polygon_To_Image(image, pts, count) :
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, [pts], (255,255,255))
    result = cv2.bitwise_and(image, mask)
    cv2.imwrite(f"kms{count:04d}.jpg", result)
"""

def onMouse_Roi_Ellipse(event, x, y, flags, param): # roi_Ellipse 생성
    global pt1
    global pt2
    global mode
    global roi_ellipse_center
    global roi_ellipse_axes
    global count
    global image1
    global image2

    if mode != 1:
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        pt1 = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        pt2 = (x, y)
        count += 1
        roi_ellipse_center = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
        roi_ellipse_axes = ((pt2[0] - pt1[0]) // 2, (pt2[1] - pt1[1]) // 2)
        cv2.ellipse(image1, roi_ellipse_center, roi_ellipse_axes, 0, 0, 360, (0, 0, 255))
        Ellipse_To_Image(image2, roi_ellipse_center, roi_ellipse_axes, count)
        cv2.imshow("image", image1)
"""
def onMouse_Polygon(event, x, y, flags, param) :
    global pts
    global mode
    global count
    global image

    if mode != 2:
        return

    if event == cv2.EVENT_LBUTTONDOWN :
        if len(pts) == 0:
            pts.append((x, y))
        else:
            if np.sqrt((pts[0][0]-x)**2 + (pts[0][1]-y)**2) <= 20: # ㅅ발 내각 어케함
                pts.append(pts[0])
                Polygon_To_Image(image, pts, count)
                pts = []
                count += 1
                cv2.imshow("image", image)
            else:
                pts.append((x, y))
            if len(pts) > 1:
                cv2.line(image, pts[-2], pts[-1], (0, 0, 255), 2)
                cv2.imshow("image", image)
"""

pt1 = (-1, -1)
pt2 = (-1, -1)
roi_ellipse_center = (0, 0)
roi_ellipse_axes = (0, 0)
pts = []
count = 0
image1 = cv2.imread("input.jpg") # 나한테 보여지는 이미지. 빨간 타원 생김.
image1 = cv2.resize(image1, (640, 480))
image2 = cv2.imread("input.jpg") # 결과 윈도우에 사용될 이미지. 빨간 선 없어짐.
image2 = cv2.resize(image2, (640, 480))

cv2.namedWindow("image")
cv2.imshow("image", image1)
mode = 0

while True :
    key = cv2.waitKey(100)
    if key == 27 :
        break
    elif key == ord('1'):
        cv2.setMouseCallback("image", onMouse_Roi_Ellipse)
        mode = 1
        """
    elif key == ord('2'):
        cv2.setMouseCallback("image", onMouse_Polygon)
        mode = 2
        """

cv2.destroyAllWindows()