import cv2
import numpy as np
from matplotlib import pyplot as plt 

img = cv2.imread(r'C:\Users\Owen\Pictures\lena.jpg')  #加载想要处理的图像
mask = np.zeros(img.shape[:2],np.uint8)#创建一个与所加载图像同形状的掩模，并用0填充

bgdModel = np.zeros((1,65),np.float64)  #创建以0填充的前景背景模型
fgdModel = np.zeros((1,65),np.float64)  #创建以0填充的后景背景模型

rect = (100,50,421,378)  #准备用一个标识出想要隔离的对象的矩形来初始化GrabCut算法。背景和前景模型都要基于这个初始矩形所留下的区域来决定。
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)  #使用指定的空模型和掩模来运行GrabCut算法，实际上是用一个矩形来初始化这个操作。
                                                                      #fgdModel后的参数iterCount（demo中为5）是算法的迭代次数（整型数）
#经过以上处理后，mask已经变成包含0~3的值，值为0和2的将转化为0，值为1和3的将转为1，然后保存在mask2中。
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')   #对mask中的值进行转换，这样就可以用mask2过滤出所有的0值像素。
img = img * mask2[:,:,np.newaxis]

#并排展示。
plt.subplot(121)
plt.imshow(img)
plt.title("grabcut")
plt.xticks([])
plt.yticks([])
plt.subplot(122)
plt.imshow(cv2.cvtColor(cv2.imread(r'C:\Users\Owen\Pictures\lena.jpg'),cv2.COLOR_BGR2GRAY))
plt.title("original")
plt.xticks([])
plt.yticks([])
plt.show()