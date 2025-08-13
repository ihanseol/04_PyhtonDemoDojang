# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'kakaomap_uiPifJXA.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPlainTextEdit,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(930, 516)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setModal(True)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 30, 211, 31))
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(11)
        self.label.setFont(font)
        self.textEdit = QTextEdit(Dialog)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(10, 60, 901, 51))
        font1 = QFont()
        font1.setPointSize(11)
        self.textEdit.setFont(font1)
        self.plainTextEdit = QPlainTextEdit(Dialog)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(10, 130, 901, 251))
        self.plainTextEdit.setFont(font1)
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(590, 440, 191, 51))
        self.pushButton.setFont(font)
        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(790, 440, 131, 51))
        self.pushButton_2.setFont(font)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Get TM Cordinate - Using KaKao API", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Address", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Get TM Cordinate", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi

