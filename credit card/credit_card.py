import cv2
import numpy as np
from imutils import contours
import argparse
import myutils



def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def cv_sobel_x(tophat):  #水平方向Sobel算子梯度滤波处理
    gradX=cv2.Sobel(tophat,ddepth = cv2.CV_32F,dx=1,dy=0,ksize=-1)
    gradX=np.absolute(gradX)
    (minVal,maxVal)=(np.min(gradX),np.max(gradX))
    gradX = (255*((gradX-minVal)/(maxVal-minVal)))
    gradX = gradX.astype("uint8")
    return gradX    





def cv_credit_card(img,image):
    FIRST_NUMBER = {  #字典
        "3":"American Express",
        "4":"Visa",
        "5":"MasterCart",
        "6":"Discover Card",
    }

    #cv_show('template',img)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#转为灰度图
    #cv_show('gray',gray)

    binary = cv2.threshold(gray,10,255,cv2.THRESH_BINARY_INV)[1] #注意阈值二值化函数返回的参数有两个！！
    #cv_show('binary',binary)


    #计算轮廓
    #cv2.findContours()函数接受的参数为二值图。cv2.RETR_EXTERNAL只检测最外围的图像，cv2.CHAIN_APPROX_SIMPLE只保留中点坐标
    #返回的list中每个元素都是图像中的一个轮廓

    refCnts,hierarchy = cv2.findContours(binary.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  

    cv2.drawContours(img,refCnts,-1,(0,0,255),3)  #画出轮廓
    #cv_show('img',img)

    #从左到右排序。0-9

    refCnts = myutils.sort_contours(refCnts,method="left-to-right")[0]
    digits= {}

    for (i,c) in enumerate(refCnts):
        #计算外接矩形
        (x,y,w,h) = cv2.boundingRect(c)
        #截取图像
        roi = binary[y:y+h,x:x+w]
        #重新设定大小
        roi = cv2.resize(roi,(57,88))
        #设定digits
        digits[i]=roi

    ###以上为模板的处理，以下为图片处理


    #初始化卷积核
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9,3))
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))

    #cv_show('image',image)
    image = myutils.resize(image,width=300)
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #转化为灰度图
    image_tophat = cv2.morphologyEx(image_gray,cv2.MORPH_TOPHAT,rectKernel)  #礼帽处理，突出更明亮的区域
    #cv_show('tophat',image_tophat)

    gradX = cv_sobel_x(image_tophat)  #水平方向梯度滤波处理
    #cv_show('gradX',gradX)

    gradX = cv2.morphologyEx(gradX,cv2.MORPH_CLOSE,rectKernel) #闭操作，让数字连在一起
    #cv_show('gradX_MORPH_CLOSE',gradX)

    image_threshold = cv2.threshold(gradX,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]  #THRESH_OTSU自动寻找合适的阈值，适合双峰，需把阈值下限设为0
    #cv_show('image_threshold',image_threshold)

    image_threshold = cv2.morphologyEx(image_threshold,cv2.MORPH_CLOSE,sqKernel)



    threshCnts,hierarchy = cv2.findContours(image_threshold.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #计算最外层轮廓

    cnts = threshCnts
    cur_img = image.copy()
    cv2.drawContours(cur_img,cnts,-1,(0,0,255),3)  #画出轮廓
    #cv_show('cur_img',cur_img)  

    locs=[]  #轮廓位置


    for (i,c) in enumerate(cnts):
        (x,y,w,h) = cv2.boundingRect(c)  #寻找矩形
        ar = w/float(h)  #求宽和高的比例

        if ar>2.5 and ar<4.0:  #把不符合的筛出去
            if(w>40 and w <55)and(h>10 and h <20):
                locs.append((x,y,w,h))   


    locs = sorted(locs,key=lambda x:x[0])  #排个序


    output = []

    for (i,(gX,gY,gW,gH)) in enumerate(locs):
        groupOutput = []
        group = image_gray[gY - 5:gY + gH + 5,gX-5:gX + gW + 5]

        group = cv2.threshold(group,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]  #自适应二值化处理
        digitCnts,hierarchy = cv2.findContours(group.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #计算最外层轮廓
        digitCnts = contours.sort_contours(digitCnts,method = "left-to-right")[0]
        for c in digitCnts:
            (x,y,w,h) = cv2.boundingRect(c)
            roi = group[y:y+h,x:x+w]
            roi = cv2.resize(roi,(57,88))
            #cv_show('roi',roi)
            #print(roi)

            #匹配度
            scores=[]
            
            for (digit,digitROI) in digits.items(): #遍历求匹配度,在模板中计算每一个得分
                result = cv2.matchTemplate(roi,digitROI,cv2.TM_CCOEFF)
                (_,score,_,_) = cv2.minMaxLoc(result)
                scores.append(score)
            #得到最合适的数字
            groupOutput.append(str(np.argmax(scores)))

        #画出来
        cv2.rectangle(image,(gX-5,gY-5),(gX+gW+5,gY+gH+5),(0,0,255),1)
        cv2.putText(image, "".join(groupOutput),(gX,gY-15),cv2.FONT_HERSHEY_SIMPLEX,0.65,(0,0,255),2)

        output.extend(groupOutput)

    return image,output

