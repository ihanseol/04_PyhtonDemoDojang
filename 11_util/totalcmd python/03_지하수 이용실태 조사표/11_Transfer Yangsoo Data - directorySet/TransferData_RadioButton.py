import os
import pickle
import sys
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow
from ui_transfer_radio import Ui_MainWindow

import FileProcessing_V4_20240708 as fp2c
from FileProcessing_V4_20240708 import TransferYangSooFile

# from TransferYangsoo import TransferYangSooFile
# fp2c - file processing class v2

"""
2024/7/8 
    TransferYangSooFile Refactor
    와 디렉토리 패스와 관련된 부분,
    그리고
    BASEDIR 세팅에서, 추가한 부분등 ...
"""

fp = fp2c.FileBase('')
TYF = TransferYangSooFile()


class SavedpathClass:
    def __init__(self):
        self.flocation = ''
        self.ls_directory = 'c:\\Program Files\\totalcmd\\AqtSolv\\'

    def savepath_to_file(self, path_data):
        file_path = os.path.join(self.ls_directory, 'SaveFolder.sav')
        os.makedirs(self.ls_directory, exist_ok=True)  # Create the directory if it doesn't exist

        # Save the data to the file
        with open(file_path, 'wb') as file:
            pickle.dump(path_data, file)

        print(f'File saved to {file_path}')
        self.flocation = path_data

    def loadpath_to_file(self):
        file_path = os.path.join(self.ls_directory, 'SaveFolder.sav')
        with open(file_path, 'rb') as file:
            loaded_data = pickle.load(file)

        print(f'File loaded from {file_path}')
        self.flocation = loaded_data


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.BASE_PATH = ''

        self.sp = SavedpathClass()
        self.sp.loadpath_to_file()

        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.pushButton_2.clicked.connect(self.on_pushButton_2_clicked)
        self.pushButton_3.clicked.connect(self.on_pushButton_3_clicked)

        self.BASE_PATH = self.sp.flocation
        self.lineEdit.setText(self.sp.flocation)

        for i in range(1, 4):
            radio_button = getattr(self, f'radioButton_{i}')
            radio_button.toggled.connect(self.on_radio_button_toggled)

    def on_radio_button_toggled(self):
        radio_button = self.sender()
        radio_button_name = radio_button.objectName()

        if radio_button.isChecked():
            self.lineEdit_2.setText(f"선택한 항목: {radio_button_name}, {radio_button.text()}")

    def on_pushButton_clicked(self):
        # seclect button

        self.lineEdit_2.setText("Selection button clicked ...")
        current_year = datetime.now().year
        if self.sp.flocation != '':
            location_temp = self.sp.flocation
        else:
            location_temp = f'd:\\09_hardRain\\09_ihanseol - {current_year}\\'

        select_folder = fp.select_folder(location_temp)
        check = TYF.isit_yangsoo_inside(select_folder)
        if not check:
            return False

        self.BASE_PATH = select_folder
        self.lineEdit.setText(select_folder)
        self.sp.savepath_to_file(select_folder)

    def on_pushButton_2_clicked(self):
        # Exit button
        self.lineEdit_2.setText("Exit button clicked ...")
        self.close()

    def on_pushButton_3_clicked(self):
        # Run Butotton ...

        self.lineEdit_2.setText("Run button clicked ...")

        path = TYF.setBASEDIR(self.BASE_PATH)

        if path == "FALSE":
            TYF.BASEDIR = self.sp.flocation
            return False

        self.BASE_PATH = path
        self.lineEdit.setText(self.BASE_PATH)

        if self.radioButton_1.isChecked():
            TYF.move_origin_to_ihanseol(TYF.DOCUMENTS)

        if self.radioButton_2.isChecked():
            TYF.move_origin_to_ihanseol(TYF.SEND)

        if self.radioButton_3.isChecked():
            TYF.move_origin_to_ihanseol(TYF.SEND2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('windows')
    # app.setStyle('windowsvista')

    window = MainWindow()
    window.show()

    app.exec()
