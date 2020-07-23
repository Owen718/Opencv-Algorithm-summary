import cv2
import numpy as np
from matplotlib import pyplot as plt
 
img1 = cv2.imread(r'C:\Users\Owen\Pictures\weixin1.jpg')

 
img_hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)     # bgr转hsv 

 
color = ('h', 's', 'v')
 
for i, col in enumerate(color):
    # histr = cv2.calcHist([img_hsv1], [i], None, [256], [0, 256])
    hist1, bins = np.histogram(img_hsv1[:, :, i].ravel(), 256, [0, 256])  
    hist2, bins = np.histogram(img_hsv2[:, :, i].ravel(), 256, [0, 256])
    cdf1 = hist1.cumsum()  # 灰度值0-255的累计值数组
    cdf2 = hist2.cumsum()
    cdf1_hist = hist1.cumsum() / cdf1.max()  # 灰度值的累计值的比率
    cdf2_hist = hist2.cumsum() / cdf2.max()
 
    diff_cdf = [[0 for j in range(256)] for k in range(256)]  # diff_cdf 里是每2个灰度值比率间的差值
    for j in range(256):                                     
        for k in range(256):
            diff_cdf[j][k] = abs(cdf1_hist[j] - cdf2_hist[k])
 
    lut = [0 for j in range(256)]        # 映射表
    for j in range(256):
        min = diff_cdf[j][0]
        index = 0
        for k in range(256):            # 直方图规定化的映射原理
            if min > diff_cdf[j][k]:
                min = diff_cdf[j][k]
                index = k
        lut[j] = ([j, index])
 
    h = int(img_hsv1.shape[0])
    w = int(img_hsv1.shape[1])
    for j in range(h):                   # 对原图像进行灰度值的映射
        for k in range(w):
            img_hsv1[j, k, i] = lut[img_hsv1[j, k, i]][1]
 
 
hsv_img1 = cv2.cvtColor(img_hsv1, cv2.COLOR_HSV2BGR)   # hsv转bgr

 
cv2.namedWindow('firstpic', 0)
cv2.resizeWindow('firstpic', 670, 900)
cv2.namedWindow('targetpic', 0)
cv2.resizeWindow('targetpic', 670, 900)
cv2.namedWindow('defpic', 0)
cv2.resizeWindow('defpic', 670, 900)
 
cv2.imshow('firstpic', img1)

# cv2.imshow('img1', img_hsv1)
cv2.imshow('defpic', hsv_img1)
 
cv2.waitKey(0)
cv2.destroyAllWindows()