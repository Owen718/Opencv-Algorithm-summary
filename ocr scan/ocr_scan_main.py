import cv2
import scan
import sys
from ocr_scan_ui import Ui_Widget
from PyQt5.QtWidgets import QApplication,QMessageBox
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage,QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

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
        #self.pushButton_4.clicked.connect(lambda : self.import_template())
        #self.pushButton_3.clicked.connect(lambda : self.credit_num_message())

   

    def slot_btn_chooseImg(self):   #选择图片
        global image
        files,filetype = QFileDialog.getOpenFileNames(self,"选择图片",filter = "ALL Fiels(*)")
        if files:
            print(files)
            self.pushButton_2.setEnabled(True)
            image = cv2.imread(files[0])
            image2 = image.copy()
            image2 = scan.resize(image2,width = int(image.shape[0] / 5) , height = int(image.shape[1] / 5))
            self.label1_image_show(image2)



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
        global image
        cv2.imshow('image',image)
        img2=scan.scan_image(image)
        img3 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
        img3 = scan.resize(img3,width = int(image.shape[0] / 3) , height = int(img3.shape[1] / 3))
        self.label2_image_show(img3)
        self.pushButton_3.setEnabled(True)

    


    
        



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Ocr_Scan()
    w._init_()
    w.show()
    sys.exit(app.exec_())

