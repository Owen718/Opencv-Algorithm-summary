import cv2
import numpy as np


def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#hsv色彩空间增大s值 色调（H），饱和度（S），亮度（V）。

original = cv2.imread(r'C:\Users\Owen\Pictures\weixin1.jpg')
hsv = cv2.cvtColor(original,cv2.COLOR_BGR2HSV)


(h,s,v) = cv2.split(hsv)
for x in range(hsv.shape[0]):
    for y in range(hsv.shape[1]):
        v[x,y] = v[x,y] + 20
        s[x,y] = s[x,y] + 20

hsv_enhance = cv2.merge((h,s,v))

rgb_enhance = cv2.cvtColor(hsv_enhance,cv2.COLOR_HSV2BGR)

#cv_show('original',original)
cv_show('hsv_enhance',rgb_enhance)
print('yes!')