import cv2
import numpy as np

img = cv2.imread(r'C:\Users\Owen\Pictures\underwaterImage4.jpg')

B,G,R = cv2.split(img)
#定义卷积核（3*3）
k = np.array([
    [0,1,2],
    [2,2,0],
    [0,1,2]
])

print(B)


def convolution(k, data):   #(3*3)单通道二维卷积函数
    row,col= data.shape
    img_new = []
    for i in range(row-3):
        line = []
        for j in range(col-3):
            a = data[i:i+3,j:j+3]
            line.append(np.sum(np.multiply(k, a)))
        img_new.append(line)
    return np.uint8(img_new)

B = cv2.resize(B,dsize=None,fx=0.1,fy=0.1)

img_R_new = convolution(k,B)

print(img_R_new)

cv2.imshow('new R',img_R_new)
cv2.waitKey(0)
cv2.destroyAllWindows()