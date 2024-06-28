import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow
import FileProcessing as fps
import SetProjectInfo as sp


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.file_processing = fps.FileProcessing()

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

    def on_pushButton_clicked(self):
        # Get spin value and checkbox state
        spin_value = self.spinBox.value()
        checkbox_state = self.checkBox.isChecked()
        mode = 'include' if checkbox_state else 'exclude'

        # Get and validate address
        self.Address = self.textEdit.toPlainText()
        if not self.Address:
            self.textEdit_3.setText("Address is empty, Fill in the gap")
        else:
            self.textEdit_3.setText(f"{spin_value} file to Send, Company: {self.Company} / {self.Address}")
            self.file_processing.duplicate_yangsoo(spin_value)
            for i in range(1, spin_value + 1):
                self.file_processing.aqt_send(i, mode)
            sp.Set_Projectinfo(self.Company, self.Address)
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('windows')
    # app.setStyle('windowsvista')

    window = MainWindow()
    window.show()

    app.exec()
