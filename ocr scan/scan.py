import numpy as np
import cv2

def order_points(pts):
    rect = np.zeros((4,2),dtype="float32")

    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts,axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def four_point_transform(image,pts):    #图像变换
    rect = order_points(pts)
    (tl,tr,br,bl) = rect
    # 计算输入的w和h值
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))


    dst  = np.array([
        [0,0],
        [maxWidth - 1,0],
        [maxWidth - 1,maxHeight - 1],
        [0,maxHeight - 1]],dtype="float32"
    )

    M = cv2.getPerspectiveTransform,(rectdst)
    warped = cv2.warpPerspective(image,M,(maxWidth,maxHeight))

    return warped

def resize(image,width = None , height = None,inter = cv2.INTER_AREA):
    dim = None
    (h,w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r),height)
    else:
        r = width / float(w)
        dim = (width,int(h * r))
    
    resized = cv2.resize(image,dim,interpolation = inter)
    return resized

#image = cv2.imread(r"C:\Users\Owen\Pictures\page.jpg")
def scan_image(image):
    ratio = image.shape[0] / 1000.0
    orig = image.copy()

    image = resize(orig,height = 1000)


    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)   #灰度图
    gray = cv2.GaussianBlur(gray,(5,5),0)      #高斯滤波去除噪点



    edged = cv2.Canny(gray,75,200)
    #cv2.imshow('GaussianBlur',gray)
    #cv2.imshow('edged',edged)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cnts,hierarchy = cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts,key = cv2.contourArea , reverse = True)[:5]


    for c in cnts:
        peri = cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,0.02 * peri,True)

        if len(approx) == 4:
            screenCnt = approx
            break


    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    #cv2.imshow("Outline", image)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 透视变换
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)   #把坐标还原回去

    # 二值处理
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    ref = cv2.threshold(warped, 150, 255, cv2.THRESH_BINARY)[1]

    return resize(ref,height = 1000)


#cv2.imshow("Original", resize(orig, height = 650))
#cv2.imshow("Scanned", resize(ref, height = 650))

