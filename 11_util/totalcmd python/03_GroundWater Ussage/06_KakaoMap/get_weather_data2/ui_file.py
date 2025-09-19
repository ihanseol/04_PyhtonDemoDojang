# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Retrieve Weater DataBIDjgc.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGroupBox,
                               QHBoxLayout, QListView, QMainWindow, QPushButton,
                               QSizePolicy, QStatusBar, QTabWidget, QVBoxLayout,
                               QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1389, 937)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"D2Coding ligature"])
        font.setPointSize(11)
        MainWindow.setFont(font)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(9, 9, 1371, 911))
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 1091, 231))
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setMaximumSize(QSize(1075, 380))
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 30, 621, 61))
        self.horizontalLayout_1 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_1.setObjectName(u"horizontalLayout_1")
        self.horizontalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.checkBox_1 = QCheckBox(self.layoutWidget)
        self.checkBox_1.setObjectName(u"checkBox_1")

        self.horizontalLayout_1.addWidget(self.checkBox_1)

        self.checkBox_2 = QCheckBox(self.layoutWidget)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_1.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.layoutWidget)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.horizontalLayout_1.addWidget(self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.layoutWidget)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.horizontalLayout_1.addWidget(self.checkBox_4)

        self.checkBox_5 = QCheckBox(self.layoutWidget)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.horizontalLayout_1.addWidget(self.checkBox_5)

        self.checkBox_6 = QCheckBox(self.layoutWidget)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.horizontalLayout_1.addWidget(self.checkBox_6)

        self.checkBox_7 = QCheckBox(self.layoutWidget)
        self.checkBox_7.setObjectName(u"checkBox_7")

        self.horizontalLayout_1.addWidget(self.checkBox_7)

        self.verticalLayout.addWidget(self.groupBox)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.groupBox_2 = QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 10, 1031, 181))
        self.layoutWidget_2 = QWidget(self.groupBox_2)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(30, 30, 951, 51))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.checkBox_8 = QCheckBox(self.layoutWidget_2)
        self.checkBox_8.setObjectName(u"checkBox_8")

        self.horizontalLayout_2.addWidget(self.checkBox_8)

        self.checkBox_9 = QCheckBox(self.layoutWidget_2)
        self.checkBox_9.setObjectName(u"checkBox_9")

        self.horizontalLayout_2.addWidget(self.checkBox_9)

        self.checkBox_10 = QCheckBox(self.layoutWidget_2)
        self.checkBox_10.setObjectName(u"checkBox_10")

        self.horizontalLayout_2.addWidget(self.checkBox_10)

        self.checkBox_11 = QCheckBox(self.layoutWidget_2)
        self.checkBox_11.setObjectName(u"checkBox_11")

        self.horizontalLayout_2.addWidget(self.checkBox_11)

        self.checkBox_13 = QCheckBox(self.layoutWidget_2)
        self.checkBox_13.setObjectName(u"checkBox_13")

        self.horizontalLayout_2.addWidget(self.checkBox_13)

        self.checkBox_14 = QCheckBox(self.layoutWidget_2)
        self.checkBox_14.setObjectName(u"checkBox_14")

        self.horizontalLayout_2.addWidget(self.checkBox_14)

        self.checkBox_15 = QCheckBox(self.layoutWidget_2)
        self.checkBox_15.setObjectName(u"checkBox_15")

        self.horizontalLayout_2.addWidget(self.checkBox_15)

        self.checkBox_16 = QCheckBox(self.layoutWidget_2)
        self.checkBox_16.setObjectName(u"checkBox_16")

        self.horizontalLayout_2.addWidget(self.checkBox_16)

        self.checkBox_17 = QCheckBox(self.layoutWidget_2)
        self.checkBox_17.setObjectName(u"checkBox_17")

        self.horizontalLayout_2.addWidget(self.checkBox_17)

        self.checkBox_18 = QCheckBox(self.layoutWidget_2)
        self.checkBox_18.setObjectName(u"checkBox_18")

        self.horizontalLayout_2.addWidget(self.checkBox_18)

        self.checkBox_19 = QCheckBox(self.layoutWidget_2)
        self.checkBox_19.setObjectName(u"checkBox_19")

        self.horizontalLayout_2.addWidget(self.checkBox_19)

        self.layoutWidget_9 = QWidget(self.groupBox_2)
        self.layoutWidget_9.setObjectName(u"layoutWidget_9")
        self.layoutWidget_9.setGeometry(QRect(30, 90, 531, 51))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget_9)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.checkBox_20 = QCheckBox(self.layoutWidget_9)
        self.checkBox_20.setObjectName(u"checkBox_20")

        self.horizontalLayout_3.addWidget(self.checkBox_20)

        self.checkBox_21 = QCheckBox(self.layoutWidget_9)
        self.checkBox_21.setObjectName(u"checkBox_21")

        self.horizontalLayout_3.addWidget(self.checkBox_21)

        self.checkBox_22 = QCheckBox(self.layoutWidget_9)
        self.checkBox_22.setObjectName(u"checkBox_22")

        self.horizontalLayout_3.addWidget(self.checkBox_22)

        self.checkBox_23 = QCheckBox(self.layoutWidget_9)
        self.checkBox_23.setObjectName(u"checkBox_23")

        self.horizontalLayout_3.addWidget(self.checkBox_23)

        self.checkBox_24 = QCheckBox(self.layoutWidget_9)
        self.checkBox_24.setObjectName(u"checkBox_24")

        self.horizontalLayout_3.addWidget(self.checkBox_24)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.groupBox_3 = QGroupBox(self.tab_3)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 10, 1051, 161))
        self.layoutWidget_3 = QWidget(self.groupBox_3)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(20, 40, 811, 51))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.checkBox_25 = QCheckBox(self.layoutWidget_3)
        self.checkBox_25.setObjectName(u"checkBox_25")

        self.horizontalLayout_4.addWidget(self.checkBox_25)

        self.checkBox_26 = QCheckBox(self.layoutWidget_3)
        self.checkBox_26.setObjectName(u"checkBox_26")

        self.horizontalLayout_4.addWidget(self.checkBox_26)

        self.checkBox_27 = QCheckBox(self.layoutWidget_3)
        self.checkBox_27.setObjectName(u"checkBox_27")

        self.horizontalLayout_4.addWidget(self.checkBox_27)

        self.checkBox_28 = QCheckBox(self.layoutWidget_3)
        self.checkBox_28.setObjectName(u"checkBox_28")

        self.horizontalLayout_4.addWidget(self.checkBox_28)

        self.checkBox_29 = QCheckBox(self.layoutWidget_3)
        self.checkBox_29.setObjectName(u"checkBox_29")

        self.horizontalLayout_4.addWidget(self.checkBox_29)

        self.checkBox_30 = QCheckBox(self.layoutWidget_3)
        self.checkBox_30.setObjectName(u"checkBox_30")

        self.horizontalLayout_4.addWidget(self.checkBox_30)

        self.checkBox_31 = QCheckBox(self.layoutWidget_3)
        self.checkBox_31.setObjectName(u"checkBox_31")

        self.horizontalLayout_4.addWidget(self.checkBox_31)

        self.checkBox_32 = QCheckBox(self.layoutWidget_3)
        self.checkBox_32.setObjectName(u"checkBox_32")

        self.horizontalLayout_4.addWidget(self.checkBox_32)

        self.checkBox_33 = QCheckBox(self.layoutWidget_3)
        self.checkBox_33.setObjectName(u"checkBox_33")

        self.horizontalLayout_4.addWidget(self.checkBox_33)

        self.checkBox_34 = QCheckBox(self.layoutWidget_3)
        self.checkBox_34.setObjectName(u"checkBox_34")

        self.horizontalLayout_4.addWidget(self.checkBox_34)

        self.layoutWidget_10 = QWidget(self.groupBox_3)
        self.layoutWidget_10.setObjectName(u"layoutWidget_10")
        self.layoutWidget_10.setGeometry(QRect(20, 90, 351, 51))
        self.horizontalLayout_5 = QHBoxLayout(self.layoutWidget_10)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.checkBox_35 = QCheckBox(self.layoutWidget_10)
        self.checkBox_35.setObjectName(u"checkBox_35")

        self.horizontalLayout_5.addWidget(self.checkBox_35)

        self.checkBox_36 = QCheckBox(self.layoutWidget_10)
        self.checkBox_36.setObjectName(u"checkBox_36")

        self.horizontalLayout_5.addWidget(self.checkBox_36)

        self.checkBox_37 = QCheckBox(self.layoutWidget_10)
        self.checkBox_37.setObjectName(u"checkBox_37")

        self.horizontalLayout_5.addWidget(self.checkBox_37)

        self.checkBox_38 = QCheckBox(self.layoutWidget_10)
        self.checkBox_38.setObjectName(u"checkBox_38")

        self.horizontalLayout_5.addWidget(self.checkBox_38)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.groupBox_4 = QGroupBox(self.tab_4)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(9, 10, 1061, 181))
        self.layoutWidget_4 = QWidget(self.groupBox_4)
        self.layoutWidget_4.setObjectName(u"layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(20, 20, 861, 51))
        self.horizontalLayout_6 = QHBoxLayout(self.layoutWidget_4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.checkBox_39 = QCheckBox(self.layoutWidget_4)
        self.checkBox_39.setObjectName(u"checkBox_39")

        self.horizontalLayout_6.addWidget(self.checkBox_39)

        self.checkBox_40 = QCheckBox(self.layoutWidget_4)
        self.checkBox_40.setObjectName(u"checkBox_40")

        self.horizontalLayout_6.addWidget(self.checkBox_40)

        self.checkBox_41 = QCheckBox(self.layoutWidget_4)
        self.checkBox_41.setObjectName(u"checkBox_41")

        self.horizontalLayout_6.addWidget(self.checkBox_41)

        self.checkBox_42 = QCheckBox(self.layoutWidget_4)
        self.checkBox_42.setObjectName(u"checkBox_42")

        self.horizontalLayout_6.addWidget(self.checkBox_42)

        self.checkBox_43 = QCheckBox(self.layoutWidget_4)
        self.checkBox_43.setObjectName(u"checkBox_43")

        self.horizontalLayout_6.addWidget(self.checkBox_43)

        self.checkBox_44 = QCheckBox(self.layoutWidget_4)
        self.checkBox_44.setObjectName(u"checkBox_44")

        self.horizontalLayout_6.addWidget(self.checkBox_44)

        self.checkBox_45 = QCheckBox(self.layoutWidget_4)
        self.checkBox_45.setObjectName(u"checkBox_45")

        self.horizontalLayout_6.addWidget(self.checkBox_45)

        self.checkBox_46 = QCheckBox(self.layoutWidget_4)
        self.checkBox_46.setObjectName(u"checkBox_46")

        self.horizontalLayout_6.addWidget(self.checkBox_46)

        self.checkBox_47 = QCheckBox(self.layoutWidget_4)
        self.checkBox_47.setObjectName(u"checkBox_47")

        self.horizontalLayout_6.addWidget(self.checkBox_47)

        self.checkBox_48 = QCheckBox(self.layoutWidget_4)
        self.checkBox_48.setObjectName(u"checkBox_48")

        self.horizontalLayout_6.addWidget(self.checkBox_48)

        self.layoutWidget_7 = QWidget(self.groupBox_4)
        self.layoutWidget_7.setObjectName(u"layoutWidget_7")
        self.layoutWidget_7.setGeometry(QRect(20, 120, 861, 51))
        self.horizontalLayout_8 = QHBoxLayout(self.layoutWidget_7)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.checkBox_59 = QCheckBox(self.layoutWidget_7)
        self.checkBox_59.setObjectName(u"checkBox_59")

        self.horizontalLayout_8.addWidget(self.checkBox_59)

        self.checkBox_60 = QCheckBox(self.layoutWidget_7)
        self.checkBox_60.setObjectName(u"checkBox_60")

        self.horizontalLayout_8.addWidget(self.checkBox_60)

        self.checkBox_61 = QCheckBox(self.layoutWidget_7)
        self.checkBox_61.setObjectName(u"checkBox_61")

        self.horizontalLayout_8.addWidget(self.checkBox_61)

        self.checkBox_62 = QCheckBox(self.layoutWidget_7)
        self.checkBox_62.setObjectName(u"checkBox_62")

        self.horizontalLayout_8.addWidget(self.checkBox_62)

        self.checkBox_63 = QCheckBox(self.layoutWidget_7)
        self.checkBox_63.setObjectName(u"checkBox_63")

        self.horizontalLayout_8.addWidget(self.checkBox_63)

        self.checkBox_64 = QCheckBox(self.layoutWidget_7)
        self.checkBox_64.setObjectName(u"checkBox_64")

        self.horizontalLayout_8.addWidget(self.checkBox_64)

        self.checkBox_65 = QCheckBox(self.layoutWidget_7)
        self.checkBox_65.setObjectName(u"checkBox_65")

        self.horizontalLayout_8.addWidget(self.checkBox_65)

        self.layoutWidget_6 = QWidget(self.groupBox_4)
        self.layoutWidget_6.setObjectName(u"layoutWidget_6")
        self.layoutWidget_6.setGeometry(QRect(20, 70, 861, 51))
        self.horizontalLayout_7 = QHBoxLayout(self.layoutWidget_6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.checkBox_49 = QCheckBox(self.layoutWidget_6)
        self.checkBox_49.setObjectName(u"checkBox_49")

        self.horizontalLayout_7.addWidget(self.checkBox_49)

        self.checkBox_50 = QCheckBox(self.layoutWidget_6)
        self.checkBox_50.setObjectName(u"checkBox_50")

        self.horizontalLayout_7.addWidget(self.checkBox_50)

        self.checkBox_51 = QCheckBox(self.layoutWidget_6)
        self.checkBox_51.setObjectName(u"checkBox_51")

        self.horizontalLayout_7.addWidget(self.checkBox_51)

        self.checkBox_52 = QCheckBox(self.layoutWidget_6)
        self.checkBox_52.setObjectName(u"checkBox_52")

        self.horizontalLayout_7.addWidget(self.checkBox_52)

        self.checkBox_53 = QCheckBox(self.layoutWidget_6)
        self.checkBox_53.setObjectName(u"checkBox_53")

        self.horizontalLayout_7.addWidget(self.checkBox_53)

        self.checkBox_54 = QCheckBox(self.layoutWidget_6)
        self.checkBox_54.setObjectName(u"checkBox_54")

        self.horizontalLayout_7.addWidget(self.checkBox_54)

        self.checkBox_55 = QCheckBox(self.layoutWidget_6)
        self.checkBox_55.setObjectName(u"checkBox_55")

        self.horizontalLayout_7.addWidget(self.checkBox_55)

        self.checkBox_56 = QCheckBox(self.layoutWidget_6)
        self.checkBox_56.setObjectName(u"checkBox_56")

        self.horizontalLayout_7.addWidget(self.checkBox_56)

        self.checkBox_57 = QCheckBox(self.layoutWidget_6)
        self.checkBox_57.setObjectName(u"checkBox_57")

        self.horizontalLayout_7.addWidget(self.checkBox_57)

        self.checkBox_58 = QCheckBox(self.layoutWidget_6)
        self.checkBox_58.setObjectName(u"checkBox_58")

        self.horizontalLayout_7.addWidget(self.checkBox_58)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.groupBox_5 = QGroupBox(self.tab_5)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(9, 9, 1071, 191))
        self.layoutWidget_5 = QWidget(self.groupBox_5)
        self.layoutWidget_5.setObjectName(u"layoutWidget_5")
        self.layoutWidget_5.setGeometry(QRect(20, 30, 991, 51))
        self.horizontalLayout_9 = QHBoxLayout(self.layoutWidget_5)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.checkBox_66 = QCheckBox(self.layoutWidget_5)
        self.checkBox_66.setObjectName(u"checkBox_66")

        self.horizontalLayout_9.addWidget(self.checkBox_66)

        self.checkBox_67 = QCheckBox(self.layoutWidget_5)
        self.checkBox_67.setObjectName(u"checkBox_67")

        self.horizontalLayout_9.addWidget(self.checkBox_67)

        self.checkBox_68 = QCheckBox(self.layoutWidget_5)
        self.checkBox_68.setObjectName(u"checkBox_68")

        self.horizontalLayout_9.addWidget(self.checkBox_68)

        self.checkBox_69 = QCheckBox(self.layoutWidget_5)
        self.checkBox_69.setObjectName(u"checkBox_69")

        self.horizontalLayout_9.addWidget(self.checkBox_69)

        self.checkBox_70 = QCheckBox(self.layoutWidget_5)
        self.checkBox_70.setObjectName(u"checkBox_70")

        self.horizontalLayout_9.addWidget(self.checkBox_70)

        self.checkBox_71 = QCheckBox(self.layoutWidget_5)
        self.checkBox_71.setObjectName(u"checkBox_71")

        self.horizontalLayout_9.addWidget(self.checkBox_71)

        self.checkBox_72 = QCheckBox(self.layoutWidget_5)
        self.checkBox_72.setObjectName(u"checkBox_72")

        self.horizontalLayout_9.addWidget(self.checkBox_72)

        self.checkBox_73 = QCheckBox(self.layoutWidget_5)
        self.checkBox_73.setObjectName(u"checkBox_73")

        self.horizontalLayout_9.addWidget(self.checkBox_73)

        self.checkBox_74 = QCheckBox(self.layoutWidget_5)
        self.checkBox_74.setObjectName(u"checkBox_74")

        self.horizontalLayout_9.addWidget(self.checkBox_74)

        self.checkBox_75 = QCheckBox(self.layoutWidget_5)
        self.checkBox_75.setObjectName(u"checkBox_75")

        self.horizontalLayout_9.addWidget(self.checkBox_75)

        self.checkBox_76 = QCheckBox(self.layoutWidget_5)
        self.checkBox_76.setObjectName(u"checkBox_76")

        self.horizontalLayout_9.addWidget(self.checkBox_76)

        self.layoutWidget_12 = QWidget(self.groupBox_5)
        self.layoutWidget_12.setObjectName(u"layoutWidget_12")
        self.layoutWidget_12.setGeometry(QRect(20, 130, 991, 51))
        self.horizontalLayout_11 = QHBoxLayout(self.layoutWidget_12)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.checkBox_88 = QCheckBox(self.layoutWidget_12)
        self.checkBox_88.setObjectName(u"checkBox_88")

        self.horizontalLayout_11.addWidget(self.checkBox_88)

        self.checkBox_89 = QCheckBox(self.layoutWidget_12)
        self.checkBox_89.setObjectName(u"checkBox_89")

        self.horizontalLayout_11.addWidget(self.checkBox_89)

        self.checkBox_90 = QCheckBox(self.layoutWidget_12)
        self.checkBox_90.setObjectName(u"checkBox_90")

        self.horizontalLayout_11.addWidget(self.checkBox_90)

        self.checkBox_91 = QCheckBox(self.layoutWidget_12)
        self.checkBox_91.setObjectName(u"checkBox_91")

        self.horizontalLayout_11.addWidget(self.checkBox_91)

        self.checkBox_92 = QCheckBox(self.layoutWidget_12)
        self.checkBox_92.setObjectName(u"checkBox_92")

        self.horizontalLayout_11.addWidget(self.checkBox_92)

        self.checkBox_93 = QCheckBox(self.layoutWidget_12)
        self.checkBox_93.setObjectName(u"checkBox_93")

        self.horizontalLayout_11.addWidget(self.checkBox_93)

        self.checkBox_94 = QCheckBox(self.layoutWidget_12)
        self.checkBox_94.setObjectName(u"checkBox_94")

        self.horizontalLayout_11.addWidget(self.checkBox_94)

        self.checkBox_95 = QCheckBox(self.layoutWidget_12)
        self.checkBox_95.setObjectName(u"checkBox_95")

        self.horizontalLayout_11.addWidget(self.checkBox_95)

        self.checkBox_96 = QCheckBox(self.layoutWidget_12)
        self.checkBox_96.setObjectName(u"checkBox_96")

        self.horizontalLayout_11.addWidget(self.checkBox_96)

        self.checkBox_97 = QCheckBox(self.layoutWidget_12)
        self.checkBox_97.setObjectName(u"checkBox_97")

        self.horizontalLayout_11.addWidget(self.checkBox_97)

        self.layoutWidget_11 = QWidget(self.groupBox_5)
        self.layoutWidget_11.setObjectName(u"layoutWidget_11")
        self.layoutWidget_11.setGeometry(QRect(20, 80, 991, 51))
        self.horizontalLayout_10 = QHBoxLayout(self.layoutWidget_11)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.checkBox_77 = QCheckBox(self.layoutWidget_11)
        self.checkBox_77.setObjectName(u"checkBox_77")

        self.horizontalLayout_10.addWidget(self.checkBox_77)

        self.checkBox_78 = QCheckBox(self.layoutWidget_11)
        self.checkBox_78.setObjectName(u"checkBox_78")

        self.horizontalLayout_10.addWidget(self.checkBox_78)

        self.checkBox_79 = QCheckBox(self.layoutWidget_11)
        self.checkBox_79.setObjectName(u"checkBox_79")

        self.horizontalLayout_10.addWidget(self.checkBox_79)

        self.checkBox_80 = QCheckBox(self.layoutWidget_11)
        self.checkBox_80.setObjectName(u"checkBox_80")

        self.horizontalLayout_10.addWidget(self.checkBox_80)

        self.checkBox_81 = QCheckBox(self.layoutWidget_11)
        self.checkBox_81.setObjectName(u"checkBox_81")

        self.horizontalLayout_10.addWidget(self.checkBox_81)

        self.checkBox_82 = QCheckBox(self.layoutWidget_11)
        self.checkBox_82.setObjectName(u"checkBox_82")

        self.horizontalLayout_10.addWidget(self.checkBox_82)

        self.checkBox_83 = QCheckBox(self.layoutWidget_11)
        self.checkBox_83.setObjectName(u"checkBox_83")

        self.horizontalLayout_10.addWidget(self.checkBox_83)

        self.checkBox_84 = QCheckBox(self.layoutWidget_11)
        self.checkBox_84.setObjectName(u"checkBox_84")

        self.horizontalLayout_10.addWidget(self.checkBox_84)

        self.checkBox_85 = QCheckBox(self.layoutWidget_11)
        self.checkBox_85.setObjectName(u"checkBox_85")

        self.horizontalLayout_10.addWidget(self.checkBox_85)

        self.checkBox_86 = QCheckBox(self.layoutWidget_11)
        self.checkBox_86.setObjectName(u"checkBox_86")

        self.horizontalLayout_10.addWidget(self.checkBox_86)

        self.checkBox_87 = QCheckBox(self.layoutWidget_11)
        self.checkBox_87.setObjectName(u"checkBox_87")

        self.horizontalLayout_10.addWidget(self.checkBox_87)

        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.groupBox_6 = QGroupBox(self.tab_6)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(10, 10, 1061, 181))
        self.layoutWidget_8 = QWidget(self.groupBox_6)
        self.layoutWidget_8.setObjectName(u"layoutWidget_8")
        self.layoutWidget_8.setGeometry(QRect(20, 40, 591, 51))
        self.horizontalLayout_14 = QHBoxLayout(self.layoutWidget_8)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.checkBox_98 = QCheckBox(self.layoutWidget_8)
        self.checkBox_98.setObjectName(u"checkBox_98")

        self.horizontalLayout_14.addWidget(self.checkBox_98)

        self.checkBox_99 = QCheckBox(self.layoutWidget_8)
        self.checkBox_99.setObjectName(u"checkBox_99")

        self.horizontalLayout_14.addWidget(self.checkBox_99)

        self.checkBox_100 = QCheckBox(self.layoutWidget_8)
        self.checkBox_100.setObjectName(u"checkBox_100")

        self.horizontalLayout_14.addWidget(self.checkBox_100)

        self.checkBox_101 = QCheckBox(self.layoutWidget_8)
        self.checkBox_101.setObjectName(u"checkBox_101")

        self.horizontalLayout_14.addWidget(self.checkBox_101)

        self.checkBox_102 = QCheckBox(self.layoutWidget_8)
        self.checkBox_102.setObjectName(u"checkBox_102")

        self.horizontalLayout_14.addWidget(self.checkBox_102)

        self.checkBox_103 = QCheckBox(self.layoutWidget_8)
        self.checkBox_103.setObjectName(u"checkBox_103")

        self.horizontalLayout_14.addWidget(self.checkBox_103)

        self.tabWidget.addTab(self.tab_6, "")
        self.listView = QListView(self.frame)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(10, 260, 211, 641))
        self.listView_info = QListView(self.frame)
        self.listView_info.setObjectName(u"listView_info")
        self.listView_info.setGeometry(QRect(230, 260, 871, 641))
        self.pushButton_4 = QPushButton(self.frame)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(1120, 830, 231, 61))
        font1 = QFont()
        font1.setFamilies([u"Consolas"])
        font1.setPointSize(11)
        self.pushButton_4.setFont(font1)
        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(1120, 40, 231, 211))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy1)
        self.pushButton_2.setFont(font1)

        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.widget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy1.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy1)
        self.pushButton_3.setFont(font1)

        self.verticalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_1 = QPushButton(self.widget)
        self.pushButton_1.setObjectName(u"pushButton_1")
        sizePolicy1.setHeightForWidth(self.pushButton_1.sizePolicy().hasHeightForWidth())
        self.pushButton_1.setSizePolicy(sizePolicy1)
        self.pushButton_1.setFont(font1)

        self.verticalLayout_2.addWidget(self.pushButton_1)

        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy1.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy1)
        self.pushButton_5.setFont(font1)

        self.verticalLayout_2.addWidget(self.pushButton_5)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(2)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"30 Year RainFall Data Gathering ...", None))
        self.groupBox.setTitle(
            QCoreApplication.translate("MainWindow", u"\uc11c\uc6b8, \uacbd\uae30 \uc9c0\uc5ed\uc120\ud0dd", None))
        self.checkBox_1.setText(QCoreApplication.translate("MainWindow", u"\ubc31\ub839\ub3c4", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\uc11c\uc6b8", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"\uc778\ucc9c", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"\ub3d9\ub450\ucc9c", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"\uad00\uc545\uc0b0", None))
        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"\uc218\uc6d0", None))
        self.checkBox_7.setText(QCoreApplication.translate("MainWindow", u"\uac15\ud654", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),
                                  QCoreApplication.translate("MainWindow", u"\uc11c\uc6b8,\uacbd\uae30", None))
        self.groupBox_2.setTitle(
            QCoreApplication.translate("MainWindow", u"\uac15\uc6d0\ub3c4, \uc9c0\uc5ed\uc120\ud0dd", None))
        self.checkBox_8.setText(QCoreApplication.translate("MainWindow", u"\uac15\ub989", None))
        self.checkBox_9.setText(QCoreApplication.translate("MainWindow", u"\ub300\uad00\ub839", None))
        self.checkBox_10.setText(QCoreApplication.translate("MainWindow", u"\ub3d9\ud574", None))
        self.checkBox_11.setText(QCoreApplication.translate("MainWindow", u"\ubd81\uac15\ub989", None))
        self.checkBox_13.setText(QCoreApplication.translate("MainWindow", u"\ubd81\ucd98\ucc9c", None))
        self.checkBox_14.setText(QCoreApplication.translate("MainWindow", u"\uc0bc\ucc99", None))
        self.checkBox_15.setText(QCoreApplication.translate("MainWindow", u"\uc18d\ucd08", None))
        self.checkBox_16.setText(QCoreApplication.translate("MainWindow", u"\uc601\uc6d4", None))
        self.checkBox_17.setText(QCoreApplication.translate("MainWindow", u"\uc6d0\uc8fc", None))
        self.checkBox_18.setText(QCoreApplication.translate("MainWindow", u"\uc778\uc81c", None))
        self.checkBox_19.setText(QCoreApplication.translate("MainWindow", u"\uc548\ub3d9", None))
        self.checkBox_20.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc120\uad70", None))
        self.checkBox_21.setText(QCoreApplication.translate("MainWindow", u"\ucca0\uc6d0", None))
        self.checkBox_22.setText(QCoreApplication.translate("MainWindow", u"\ucd98\ucc9c", None))
        self.checkBox_23.setText(QCoreApplication.translate("MainWindow", u"\ud0dc\ubc31", None))
        self.checkBox_24.setText(QCoreApplication.translate("MainWindow", u"\ud64d\ucc9c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  QCoreApplication.translate("MainWindow", u"\uac15\uc6d0\ub3c4", None))
        self.groupBox_3.setTitle(
            QCoreApplication.translate("MainWindow", u"\ucda9\uccad\ub3c4, \uc9c0\uc5ed\uc120\ud0dd", None))
        self.checkBox_25.setText(QCoreApplication.translate("MainWindow", u"\ubcf4\uc740", None))
        self.checkBox_26.setText(QCoreApplication.translate("MainWindow", u"\uc11c\uccad\uc8fc", None))
        self.checkBox_27.setText(QCoreApplication.translate("MainWindow", u"\uc81c\ucc9c", None))
        self.checkBox_28.setText(QCoreApplication.translate("MainWindow", u"\uccad\uc8fc", None))
        self.checkBox_29.setText(QCoreApplication.translate("MainWindow", u"\ucd94\ud48d\ub839", None))
        self.checkBox_30.setText(QCoreApplication.translate("MainWindow", u"\ucda9\uc8fc", None))
        self.checkBox_31.setText(QCoreApplication.translate("MainWindow", u"\ub300\uc804", None))
        self.checkBox_32.setText(QCoreApplication.translate("MainWindow", u"\uc138\uc885", None))
        self.checkBox_33.setText(QCoreApplication.translate("MainWindow", u"\uae08\uc0b0", None))
        self.checkBox_34.setText(QCoreApplication.translate("MainWindow", u"\ubcf4\ub839", None))
        self.checkBox_35.setText(QCoreApplication.translate("MainWindow", u"\ubd80\uc5ec", None))
        self.checkBox_36.setText(QCoreApplication.translate("MainWindow", u"\uc11c\uc0b0", None))
        self.checkBox_37.setText(QCoreApplication.translate("MainWindow", u"\ucc9c\uc548", None))
        self.checkBox_38.setText(QCoreApplication.translate("MainWindow", u"\ud64d\uc131", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3),
                                  QCoreApplication.translate("MainWindow", u"\ucda9\uccad\ub3c4", None))
        self.groupBox_4.setTitle(
            QCoreApplication.translate("MainWindow", u"\uc804\ub77c\ub3c4, \uc9c0\uc5ed\uc120\ud0dd", None))
        self.checkBox_39.setText(QCoreApplication.translate("MainWindow", u"\uad11\uc8fc", None))
        self.checkBox_40.setText(QCoreApplication.translate("MainWindow", u"\uace0\ucc3d", None))
        self.checkBox_41.setText(QCoreApplication.translate("MainWindow", u"\uace0\ucc3d\uad70", None))
        self.checkBox_42.setText(QCoreApplication.translate("MainWindow", u"\uad70\uc0b0", None))
        self.checkBox_43.setText(QCoreApplication.translate("MainWindow", u"\ub0a8\uc6d0", None))
        self.checkBox_44.setText(QCoreApplication.translate("MainWindow", u"\ubd80\uc548", None))
        self.checkBox_45.setText(QCoreApplication.translate("MainWindow", u"\uc21c\ucc3d\uad70", None))
        self.checkBox_46.setText(QCoreApplication.translate("MainWindow", u"\uc784\uc2e4", None))
        self.checkBox_47.setText(QCoreApplication.translate("MainWindow", u"\uc7a5\uc218", None))
        self.checkBox_48.setText(QCoreApplication.translate("MainWindow", u"\uc804\uc8fc", None))
        self.checkBox_59.setText(QCoreApplication.translate("MainWindow", u"\uc644\ub3c4", None))
        self.checkBox_60.setText(QCoreApplication.translate("MainWindow", u"\uc7a5\ud765", None))
        self.checkBox_61.setText(QCoreApplication.translate("MainWindow", u"\uc8fc\uc554", None))
        self.checkBox_62.setText(QCoreApplication.translate("MainWindow", u"\uc9c4\ub3c4(\ucca8\ucca0\uc0b0)", None))
        self.checkBox_63.setText(QCoreApplication.translate("MainWindow", u"\uc9c4\ub3c4\uad70", None))
        self.checkBox_64.setText(QCoreApplication.translate("MainWindow", u"\ud574\ub0a8", None))
        self.checkBox_65.setText(QCoreApplication.translate("MainWindow", u"\ud751\uc0b0\ub3c4", None))
        self.checkBox_49.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc74d", None))
        self.checkBox_50.setText(QCoreApplication.translate("MainWindow", u"\uac15\uc9c4\uad70", None))
        self.checkBox_51.setText(QCoreApplication.translate("MainWindow", u"\uace0\ud765", None))
        self.checkBox_52.setText(QCoreApplication.translate("MainWindow", u"\uad11\uc591\uc2dc", None))
        self.checkBox_53.setText(QCoreApplication.translate("MainWindow", u"\ubaa9\ud3ec", None))
        self.checkBox_54.setText(QCoreApplication.translate("MainWindow", u"\ubb34\uc548", None))
        self.checkBox_55.setText(QCoreApplication.translate("MainWindow", u"\ubcf4\uc131\uad70", None))
        self.checkBox_56.setText(QCoreApplication.translate("MainWindow", u"\uc21c\ucc9c", None))
        self.checkBox_57.setText(QCoreApplication.translate("MainWindow", u"\uc5ec\uc218", None))
        self.checkBox_58.setText(QCoreApplication.translate("MainWindow", u"\uc601\uad11\uad70", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4),
                                  QCoreApplication.translate("MainWindow", u"\uc804\ub77c\ub3c4", None))
        self.groupBox_5.setTitle(
            QCoreApplication.translate("MainWindow", u"\uacbd\uc0c1\ub3c4, \uc9c0\uc5ed\uc120\ud0dd", None))
        self.checkBox_66.setText(QCoreApplication.translate("MainWindow", u"\ub300\uad6c", None))
        self.checkBox_67.setText(QCoreApplication.translate("MainWindow", u"\ub300\uad6c(\uae30)", None))
        self.checkBox_68.setText(QCoreApplication.translate("MainWindow", u"\uc6b8\uc0b0", None))
        self.checkBox_69.setText(QCoreApplication.translate("MainWindow", u"\ubd80\uc0b0", None))
        self.checkBox_70.setText(QCoreApplication.translate("MainWindow", u"\uacbd\uc8fc\uc2dc", None))
        self.checkBox_71.setText(QCoreApplication.translate("MainWindow", u"\uad6c\ubbf8", None))
        self.checkBox_72.setText(QCoreApplication.translate("MainWindow", u"\ubb38\uacbd", None))
        self.checkBox_73.setText(QCoreApplication.translate("MainWindow", u"\ubd09\ud654", None))
        self.checkBox_74.setText(QCoreApplication.translate("MainWindow", u"\uc0c1\uc8fc", None))
        self.checkBox_75.setText(QCoreApplication.translate("MainWindow", u"\uc548\ub3d9", None))
        self.checkBox_76.setText(QCoreApplication.translate("MainWindow", u"\uc601\ub355", None))
        self.checkBox_88.setText(QCoreApplication.translate("MainWindow", u"\ubc00\uc591", None))
        self.checkBox_89.setText(QCoreApplication.translate("MainWindow", u"\ubd81\ucc3d\uc6d0", None))
        self.checkBox_90.setText(QCoreApplication.translate("MainWindow", u"\uc0b0\uccad", None))
        self.checkBox_91.setText(QCoreApplication.translate("MainWindow", u"\uc591\uc0b0\uc2dc", None))
        self.checkBox_92.setText(QCoreApplication.translate("MainWindow", u"\uc758\ub839\uad70", None))
        self.checkBox_93.setText(QCoreApplication.translate("MainWindow", u"\uc9c4\uc8fc", None))
        self.checkBox_94.setText(QCoreApplication.translate("MainWindow", u"\ucc3d\uc6d0", None))
        self.checkBox_95.setText(QCoreApplication.translate("MainWindow", u"\ud1b5\uc601", None))
        self.checkBox_96.setText(QCoreApplication.translate("MainWindow", u"\ud568\uc591\uad70", None))
        self.checkBox_97.setText(QCoreApplication.translate("MainWindow", u"\ud569\ucc9c", None))
        self.checkBox_77.setText(QCoreApplication.translate("MainWindow", u"\uc601\uc8fc", None))
        self.checkBox_78.setText(QCoreApplication.translate("MainWindow", u"\uc601\ucc9c", None))
        self.checkBox_79.setText(QCoreApplication.translate("MainWindow", u"\uc6b8\ub989\ub3c4", None))
        self.checkBox_80.setText(QCoreApplication.translate("MainWindow", u"\uc6b8\uc9c4", None))
        self.checkBox_81.setText(QCoreApplication.translate("MainWindow", u"\uc758\uc131", None))
        self.checkBox_82.setText(QCoreApplication.translate("MainWindow", u"\uccad\uc1a1\uad70", None))
        self.checkBox_83.setText(QCoreApplication.translate("MainWindow", u"\ud3ec\ud56d", None))
        self.checkBox_84.setText(QCoreApplication.translate("MainWindow", u"\uac70\uc81c", None))
        self.checkBox_85.setText(QCoreApplication.translate("MainWindow", u"\uac70\ucc3d", None))
        self.checkBox_86.setText(QCoreApplication.translate("MainWindow", u"\uae40\ud574\uc2dc", None))
        self.checkBox_87.setText(QCoreApplication.translate("MainWindow", u"\ub0a8\ud574", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5),
                                  QCoreApplication.translate("MainWindow", u"\uacbd\uc0c1\ub3c4", None))
        self.groupBox_6.setTitle(
            QCoreApplication.translate("MainWindow", u"\uc81c\uc8fc\ub3c4, \uc9c0\uc5ed\uc120\ud0dd", None))
        self.checkBox_98.setText(QCoreApplication.translate("MainWindow", u"\uace0\uc0b0", None))
        self.checkBox_99.setText(QCoreApplication.translate("MainWindow", u"\uc11c\uadc0\ud3ec", None))
        self.checkBox_100.setText(QCoreApplication.translate("MainWindow", u"\uc131\uc0b0", None))
        self.checkBox_101.setText(QCoreApplication.translate("MainWindow", u"\uc131\uc0b0", None))
        self.checkBox_102.setText(QCoreApplication.translate("MainWindow", u"\uc131\uc0b0\ud3ec", None))
        self.checkBox_103.setText(QCoreApplication.translate("MainWindow", u"\uc81c\uc8fc", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6),
                                  QCoreApplication.translate("MainWindow", u"\uc81c\uc8fc\ub3c4", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Select All", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"UnSelect All", None))
        self.pushButton_1.setText(QCoreApplication.translate("MainWindow", u"Collect Weater Data", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Convert To BAS", None))
    # retranslateUi
