#高通滤波器
#高通滤波器（High Pass Filter，HPF）是检测图像的某个区域，
#然后根据像素与周围像素的亮度差值来提升（boost）该像素的亮度的滤波器。
#高通滤波器是根据像素与邻近像素的亮度差值来提升该像素的亮度。
# 低通滤波器（Low Pass Filter，LPF）则是在像素与周围像素的亮度差值小于一个特定值时，平滑该像素的亮度。
# 它主要用于去噪和模糊化，例如，高斯模糊是最常用的模糊滤波器（平滑滤波器）之一，它是一个削弱高频信号强度的低通滤波器。

import cv2
import numpy as np
from scipy import ndimage



kernel_3x3 = np.array([
        [-1,-1,-1],
        [-1,8,-1],
        [-1,-1,-1]
])

kernel_5x5 = np.array([
        [-1,-1,-1,-1,-1],
        [-1, 1, 2, 1,-1],  
        [-1, 2, 4, 2,-1],  
        [-1, 1, 2, 1,-1],  
        [-1,-1,-1,-1,-1],    
])

img = cv2.imread(r'C:\Users\Owen\Pictures\lena.jpg',0)

k3 = ndimage.convolve(img,kernel_3x3)
k5 = ndimage.convolve(img,kernel_5x5)

blurred = cv2.GaussianBlur(img,(11,11),0)  #高斯模糊是一个削弱高频信号强度的低通滤波器
g_hpf = img - blurred  #原图与其相减，可保留更多的特征信息。

cv2.imshow("Gaussian blurred",blurred)
cv2.imshow("img",img)
cv2.imshow("3x3",k3)
cv2.imshow("5x5",k5)
cv2.imshow("g_hpf",g_hpf)

cv2.waitKey(0)
cv2.destroyAllWindows()