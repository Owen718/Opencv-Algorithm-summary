
import cv2
 
def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread(r'D:\github\Underwater-robot-competition\AUV_code\IPC\AUC_video_manager\screenshot.png')
original = cv2.resize(img, None, fx=0.5, fy=0.5)


def clahe_return(img):
    # 创建CLAHE对象
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # 限制对比度的自适应阈值均衡化
    dst = clahe.apply(img)
    # 使用全局直方图均衡化
    #equa = cv2.equalizeHist(img)
    # 分别显示原图，CLAHE，HE
    return dst

def RGB_clahe(img):  #限制性直方图
    b,g,r = cv2.split(img)
    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    b = clahe.apply(b)
    g = clahe.apply(g)
    r = clahe.apply(r)

    clahed = cv2.merge([b,g,r])
    return clahed


clahed = RGB_clahe(img)

cv2.imshow("img", original)
cv2.imshow("clahed", clahed)
cv2.waitKey()


#hsv色彩空间增大s值 色调（H），饱和度（S），亮度（V）。
hsv = cv2.cvtColor(original,cv2.COLOR_BGR2HSV)

(h,s,v) = cv2.split(hsv)
for x in range(hsv.shape[0]):
    for y in range(hsv.shape[1]):
        v[x,y] = v[x,y] + 20
        s[x,y] = s[x,y] + 20

hsv_enhance = cv2.merge((h,s,v))

rgb_enhance = cv2.cvtColor(hsv_enhance,cv2.COLOR_HSV2BGR)

cv_show('hsv_enhance',rgb_enhance)
