
import sys
from credit_card_ui import Ui_Widget
from PyQt5.QtWidgets import QApplication,QMessageBox
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage,QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
import credit_card
import cv2


class PyQt5_Credit_Card(QtWidgets.QWidget,Ui_Widget):
    def _init_(self):
        super(PyQt5_Credit_Card, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("信用卡识别")
        self.label_1.setText(" ")
        self.label_2.setText(" ")

        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)

        self.pushButton.clicked.connect(lambda:self.slot_btn_chooseImg())
        self.pushButton_2.clicked.connect(lambda : self.credit_card_deal())
        self.pushButton_4.clicked.connect(lambda : self.import_template())
        self.pushButton_3.clicked.connect(lambda : self.credit_num_message())

   

    def slot_btn_chooseImg(self):   #选择图片
        global image
        files,filetype = QFileDialog.getOpenFileNames(self,"选择图片",filter = "ALL Fiels(*)")
        if files:
            print(files)
            self.pushButton_2.setEnabled(True)
            image = cv2.imread(files[0])
            image2 = image.copy()
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
        height, width, bytesPerComponent = img.shape   #返回的是图像的行数，列数，色彩通道数
        bytesPerLine = 3 * width    #每行的字节数        
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)         
        pixmap = QPixmap.fromImage(QImg)
        self.label_2.setPixmap(pixmap)

    def import_template(self):      #导入模板图片
        global img
        files,filetype = QFileDialog.getOpenFileNames(self,"选择图片",filter = "ALL Fiels(*)")
        if files:
            print(files)
            self.pushButton.setEnabled(True)
            img = cv2.imread(files[0])
            cv2.imshow("template",img)


    def credit_card_deal(self):    #信用卡图片识别
        global img,image,credit_num
        img2,credit_num = credit_card.cv_credit_card(img,image)
        self.label2_image_show(img2)
        self.pushButton_3.setEnabled(True)

    
    def credit_num_message(self):
        global credit_num
        QMessageBox.information(self, "信用卡卡号",str(credit_num),QMessageBox.Yes | QMessageBox.No)


    
        



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = PyQt5_Credit_Card()
    w._init_()
    w.show()
    sys.exit(app.exec_())
