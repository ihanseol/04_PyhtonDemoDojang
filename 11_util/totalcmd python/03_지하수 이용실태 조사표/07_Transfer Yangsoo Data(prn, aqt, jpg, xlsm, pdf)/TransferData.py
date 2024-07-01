import os
import sys
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow
from ui_transfer import Ui_MainWindow
import FileProcessing_V3 as fp2c
from FileProcessing_V3 import TransferYangSooFile

# fp2c - file processing class v2

fp = fp2c.FileBase('')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.BASE_PATH = ''
        self.tyd = TransferYangSooFile()
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.pushButton_2.clicked.connect(self.on_pushButton_2_clicked)
        self.pushButton_3.clicked.connect(self.on_pushButton_3_clicked)

        self.lineEdit.setText("Please select the base folder to move ...")

    def on_pushButton_clicked(self):
        self.lineEdit_2.setText("Selection button clicked ...")
        current_year = datetime.now().year
        folder_name = fp.select_folder(f'd:\\09_hardRain\\09_ihanseol - {current_year}\\')

        self.BASE_PATH = folder_name
        self.lineEdit.setText(folder_name)

    def on_pushButton_2_clicked(self):
        self.lineEdit_2.setText("Exit button clicked ...")
        self.close()

    def on_pushButton_3_clicked(self):
        self.lineEdit_2.setText("Run button clicked ...")

        path = self.tyd.setBASEDIR(self.BASE_PATH)

        self.BASE_PATH = path
        self.lineEdit.setText(self.BASE_PATH)

        if self.checkBox_1.isChecked():
            self.tyd.move_documents_to_ihanseol()

        if self.checkBox_2.isChecked():
            self.tyd.move_send_to_ihanseol()

        if self.checkBox_3.isChecked():
            self.tyd.move_send2_to_ihanseol()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('windows')
    # app.setStyle('windowsvista')

    window = MainWindow()
    window.show()

    app.exec()
