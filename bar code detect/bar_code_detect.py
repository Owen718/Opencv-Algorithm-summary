import cv2
import numpy as np
import pytesseract
from PIL import Image


def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread(r'C:\bar_code_test.jpg')

#cv_show('origin',img)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#cv_show('gray',gray)

#ret,binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

#cv_show('binary',binary)

#x方向梯度计算
sobelx =cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
sobelx = cv2.convertScaleAbs(sobelx)
cv_show('sobelx',sobelx)
#y方向梯度计算
sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)
sobely = cv2.convertScaleAbs(sobely)
#cv_show('sobely',sobely)

sobel = sobelx - sobely

#sobelxy = cv2.addWeighted(sobelx,0.5,sobely,0.5,0)
#cv_show('sobelx-y',sobel)
#cv_show('sobelx+y',sobelxy)
#测试可知x方向sobel计算效果最好。选取sobelx图像

#高斯滤波
gaussian = cv2.GaussianBlur(sobelx,(9,9),1)
#cv_show('gaussian',gaussian)

#二值化
ret,binary = cv2.threshold(gaussian,127,255,cv2.THRESH_BINARY)
#cv_show('binary',binary)

#闭运算
kernel = np.ones((5,5),np.uint8)
closing  = cv2.morphologyEx(binary,cv2.MORPH_CLOSE,kernel)

#cv_show('closing',closing)

#x方向上缩小
resized_small  = cv2.resize(closing,dsize=None,fx = 0.4,fy=1)
cv_show('resized_small',resized_small)

#膨胀与腐蚀
kernel = np.ones((3,3),np.uint8)
dige = cv2.dilate(resized_small,kernel,iterations = 2)  #膨胀
erosion = cv2.erode(dige,kernel,iterations=4)   #腐蚀
cv_show('erosion',erosion)

#再次二值化
ret,binary = cv2.threshold(erosion,200,255,cv2.THRESH_BINARY)
cv_show('binary',binary)

#x方向放大
resized_big = cv2.resize(binary,dsize=None,fx=2.5,fy=1)
cv_show('resized_big',resized_big)

#画出全部轮廓
(contours,hierarchy)= cv2.findContours(resized_big,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)   #opencv4.x中需修改为： contours,hierarchy= cv2.findContours(closing,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
draw_img  = img.copy()
res = cv2.drawContours(draw_img , contours,-1,(0,0,255),2)
cv_show('res',res)

#遍历寻找条形码
max_area=0
(max_x,max_y,max_h,max_w)=(0,0,0,0)
for (i,c) in enumerate(contours):
    (x,y,w,h) = cv2.boundingRect(c)
    #cv_show('roi',img[y:y+h,x:x+w])
    if h*w > max_area and w>h:
        (max_x,max_y,max_w,max_h) = (x,y,w,h)
        bar_code_contours = c
#显示条形码        
roi = img[max_y-5:max_y+max_h+5,max_x-5:max_x+max_w+5]
cv_show('roi',roi)
#框出条形码
draw_img = img.copy()
res = cv2.rectangle(draw_img,(max_x-3,max_y-3),(max_x+w+3,max_y+h+3),(0,0,255),2)
cv_show('res',res)


#显示条形码下的数字和字母
number_roi = img[max_y+max_h-3:max_y+max_h+int(0.6*max_h),max_x:max_x+max_w]
cv_show('number',number_roi)
#框出数字和字母
res = cv2.rectangle(res,(max_x,max_y+max_h),(max_x+max_w,max_y+max_h+int(0.6*max_h)),(0,255,0),2)
cv_show('res',res)




ret,number_binary = cv2.threshold(number_roi,127,255,cv2.THRESH_BINARY_INV)
cv2.imwrite('number.jpg',number_binary)
cv_show('number_binary',number_binary)

#指定白名单进行OCR识别
print(pytesseract.image_to_string(Image.open('number.jpg'),lang='eng',config='psm 7 digits'))    #注意需要修改 Tesseract-OCR\tessdata\configs文件夹里的digits文件，将其修改为：tessedit_char_whitelist ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789


