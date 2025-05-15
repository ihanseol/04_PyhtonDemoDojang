"""
 양수파일을 생성해 주는 프로그램
  2024,12,12 일
  A1_기사용관정현황_2024_09_22.xlsm

  지금 내가가져오는 엑셀파일이 최신의 엑셀파일인지 아닌지를 확인하지를 못해서 ...
  파일이름을 토탈커맨더 디렉토리에서 파일이름을 위처럼 깃폴더와 일치시키고
  파일이름을 바꾸어 주는 부분을 추가 해준다.
"""

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from ui_for_yangsoo_file_generator import Ui_MainWindow

from FileProcessing_V4_20250211 import PrepareYangsoofile
from FileProcessing_V4_20250211 import AqtProjectInfoInjector
from FileProcessing_V4_20250211 import AqtExcelProjectInfoInjector


class MyClass:
    def __init__(self, resource):
        self.resource = resource
        print(f"Resource {resource} opened")

    def close(self):
        print(f"Resource {self.resource} closed")
        # Add resource cleanup code here
        self.resource = None

    def __enter__(self):
        # Initialization code
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup code
        self.close()


"""
 self.spi = AqtProjectInfoInjector("d:\\05_Send\\", "")
 self.spiexcel = AqtExcelProjectInfoInjector("d:\\05_Send\\", "")
 spi -- Set Project Info
"""


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
        for i in range(1, 16):
            radio_button = getattr(self, f'radio{i}')
            radio_button.toggled.connect(self.on_radio_button_toggled)

        self.textEdit_2.setText("선택한 항목: 주식회사 한일지하수")
        self.Company = "주식회사 한일지하수"
        self.Address = "주소는 없어요"
        self.spi = AqtProjectInfoInjector("d:\\05_Send\\", "")
        self.spiexcel = AqtExcelProjectInfoInjector("d:\\05_Send\\", "")

    def on_radio_button_toggled(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.textEdit_2.setText(f"선택한 항목: {radio_button.text()}")
            self.Company = radio_button.text()
            print(f'Company : {self.Company}')

    def on_pushButton_clicked(self):
        """
            Run Button , Number 1 Tab
        """
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
            self.spi.Set_Projectinfo(self.Company, self.Address)

    def on_pushButton3_clicked(self):
        """
                  Run Button , Number 2 Tab
        """
        self.Address = self.textEdit.toPlainText()
        self.textEdit_3.setText("Run ProjectInfo Using Aqt File")

        spin_value = self.spinBox.value()
        checkbox_state = self.checkBox.isChecked()

        self.file_processing.set_directory(self.file_processing.SEND)
        aqt_files = self.file_processing.get_aqt_files()

        """
             aqt_file 이 있고, yansoo_file 이 있으면 - 01
             aqt_file이 있고, yansoo file이 없으면 - 02
             aqt_file 도 없고, yansoo file 도 없으면 - main 으로 파일 제너레이션 ...
        """

        if self.file_processing.is_exist(self.file_processing.YANSOO_SPEC):
            # 양수스펙파일이 있으면
            print(f'self.Company : {self.Company}, self.Address: {self.Address}')

            if len(aqt_files) > 0:
                self.spiexcel.process_projectinfo_byexcel()
            else:

                gong_lists = self.spiexcel.get_gong_list()
                for i in gong_lists:
                    self.file_processing.aqtfile_to_send(i, checkbox_state or self.spiexcel.is_jiyeol)
                self.spiexcel.process_projectinfo_byexcel()
        else:
            # 양수스펙파일이 없으면
            if len(aqt_files) > 0:
                print(f'main_call : self.Company : {self.Company}, self.Address: {self.Address}')
                # self.spi.main_call_project_info(self.Address, self.Company)
                self.spi.Set_Projectinfo(self.Company, self.Address)
            else:
                print(f'copyaqt_and_set :  self.Company : {self.Company}, self.Address: {self.Address}')
                self.copyaqt_and_set()

    def copyaqt_and_set(self):
        # Get spin value and checkbox state
        spin_value = self.spinBox.value()
        checkbox_state = self.checkBox.isChecked()

        # Get and validate address
        self.Address = self.textEdit.toPlainText()
        if not self.Address:
            self.textEdit_3.setText("Address is empty, Fill in the gap")
        else:
            self.textEdit_3.setText(f"{spin_value} file to Send, Company: {self.Company} / {self.Address}")
            for i in range(1, spin_value + 1):
                self.file_processing.aqtfile_to_send(i, checkbox_state)

            print(f'inside, copyaqt_and_set : self.Company : {self.Company}, self.Address: {self.Address}')
            self.spi.Set_Projectinfo(self.Company, self.Address)

    def on_pushButton2_clicked(self):
        self.close()

    def on_pushButton4_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('windows')
    # app.setStyle('windowsvista')
    # app.setStyle('fusion')

    window = MainWindow()
    window.show()

    app.exec()
