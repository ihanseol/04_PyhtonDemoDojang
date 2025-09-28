# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_yangsooXbWdsw.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QLayout, QListView, QMainWindow,
                               QMenuBar, QPushButton, QSizePolicy, QStatusBar,
                               QTabWidget, QTextEdit, QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 677)
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 30, 611, 271))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.layoutWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.textEdit = QTextEdit(self.tab)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(20, 10, 571, 161))
        font1 = QFont()
        font1.setFamilies([u"Consolas"])
        font1.setPointSize(11)
        self.textEdit.setFont(font1)
        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(330, 180, 261, 51))
        self.pushButton_3 = QPushButton(self.tab)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(50, 180, 261, 51))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.pushButton_2 = QPushButton(self.tab_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(310, 180, 261, 51))
        self.pushButton_4 = QPushButton(self.tab_2)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(20, 180, 261, 51))
        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.layoutWidget_2 = QWidget(self.centralwidget)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 310, 611, 301))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.listView = QListView(self.layoutWidget_2)
        self.listView.setObjectName(u"listView")

        self.verticalLayout_2.addWidget(self.listView)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 640, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"\uc591\uc218\uc2dc\ud5d8 \uc790\ub3d9\ud654", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow",
                                                         u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                                         "p, li { white-space: pre-wrap; }\n"
                                                         "hr { height: 1px; border-width: 0; }\n"
                                                         "li.unchecked::marker { content: \"\\2610\"; }\n"
                                                         "li.checked::marker { content: \"\\2612\"; }\n"
                                                         "</style></head><body style=\" font-family:'Consolas'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\uc774\uac83\uc740, \uc591\uc218\uc2dc\ud5d8\uc77c\ubcf4\uc758 \uc790\ub3d9\ud654 \ud504\ub85c\uadf8\ub7a8\uc774\uba70 \uc2a4\ud15d\uc740 2\ub2e8\uacc4\ub85c \uad6c\uc131\ub418\uc5b4, 1\ub2e8\uacc4 \uc2a4\ud15d\uc740, YanSoo.XLSX \ud30c\uc77c\uc5d0\uc11c \ub370\uc774\ud130\ub97c \uc77d\uc5b4\uc640\uc11c \uc591\uc218\uc77c\ubcf4\ud30c\uc77c\uc5d0 \ub370\uc774\ud130\ub97c \uc5c5\ub370\uc774\ud2b8 \ud574"
                                                         "\uc8fc\ub294 1\ucc28\uacfc\uc815\uc774\uba70 2\ub2e8\uacc4 \uc2a4\ud15d\uc740, AqteSolver \ub97c \ub3cc\ub824\uc11c T,S\uac12\uc744 \uc5bb\ub294 \uacfc\uc815\uc744 \ud558\uac8c\ub41c\ub2e4.</p></body></html>",
                                                         None))
        self.textEdit.setPlaceholderText(QCoreApplication.translate("MainWindow",
                                                                    u"\uc774\uac83\uc740, \uc591\uc218\uc2dc\ud5d8\uc77c\ubcf4\uc758 \uc790\ub3d9\ud654 \ud504\ub85c\uadf8\ub7a8\uc774\uba70 \uc2a4\ud15d\uc740 2\ub2e8\uacc4\ub85c \uad6c\uc131\ub418\uc5b4, 1\ub2e8\uacc4 \uc2a4\ud15d\uc740, YanSoo.XLSX \ud30c\uc77c\uc5d0\uc11c \ub370\uc774\ud130\ub97c \uc77d\uc5b4\uc640\uc11c \uc591\uc218\uc77c\ubcf4\ud30c\uc77c\uc5d0 \ub370\uc774\ud130\ub97c \uc5c5\ub370\uc774\ud2b8 \ud574\uc8fc\ub294 1\ucc28\uacfc\uc815\uc774\uba70 2\ub2e8\uacc4 \uc2a4\ud15d\uc740, AqteSolver \ub97c \ub3cc\ub824\uc11c T,S\uac12\uc744 \uc5bb\ub294 \uacfc\uc815\uc744 \ud558\uac8c\ub41c\ub2e4.",
                                                                    None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Execute YanSoo FIrst Step", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),
                                  QCoreApplication.translate("MainWindow", u"YangSoo Test Step First", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Execute YanSoo Final Step", None))
        # if QT_CONFIG(shortcut)
        self.pushButton_2.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
        # endif // QT_CONFIG(shortcut)
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  QCoreApplication.translate("MainWindow", u"YangSoo Test Step Final", None))
    # retranslateUi
