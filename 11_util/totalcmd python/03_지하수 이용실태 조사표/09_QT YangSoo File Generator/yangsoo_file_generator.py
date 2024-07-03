import sys
import time

from PySide6.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow

from FileProcessing_V4_001 import PrepareYangsoofile
from SetProjectInfo import Set_Projectinfo
from preProjectInfo_Setting import main_call
from preProjectInfoSetting_byExcel import process_yangsoo_spec


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.pushButton_2.clicked.connect(self.on_pushButton2_clicked)
        self.pushButton_3.clicked.connect(self.on_pushButton3_clicked)
        self.pushButton_4.clicked.connect(self.on_pushButton4_clicked)

        self.file_processing = PrepareYangsoofile()

        # Connect all radio buttons to the same handler
        for i in range(1, 12):
            radio_button = getattr(self, f'radio{i}')
            radio_button.toggled.connect(self.on_radio_button_toggled)

        self.textEdit_2.setText("선택한 항목: 주식회사 한일지하수")
        self.Company = "주식회사 한일지하수"
        self.Address = "주소는 없어요"

    def on_radio_button_toggled(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.textEdit_2.setText(f"선택한 항목: {radio_button.text()}")
            self.Company = radio_button.text()
            print(f'Company : {self.Company}')

    def on_pushButton_clicked(self):
        # Get spin value and checkbox state
        spin_value = self.spinBox.value()
        checkbox_state = self.checkBox.isChecked()
        mode = True if checkbox_state else False

        # Get and validate address
        self.Address = self.textEdit.toPlainText()
        if not self.Address:
            self.textEdit_3.setText("Address is empty, Fill in the gap")
        else:
            self.textEdit_3.setText(f"{spin_value} file to Send, Company: {self.Company} / {self.Address}")
            self.file_processing.duplicate_yangsoo_excel(spin_value)
            for i in range(1, spin_value + 1):
                self.file_processing.aqtfile_to_send(i, mode)
            Set_Projectinfo(self.Company, self.Address)

    def on_pushButton3_clicked(self):
        self.Address = self.textEdit.toPlainText()
        self.textEdit_3.setText("Run ProjectInfo Using Aqt File")

        spin_value = self.spinBox.value()
        checkbox_state = self.checkBox.isChecked()
        mode = True if checkbox_state else False

        self.file_processing.set_directory(self.file_processing.SEND)
        aqt_files = self.file_processing.get_aqt_files()

        """
             aqt_file 이 있고, yansoo_file 이 있으면 - 01
             aqt_file이 있고, yansoo file이 없으면 - 02
             aqt_file 도 없고, yansoo file 도 없으면 - main 으로 파일 제너레이션 ...
        """

        if self.file_processing.is_exist(self.file_processing.YANSOO_SPEC):
            print(f'self.Company : {self.Company}, self.Address: {self.Address}')

            if len(aqt_files) > 0:
                process_yangsoo_spec()
            else:
                for i in range(1, spin_value + 1):
                    self.file_processing.aqtfile_to_send(i, mode)
                process_yangsoo_spec()
        else:
            if len(aqt_files) > 0:
                print(f'main_call : self.Company : {self.Company}, self.Address: {self.Address}')
                main_call(self.Address, self.Company)
            else:
                print(f'copyaqt_and_set :  self.Company : {self.Company}, self.Address: {self.Address}')
                self.copyaqt_and_set()

    def copyaqt_and_set(self):
        # Get spin value and checkbox state
        spin_value = self.spinBox.value()
        checkbox_state = self.checkBox.isChecked()
        mode = True if checkbox_state else False

        # Get and validate address
        self.Address = self.textEdit.toPlainText()
        if not self.Address:
            self.textEdit_3.setText("Address is empty, Fill in the gap")
        else:
            self.textEdit_3.setText(f"{spin_value} file to Send, Company: {self.Company} / {self.Address}")
            for i in range(1, spin_value + 1):
                self.file_processing.aqtfile_to_send(i, mode)

            print(f'inside, copyaqt_and_set : self.Company : {self.Company}, self.Address: {self.Address}')
            Set_Projectinfo(self.Company, self.Address)

    def on_pushButton2_clicked(self):
        self.close()

    def on_pushButton4_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('windows')
    # app.setStyle('windows')

    window = MainWindow()
    window.show()

    app.exec()
