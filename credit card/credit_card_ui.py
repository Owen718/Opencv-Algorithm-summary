

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Widget(object):
    def setupUi(self, Widget):

        Widget.setObjectName("Widget")

        self.groupBox = QtWidgets.QGroupBox()     #QGroupBox为widgets容器，layout（布局）添加进控件后，给容器设定布局。控件->layout->QgroupBox->llayout(二级布局)->lwidget(二级容器)->总布局
        self.groupBox.setObjectName("groupBox")
        self.label_1 = QtWidgets.QLabel()
        self.label_1.setObjectName("label_1")
        self.cv_layout = QtWidgets.QHBoxLayout()
        self.cv_layout.addWidget(self.label_1)
        self.groupBox.setLayout(self.cv_layout)



        self.groupBox_2 = QtWidgets.QGroupBox()
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_2 = QtWidgets.QLabel()
        self.label_2.setObjectName("label_2")
        self.cv_layout2 = QtWidgets.QHBoxLayout()
        self.cv_layout2.addWidget(self.label_2)
        self.groupBox_2.setLayout(self.cv_layout2)



        self.llayout = QtWidgets.QVBoxLayout()
        self.llayout.addWidget(self.groupBox)
        self.llayout.addWidget(self.groupBox_2)

        self.lwidget = QtWidgets.QWidget(Widget)
        self.lwidget.setLayout(self.llayout)
        




        self.widget = QtWidgets.QWidget(Widget)
        self.widget.setObjectName("widget")



        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setObjectName("pushButton_4")

        self.rlayout = QtWidgets.QVBoxLayout()
        self.rlayout.addWidget(self.pushButton_4)
        self.rlayout.addWidget(self.pushButton)
        self.rlayout.addWidget(self.pushButton_2)
        self.rlayout.addWidget(self.pushButton_3)

        self.rwidget = QtWidgets.QWidget()
        self.rwidget.setLayout(self.rlayout)



    
        self.alllayout = QtWidgets.QHBoxLayout()
        self.alllayout.addWidget(self.lwidget)
        self.alllayout.addWidget(self.rwidget)

        Widget.setLayout(self.alllayout)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.groupBox.setTitle(_translate("Widget", "原始图片"))
        self.label_1.setText(_translate("Widget", "TextLabel"))
        self.groupBox_2.setTitle(_translate("Widget", "识别结果"))
        self.label_2.setText(_translate("Widget", "TextLabel"))
        self.pushButton.setText(_translate("Widget", "打开图片"))
        self.pushButton_2.setText(_translate("Widget", "识别卡号"))
        self.pushButton_3.setText(_translate("Widget", "输出结果"))
        self.pushButton_4.setText(_translate("Widget","导入识别模板"))

