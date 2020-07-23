import cv2
import numpy as np
import math

def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#hsv色彩空间增大s值 色调（H），饱和度（S），亮度（V）。

original = cv2.imread(r'C:\Users\Owen\Pictures\weixin1.jpg')
bgr = original.copy()


def log_transfer_enhance(bgr,c,v):  #s=c*log(1+v*r)/log(v+1)   r=(0,1)
    (b,g,r) = cv2.split(bgr)
    for x in range(bgr.shape[0]):
        for y in range(bgr.shape[1]):
            b[x,y] = c * math.log(1 + v * b[x,y]) / math.log(v + 1)
            g[x,y] = c * math.log(1 + v * g[x,y]) / math.log(v + 1)
            r[x,y] = c * math.log(1 + v * r[x,y]) / math.log(v + 1)
    img = cv2.merge((b,g,r))
    cv2.normalize(img,img,0,255,cv2.NORM_MINMAX)
    m_img=cv2.convertScaleAbs(img)
    return m_img

for i in range(1,9):
    img  = log_transfer_enhance(bgr,1,i)
    cv2.imshow(str(i),img)

