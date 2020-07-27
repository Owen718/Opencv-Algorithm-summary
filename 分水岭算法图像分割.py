import numpy as np
import cv2


def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



img = cv2.imread(r'C:\Users\Owen\Pictures\luoleye2.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#二值化
ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
cv_show('thresh',thresh)
#开操作去除噪声数据
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=2)
cv_show('opening',opening)

#通过对开操作变换后的图像进行膨胀操作，可以得到大部分都是背景的区域：
sure_bg = cv2.dilate(opening,kernel,iterations=3)
cv_show('sure_bg',sure_bg)

#反之，可以通过distanceTransform来获取确定的前景区域。也就是说这是图像中最可能是前景的区域，越是远离背景区域的边界的点越可能属于前景。
#在得到distanceTransform操作的结果后，应用一个阈值来决定哪些区域是前景，这样得到正确结果的概率很高。

dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret,sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
cv_show('sure_fg',sure_fg)

#所得到的前景和背景有重合的部分，怎么办呢？首先要确定这些区域，可从sure_bg与sure_fg的集合相减得到。
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)  #两图像相减。
cv_show('unknonw',unknown)

#有了这些区域，就可以设定栅栏来阻止水汇聚了，通过connectedComponents函数完成。
ret,markers = cv2.connectedComponents(sure_fg)

#在背景区域上+1，将unknown区域设为0
markers = markers +1 
markers[unknown==255] = 0

#打开门，让水漫进来并把栅栏绘成红色
markers = cv2.watershed(img,markers)
img[markers == -1] = [0,0,255]
img = img.astype(np.uint8)  #数值转化为uint8,不然报错。 ？
cv_show('img',img)
