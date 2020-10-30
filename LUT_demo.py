import cv2
import numpy as np 



def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

def Creat_singlechannel_lookuptable(quan_val):  #创建一个单通道lut
    lut = np.zeros(256,dtype = np.uint8)
    for i in range(255):
        lut[i]=quan_val * int( i / quan_val)
    return lut


def Creat_BGRchannel_lookuptable():
    identity = np.arange(256, dtype = np.dtype('uint8'))
    zeros = np.zeros(256, np.dtype('uint8'))
    lut = np.dstack((identity, identity, zeros))
    return lut



img = cv2.imread(r'C:\Users\Owen\Pictures\lena.jpg',0)

cv_show('img',img)
lut = Creat_singlechannel_lookuptable(100)   #

out = cv2.LUT(img,lut)

cv_show('out',out)
        

cap=cv2.VideoCapture(0)
while True:
    ret,img=cap.read()
    if not ret:
            break
    showimg=cv2.LUT(img,lut)
    cv2.imshow("img",showimg)
    cv2.waitKey(1)   