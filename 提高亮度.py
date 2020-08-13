import cv2
import numpy as np

def enhance_lighted(img,k,b):  #RGB色彩空间下，线性提高图片亮度
    row,col,channel_num = img.shape
    img_lighted = np.zeros(img.shape,dtype = np.uint8)
    for x in range(row):
        for y in range(col):
            for i in range(channel_num):
                img_lighted[x,y,i] = k * img[x,y,i] + b
    return img_lighted


def enhance_lighted_2(img,k,b):
    img = img * k + b
    return np.uint8(img)

def hsv_light_enhance(hsvimg,k,b):  #hsv色彩空间洗下，利用v明度分量提高图片亮度
    hsvimg[:,:,2]=hsvimg[:,:,2] * k + b
    hsvimg = cv2.cvtColor(hsvimg,cv2.COLOR_HSV2BGR)
    return np.uint8(hsvimg)



def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread(r'C:\Users\Owen\Pictures\HCF-test.jpg')

#lighted_enhanced = enhance_lighted(img,1.5,10)

HSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
lighted_enhanced = hsv_light_enhance(HSV,1,10)



cv_show('ligted',lighted_enhanced)
