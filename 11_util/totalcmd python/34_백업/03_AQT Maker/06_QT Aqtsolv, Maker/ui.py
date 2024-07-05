# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'aqt_inputxfShsV.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QGroupBox,
                               QLabel, QMainWindow, QPushButton, QRadioButton,
                               QSizePolicy, QSpinBox, QStatusBar, QTextEdit,
                               QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(582, 841)
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"D2Coding"])
        MainWindow.setFont(font)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(40, 20, 141, 20))
        font1 = QFont()
        font1.setFamilies([u"D2Coding"])
        font1.setPointSize(11)
        self.checkBox.setFont(font1)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 50, 141, 21))
        self.label.setFont(font1)
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(30, 80, 521, 31))
        font2 = QFont()
        font2.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font2.setPointSize(10)
        self.textEdit.setFont(font2)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(340, 740, 211, 61))
        font3 = QFont()
        font3.setFamilies([u"Consolas"])
        font3.setPointSize(12)
        self.pushButton.setFont(font3)
        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(400, 30, 121, 41))
        self.spinBox.setFont(font1)
        self.spinBox.setAlignment(Qt.AlignCenter)
        self.spinBox.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox.setProperty("showGroupSeparator", False)
        self.spinBox.setValue(1)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(300, 40, 141, 21))
        self.label_2.setFont(font1)
        self.textEdit_2 = QTextEdit(self.centralwidget)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setGeometry(QRect(30, 160, 521, 31))
        self.textEdit_2.setFont(font2)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 130, 191, 21))
        font4 = QFont()
        font4.setFamilies([u"Consolas"])
        font4.setPointSize(11)
        self.label_3.setFont(font4)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(30, 310, 511, 391))
        self.groupBox.setFont(font1)
        self.radio1 = QRadioButton(self.groupBox)
        self.radio1.setObjectName(u"radio1")
        self.radio1.setGeometry(QRect(20, 40, 111, 20))
        font5 = QFont()
        font5.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font5.setPointSize(11)
        self.radio1.setFont(font5)
        self.radio2 = QRadioButton(self.groupBox)
        self.radio2.setObjectName(u"radio2")
        self.radio2.setGeometry(QRect(20, 70, 191, 20))
        self.radio2.setFont(font5)
        self.radio3 = QRadioButton(self.groupBox)
        self.radio3.setObjectName(u"radio3")
        self.radio3.setGeometry(QRect(20, 100, 191, 20))
        self.radio3.setFont(font5)
        self.radio4 = QRadioButton(self.groupBox)
        self.radio4.setObjectName(u"radio4")
        self.radio4.setGeometry(QRect(20, 130, 191, 20))
        self.radio4.setFont(font5)
        self.radio4.setChecked(True)
        self.radio5 = QRadioButton(self.groupBox)
        self.radio5.setObjectName(u"radio5")
        self.radio5.setGeometry(QRect(20, 160, 191, 20))
        self.radio5.setFont(font5)
        self.radio6 = QRadioButton(self.groupBox)
        self.radio6.setObjectName(u"radio6")
        self.radio6.setGeometry(QRect(20, 190, 191, 20))
        self.radio6.setFont(font5)
        self.radio7 = QRadioButton(self.groupBox)
        self.radio7.setObjectName(u"radio7")
        self.radio7.setGeometry(QRect(20, 220, 191, 20))
        self.radio7.setFont(font5)
        self.radio8 = QRadioButton(self.groupBox)
        self.radio8.setObjectName(u"radio8")
        self.radio8.setGeometry(QRect(20, 250, 221, 20))
        self.radio8.setFont(font5)
        self.radio9 = QRadioButton(self.groupBox)
        self.radio9.setObjectName(u"radio9")
        self.radio9.setGeometry(QRect(20, 280, 221, 20))
        self.radio9.setFont(font5)
        self.radio10 = QRadioButton(self.groupBox)
        self.radio10.setObjectName(u"radio10")
        self.radio10.setGeometry(QRect(20, 310, 221, 20))
        self.radio10.setFont(font5)
        self.radio10.setChecked(False)
        self.radio11 = QRadioButton(self.groupBox)
        self.radio11.setObjectName(u"radio11")
        self.radio11.setGeometry(QRect(20, 340, 221, 20))
        self.radio11.setFont(font5)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(40, 220, 141, 21))
        self.label_4.setFont(font4)
        self.textEdit_3 = QTextEdit(self.centralwidget)
        self.textEdit_3.setObjectName(u"textEdit_3")
        self.textEdit_3.setGeometry(QRect(30, 250, 521, 31))
        self.textEdit_3.setFont(font2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\ub2e8\uacc4\ud3ec\ud568", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\uc8fc\uc18c, Address", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\uad00\uc815\uc758 \uac2f\uc218", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Engireering Company", None))
        self.groupBox.setTitle(
            QCoreApplication.translate("MainWindow", u"\uc9c0\ud558\uc218 \uc601\ud5a5\uc870\uc0ac\uc790", None))
        self.radio1.setText(QCoreApplication.translate("MainWindow", u"\uc0b0\uc218\uac1c\ubc1c(\uc8fc)", None))
        self.radio2.setText(QCoreApplication.translate("MainWindow",
                                                       u"\ub300\uc6c5\uc5d4\uc9c0\ub2c8\uc5b4\ub9c1 \uc8fc\uc2dd\ud68c\uc0ac",
                                                       None))
        self.radio3.setText(
            QCoreApplication.translate("MainWindow", u"(\uc8fc)\uc6b0\uacbd\uc5d4\uc9c0\ub2c8\uc5b4\ub9c1", None))
        self.radio4.setText(
            QCoreApplication.translate("MainWindow", u"\uc8fc\uc2dd\ud68c\uc0ac \ud55c\uc77c\uc9c0\ud558\uc218", None))
        self.radio5.setText(
            QCoreApplication.translate("MainWindow", u"(\uc8fc)\ub3d9\ud574\uc5d4\uc9c0\ub2c8\uc5b4\ub9c1", None))
        self.radio6.setText(QCoreApplication.translate("MainWindow", u"(\uc8fc)\ud604\uc724\uc774\uc5d4\uc528", None))
        self.radio7.setText(QCoreApplication.translate("MainWindow", u"(\uc8fc)\ud0dc\uc591\uc774\uc5d4\uc9c0", None))
        self.radio8.setText(QCoreApplication.translate("MainWindow",
                                                       u"(\uc8fc)\ubd80\uc5ec\uc9c0\ud558\uc218\uac1c\ubc1c \uc8fc\uc2dd\ud68c\uc0ac",
                                                       None))
        self.radio9.setText(QCoreApplication.translate("MainWindow", u"(\uc8fc)\uc804\uc77c", None))
        self.radio10.setText(QCoreApplication.translate("MainWindow", u"\uc0bc\uc6d0\uac1c\ubc1c(\uc8fc)", None))
        self.radio11.setText(
            QCoreApplication.translate("MainWindow", u"\ub9c8\uc778\uc9c0\uc624 \uc8fc\uc2dd\ud68c\uc0ac", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Message", None))
    # retranslateUi
