import numpy as np 
import cv2
#经典测试视频
cap = cv2.VideoCapture('test.avi')   #测试视频
#形态学操作需要使用算子
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
#创建混合高斯模型用于背景建模
fgbg = cv2.createBackgroundSubtractorMOG2()

while(True):
    ret,frame = cap.read()
    fgmask = fgbg.apply(frame)
    #形态学开运算去除噪点
    fgmask = cv2.morphologyEx(fgmask,cv2.MORPH_OPEN,kernel)
    #寻找轮廓
    contours , hierarchy = cv2.findContours(fgmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for c  in contours:
        #计算各轮廓的周长
        perimeter = cv2.arcLength(c,True)
        if perimeter>100: 
            #找到一个竖直矩形
            x,y,w,h = cv2.boundingRect(c)
            if h>w:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)


    cv2.imshow('frame',frame)
    cv2.imshow('fgmask',fgmask)
    k = cv2.waitKey(150) & 0xff
    if k==27:
        break

cap.release()  #释放
cv2.destroyAllWindows()

