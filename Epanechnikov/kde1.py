# 导包处理
import cv2 as cv
from math import *
import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D
import time


# 图片加载函数
def load_image(filename):
    imgs = os.listdir(filename)  # 返回指定的文件夹包含的文件或文件夹的名字的列表。
    imgs.sort(key=lambda x:x[1:5])       #  按照文件名称做排序处理
    channels = len(imgs)                      #  获得指定文件中图片的个数
    data = np.empty((300, 400, 3, channels))     # 创建一个4维空数组
    for i in range(channels):
        img = Image.open(filename + "/" + imgs[i])      # 打开对应的图片
        img1 = np.array(Image.open(filename + "/" + imgs[i]))
        rows, cols, dims = img1.shape                  # 返回对应图像的形状，分别是高,宽,维度数
        arr = np.asarray(img)                 # 复制一个img形状的数组
        data[:, :, :, i] = arr             # 赋值
    return data, rows, cols, dims


train_data,rows,cols,dims = load_image(r'D:\github\Opencv-Algorithm-summary\Epanechnikov\training3')    # 载入对应的训练图片,共20个训练样本
test_data = Image.open(r'D:\github\Opencv-Algorithm-summary\Epanechnikov\test3\image21.jpg')          # 载入对应的测试图片，有一个测试样本
test_data = np.asarray(test_data)                     # 将图片转化成数组形式


h,temp = 100,1         # 带宽值设定为120，中间变量为1
P = np.zeros((rows, cols))      # 一个二维的全0数组,为最后的输出概率
P1 = np.empty((rows,cols,dims))      # 三维的全空数组
P2 = np.zeros((rows, cols))              # 二维的全0数组


start_time = time.time()

# for train_single in train_data:
#     P1 = 1 - (  (test_data - train_single)/float(h)**2)
#     P1[P1<0]=0
#     temp = temp * P1
#     p2 = temp

for i in range(20):      #  共20个训练样本
    for j in range(rows):
        for k in range(cols):
            for l in range(dims):
                P1[j, k, l] = 1 - (((test_data[j, k, l] - train_data[j, k, l, i])/float(h))**2)
                if P1[j, k, l] < 0:         # 如果概率密度函数值小于0，那么将其赋值为0
                    P1[j, k, l] = 0
                temp = temp * P1[j, k, l]
            P2[j, k] = temp
            
            temp = 1.0
    P = P + P2                         # 图片像素的叠加
P = 15/(8*pi*20*h**3) * P         # EP函数的表达式，其中N=20

fig = plt.figure()              # 新建子图对象,开始绘制KDE三维色彩图
ax = fig.gca(projection='3d')
X = np.linspace(1,rows,rows)
Y = np.linspace(1,cols,cols)
X, Y = np.meshgrid(Y, X)
ax.plot_surface(X, Y, P, cmap=plt.get_cmap('rainbow'))            # 设置对应的xyz轴的参数及颜色的映射
plt.title('KDE_Three_dimensional_color_map',fontsize='large', fontweight='bold')
plt.savefig("KDE_result_5.jpg")                     # 保存KDE三维色彩图
plt.show()



image = np.zeros((rows,cols))                             # 开始做二值化图像
for i in range(rows):
    for j in range(cols):
        if P[i,j] < 4.55 * 10 ** -7:
            image[i,j] = 255
        else:
            image[i,j] = 0





binary = Image.fromarray(image)   # 由数组转化成对应的二维图片
plt.figure()
plt.imshow(binary)
plt.savefig("Binary_5.jpg")         # 保存为jpg格式的图像
plt.show()


# 可以创新的地方:画出来的图片可能会缺角，引入 opencv 库中的函数做一个扩张的补充
# 拍的照片文件格式过大，可以用cv库更改文件样式