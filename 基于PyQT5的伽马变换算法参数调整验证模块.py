#基于PyQT5的图像算法参数调整验证模块

#Qslider（滑动条）控件的使用
from PyQt5.QtWidgets import  QVBoxLayout,QWidget,QApplication ,QHBoxLayout,QSpinBox,QSlider,QLabel,QHBoxLayout
from PyQt5.QtGui import QIcon,QPixmap,QFont,QImage
from PyQt5.QtCore import  Qt
import sys
import cv2
import math
from skimage import exposure
import numpy as np
def gamma_enhance(bgr,c,a):  #s=c*pow(r,a)
    (b,g,r) = cv2.split(bgr)
    for x in range(bgr.shape[0]):
        for y in range(bgr.shape[1]):
            b[x,y] = c * math.pow(b[x,y]/255,a) * 255
            g[x,y] = c * math.pow(g[x,y]/255,a) * 255
            r[x,y] = c * math.pow(r[x,y]/255,a) * 255

    img = cv2.merge((b,g,r))
    cv2.normalize(img,img,0,255,cv2.NORM_MINMAX)
    m_img=cv2.convertScaleAbs(img)
    return m_img

def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

class WindowClass(QWidget):

    def __init__(self,parent=None):

        super(WindowClass, self).__init__(parent)
        layout=QVBoxLayout()
    
        self.lider_widget1 = QWidget()
        self.lider_layout1 = QHBoxLayout()
        self.lider_widget2 = QWidget()
        self.lider_layout2 = QHBoxLayout()
                
        self.cv_label = QLabel()  #显示图片的标签

        #滑动条1
        self.slider1=QSlider(Qt.Horizontal)
        self.slider1.setMinimum(1)#滑条最小值
        self.slider1.setMaximum(50)#滑条最大值
        self.slider1.setSingleStep(1)#滑条步长
        self.slider1.setTickPosition(QSlider.TicksBelow)#设置刻度位置，在下方
        self.slider1.setTickInterval(1)#设置刻度间隔

        #滑动条1的值
        self.label1=QLabel()
        self.label1.setFont(QFont(None,10))
        self.label1.setNum(self.slider1.value())

        #设置水平分布
        self.lider_layout1.addWidget(self.slider1)
        self.lider_layout1.addWidget(self.label1)
        #设置容器
        self.lider_widget1.setLayout(self.lider_layout1)

        self.lider_widget2 = QWidget()
        self.lider_layout2 = QHBoxLayout()
        


        #滑动条2
        self.slider2=QSlider(Qt.Horizontal)
        self.slider2.setMinimum(1)#滑条2最小值
        self.slider2.setMaximum(50)#滑条2最大值
        self.slider2.setSingleStep(1)#滑条2步长
        self.slider2.setTickPosition(QSlider.TicksBelow)#设置刻度位置，在下方
        self.slider2.setTickInterval(1)#设置刻度间隔

         #滑动条2的值
        self.label2=QLabel()
        self.label2.setFont(QFont(None,10))
        self.label2.setNum(self.slider2.value())

        
        #设置水平分布
        self.lider_layout2.addWidget(self.slider2)
        self.lider_layout2.addWidget(self.label2)
        #设置容器
        self.lider_widget2.setLayout(self.lider_layout2)

        

        layout.addWidget(self.lider_widget1)
        layout.addWidget(self.lider_widget2)
        layout.addWidget(self.cv_label)

        self.resize(800,800)
        self.setLayout(layout)
        self.setWindowTitle("参数验证")

        #信号槽
        self.slider1.valueChanged.connect(self.valChange1)
        self.slider2.valueChanged.connect(self.valChange2)

        self.open_img()

    def valChange1(self):
        global original
        print(self.slider1.value()/10)
        self.label1.setNum(self.slider1.value()/10)
        #enhanced=gamma_enhance(original,self.slider1.value()/10,self.slider2.value()/10)
        enhanced=exposure.adjust_gamma(original,gamma=self.slider2.value()/10,gain=self.slider1.value()/10)
        self.label_image_show(enhanced)
        #cv_show('enhanced',enhanced)

    def valChange2(self):
        print(self.slider2.value()/10)
        self.label2.setNum(self.slider2.value()/10)
        enhanced=exposure.adjust_gamma(original,gamma=self.slider2.value()/10,gain=self.slider1.value()/10)
    

        self.label_image_show(enhanced)
        #cv_show('enhanced',enhanced)

    def label_image_show(self,img):
        height, width, bytesPerComponent = img.shape   #返回的是图像的行数，列数，色彩通道数
        bytesPerLine = 3 * width    #每行的字节数        
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)         
        pixmap = QPixmap.fromImage(QImg)
        self.cv_label.setPixmap(pixmap)
        print(img.shape[0],img.shape[1])
        self.cv_label.update()

    def open_img(self):       
        global original
        original = cv2.imread(r'C:\Users\Owen\Pictures\gamma_test.jpg')
        self.label_image_show(original)
        




if __name__=="__main__":
    app=QApplication(sys.argv)
    win=WindowClass()
    win.show()
    sys.exit(app.exec_())