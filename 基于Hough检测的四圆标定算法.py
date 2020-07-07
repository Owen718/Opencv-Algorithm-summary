import  cv2
import numpy as np
import requests
import base64
import json


rectangle_xy=np.zeros((12,2))

img=cv2.imread(r'C:\Users\Owen\Pictures\Label2.jpg')  #图片地址，改为你的图片地址
#cv2.imshow('img',img)
#降噪（模糊处理用来减少瑕疵点）
result = cv2.blur(img, (5,5))
#cv2.imshow('blur result',result)
#灰度化,就是去色（类似老式照片）
gray=cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray',gray)

blur_img = cv2.GaussianBlur(gray, (3, 3), 0)
#cv2.imshow("blur_img",blur_img)


ret, binary = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
#print("阈值：", ret)
#cv2.imshow("binary", binary)
 
#param1的具体实现，用于边缘检测   
canny = cv2.Canny(img, 40, 80)  
#cv2.imshow('canny', canny) 
 
circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,70,param1=80,param2=30,minRadius=0,maxRadius=20)


circle_gray_num=0
circle_gray_average=0

for i,circle in enumerate(circles[0]):  #遍历求圆心二值化后灰度均值
    x=int(circle[0])
    y=int(circle[1])
    r=int(circle[2])
    circle_gray_num = circle_gray_num + gray[x,y]
  # img=cv2.circle(img,(x,y),r,(0,0,255),1,8,0)
    print(str(i)+"="+str(gray[x+1,y+1]))
   

circle_gray_average = circle_gray_num / len(circles[0])
#print("circle_gray_average="+str(circle_gray_average))

for i,circle in enumerate(circles[0]):  #遍历去除多余的圆并标出
    #坐标行列(就是圆心)1
    x=int(circle[0])
    y=int(circle[1])
    #半径
    r=int(circle[2])
    if(gray[x][y]>=circle_gray_average):
        circles_new=np.delete(circles[0],i,0)
    else:
        #img=cv2.circle(img,(x,y),r,(0,0,255),1,8,0)
        circles_new=circles[0]



for i,circle in enumerate(circles_new):
    rectangle_xy[i][0]=circle[0]
    rectangle_xy[i][1]=circle[1]
   
if len(circles[0]<=11):
    rectangle_xy_new=np.delete(circles[0],[len(circles[0]),11],0)


#print(rectangle_xy_new)
#寻找矩形对顶点
max_x=0
max_y=0
min_x=999999
min_y=999999
for i,xy in enumerate(rectangle_xy_new):
    if rectangle_xy_new[i][0]>max_x:
        max_x=rectangle_xy_new[i][0]
    if rectangle_xy_new[i][0]<min_x:
        min_x=rectangle_xy_new[i][0]
    if rectangle_xy_new[i][1]>max_y:
        max_y=rectangle_xy_new[i][1]
    if rectangle_xy_new[i][1]<min_y:
        min_y=rectangle_xy_new[i][1]

ret = np.array([[[0,0]]],order='F')
for i,xy in enumerate(rectangle_xy_new):
    ret = np.append(ret,[[[rectangle_xy_new[i][0],rectangle_xy_new[i][1]]]],axis=0)

ret = np.delete(ret,0,axis=0)
print(ret)





img=cv2.rectangle(img,(int(min_x),int(min_y)),(int(max_x),int(max_y)),(0,0,255))
cut_img = img[int(min_y):int(max_y),int(min_x):int(max_x)]

cv2.imshow('cut_img',cut_img)

cv2.imshow('find_circle',img)

 #按任意键退出
cv2.waitKey(0)
cv2.destroyAllWindows()


