"""
  YangSoo Test All (StepFirst, StepFinal)
  2025, 9, 28일
"""

import sys
import os
import shutil

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from ui_yangsoo import Ui_MainWindow

from File_Processing.FileManager import FileBase
from YangSoo.YanSooTest_01_FirstStep import YangSooInjector
from YangSoo.YanSooTest_02_FinalStep import PumpTestAutomation


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.injector = YangSooInjector("d:\\05_Send\\")
        self.pump_test = PumpTestAutomation()

        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.pushButton_2.clicked.connect(self.on_pushButton2_clicked)
        self.pushButton_3.clicked.connect(self.on_pushButton3_clicked)
        self.pushButton_4.clicked.connect(self.on_pushButton4_clicked)

    def on_pushButton_clicked(self):
        self.injector.initial_delete_output_file(r"c:/Users/minhwasoo/Documents/")
        self.injector.process_files()
        pass

    def on_pushButton2_clicked(self):
        self.pump_test.main_processing(Mode=2)

    def on_pushButton3_clicked(self):
        self.close()

    def on_pushButton4_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('windows')

    window = MainWindow()
    window.show()

    app.exec()
