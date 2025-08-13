import sys

from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtWidgets import QMainWindow
from get_tm_cordinate_ui import Ui_Dialog
import kakao


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.ui.pushButton_2.clicked.connect(self.on_pushButton2_clicked)

        self.ui.textEdit.setText("대전시 유성구 장대동 278-13 ")

    def on_pushButton_clicked(self):
        """
            Get TM Cordinate ...
            카카오맵 API를 이용해서, 좌표를 읽어온다.
        """
        addr = self.ui.textEdit.toPlainText()
        result01, result02, result03 = kakao.get_tm_cordinate(addr)

        self.ui.plainTextEdit.setPlainText(result01 + result02 + result03)

    def on_pushButton2_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('windows')

    window = MainWindow()
    window.show()

    app.exec()
