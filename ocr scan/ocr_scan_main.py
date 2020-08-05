# tesseract模块下载地址：https://digi.bib.uni-mannheim.de/tesseract/
# 配置环境变量path如 E:\Program Files (x86)\Tesseract-OCR
# tesseract -v进行测试
# tesseract XXX.png 得到结果 
# pip install pytesseract
# 打开anaconda lib site-packges pytesseract pytesseract.py
# 将pytesseract.py中的tesseract_cmd 修改为绝对路径即可
import cv2
import scan
import sys
import pytesseract
from ocr_scan_ui import Ui_Widget
from PyQt5.QtWidgets import QApplication,QMessageBox
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage,QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PIL import Image


class Ocr_Scan(QtWidgets.QWidget,Ui_Widget):

    def _init_(self):
        super(Ocr_Scan, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("OCR识别")
        self.label_1.setText(" ")
        self.label_2.setText(" ")

        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        

        self.pushButton.clicked.connect(lambda:self.slot_btn_chooseImg())
        self.pushButton_2.clicked.connect(lambda : self.ocr_scan_deal())
        #self.pushButton_4.clicked.connect(lambda : self.())
        self.pushButton_3.clicked.connect(lambda : self.save_scaned_img())

   

    def slot_btn_chooseImg(self):   #选择图片
        global image,image_width,image_height
        files,filetype = QFileDialog.getOpenFileNames(self,"选择图片",filter = "ALL Fiels(*)")
        if files:
            print(files)
            self.pushButton_2.setEnabled(True)
            image = cv2.imread(files[0])
            image2 = image.copy()
            image3 = cv2.resize(image2,(0,0),fx=0.2,fy=0.2,interpolation=cv2.INTER_AREA)
            image_width = image3.shape[0]
            image_height = image3.shape[1]
            self.label1_image_show(image3)



    def label1_image_show(self,img):
        height, width, bytesPerComponent = img.shape   #返回的是图像的行数，列数，色彩通道数
        bytesPerLine = 3 * width    #每行的字节数        
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)         
        pixmap = QPixmap.fromImage(QImg)
        self.label_1.setPixmap(pixmap)
        print(img.shape[0],img.shape[1])
        self.label_1.update()
        


    
    def label2_image_show(self,img):
        height, width,bytesPerComponent= img.shape   #返回的是图像的行数，列数，色彩通道数
        bytesPerLine = 3 * width    #每行的字节数        
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height,bytesPerLine, QImage.Format_RGB888)         
        pixmap = QPixmap.fromImage(QImg)
        self.label_2.setPixmap(pixmap)



    def ocr_scan_deal(self):    #OCR识别
        global image,img2
       #cv2.imshow('image',image)
        img2=scan.scan_image(image)
        img3 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
        img4 = cv2.resize(img3,(image_height,image_width),interpolation=cv2.INTER_AREA)
        self.label2_image_show(img4)
     
        cv2.imwrite('ocr_scan.jpg',img3)
        text = pytesseract.image_to_string(Image.open('ocr_scan.jpg'))
        print(text)
        self.textEdit.setText(text)
        self.pushButton_3.setEnabled(True)
    def save_scaned_img(self):
        global img2
        cv2.imwrite('scan.jpg',img2)
        QMessageBox.information(self,'提示','已保存为scan.jpg',QMessageBox.Yes | QMessageBox.No)
    


    
        



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Ocr_Scan()
    w._init_()
    w.show()
    sys.exit(app.exec_())

