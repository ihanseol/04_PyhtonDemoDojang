import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow
import FileProcessing as fps
import SetProjectInfo as SetPinfo


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.file_processing = fps.FileProcessing()
        self.radio1.toggled.connect(self.radio1_onClicked)
        self.radio2.toggled.connect(self.radio2_onClicked)
        self.radio3.toggled.connect(self.radio3_onClicked)
        self.radio4.toggled.connect(self.radio4_onClicked)
        self.radio5.toggled.connect(self.radio5_onClicked)
        self.radio6.toggled.connect(self.radio6_onClicked)
        self.radio7.toggled.connect(self.radio7_onClicked)
        self.radio8.toggled.connect(self.radio8_onClicked)
        self.radio9.toggled.connect(self.radio9_onClicked)
        self.radio10.toggled.connect(self.radio10_onClicked)
        self.radio11.toggled.connect(self.radio11_onClicked)
        self.textEdit_2.setText(f"선택한 항목: 주식회사 한일지하수")

        self.Company = "주식회사 한일지하수"
        self.Address = "주소는 없어요"



    def insert_text_into_text_edit(self):
        self.textEdit.setText("Hello, this is a sample text.")


    def radio1_onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.textEdit_2.setText(f"선택한 항목: {radioButton.text()}")
            self.Company = radioButton.text()

    def radio2_onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.textEdit_2.setText(f"선택한 항목: {radioButton.text()}")
            self.Company = radioButton.text()

    def radio3_onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.textEdit_2.setText(f"선택한 항목: {radioButton.text()}")
            self.Company = radioButton.text()

    def radio4_onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.textEdit_2.setText(f"선택한 항목: {radioButton.text()}")
            self.Company = radioButton.text()

    def radio5_onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.textEdit_2.setText(f"선택한 항목: {radioButton.text()}")
            self.Company = radioButton.text()

    def radio6_onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.textEdit_2.setText(f"선택한 항목: {radioButton.text()}")
            self.Company = radioButton.text()

    def radio7_onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.textEdit_2.setText(f"선택한 항목: {radioButton.text()}")
            self.Company = radioButton.text()

    def radio8_onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.textEdit_2.setText(f"선택한 항목: {radioButton.text()}")
            self.Company = radioButton.text()

    def radio9_onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.textEdit_2.setText(f"선택한 항목: {radioButton.text()}")
            self.Company = radioButton.text()

    def radio10_onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.textEdit_2.setText(f"선택한 항목: {radioButton.text()}")
            self.Company = radioButton.text()

    def radio11_onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.textEdit_2.setText(f"선택한 항목: {radioButton.text()}")
            self.Company = radioButton.text()


    def on_pushButton_clicked(self):
        # spin_value = number of well
        spin_value = self.spinBox.value()

        # checkbox_state = include step_file, or exclude step_file
        checkbox_state = self.checkBox.isChecked()

        # Insert the value into the textEdit
        if checkbox_state:
            mode = 'include'
        else:
            mode = 'exclude'

        self.Address = self.textEdit.toPlainText()
        if not self.Address:
            self.textEdit_3.setText(f"Address is empty, Fill in the gap")
        else:
            self.textEdit_3.setText(f"{spin_value} file to Send, Company : {self.Company} / {self.Address}")
            self.file_processing.duplicate_yangsoo(spin_value)
            for i in range(1, spin_value + 1):
                self.file_processing.aqt_send(i, mode)
            SetPinfo.set_projectinfo(self.Company, self.Address)
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyle('windows')
    app.setStyle('windowsvista')

    window = MainWindow()
    window.show()

    app.exec()
