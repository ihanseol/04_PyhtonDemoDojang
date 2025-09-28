"""
  YangSoo Test All (StepFirst, StepFinal)
  2025, 9, 28일
"""

import sys
import os
import shutil

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui_yangsoo import Ui_MainWindow

from YangSoo.YanSooTest_01_FirstStep import YangSooInjector
from YangSoo.YanSooTest_02_FinalStep import PumpTestAutomation


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.setupUi(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.injector = YangSooInjector("d:\\05_Send\\")
        self.pump_test = PumpTestAutomation()

        self.setup_connections()
        self.setup_listview()

    def setup_connections(self):
        """시그널-슬롯 연결"""
        # 버튼 연결
        self.ui.pushButton.clicked.connect(self.yangsoo_first_step)
        self.ui.pushButton_2.clicked.connect(self.yangsoo_final_step)
        self.ui.pushButton_3.clicked.connect(self.on_pushButton3_clicked)
        self.ui.pushButton_4.clicked.connect(self.on_pushButton4_clicked)

    def setup_listview(self):
        """ListView 설정"""
        # 선택된 지역 리스트뷰
        self.model = QStandardItemModel()
        self.ui.listView.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["Information Print Window"])

    def update_listview(self):
        """체크박스 상태가 변경될 때 ListView 업데이트"""
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Information Print Window"])

    def printinfo(self, *args, sep=' ', end='\n'):
        """print() 함수와 동일하게 작동하지만 listView_info에 출력하는 함수"""
        # print()와 동일한 방식으로 인자들을 문자열로 변환 및 결합
        text = sep.join(str(arg) for arg in args) + end

        # 줄바꿈 문자로 분리하여 각 줄을 별도 아이템으로 추가
        lines = text.splitlines()
        if text.endswith('\n') and lines:
            # 마지막 줄이 빈 줄인 경우 제거 (print의 기본 동작과 맞춤)
            pass

        for line in lines:
            if line or not lines:  # 빈 줄이 아니거나 전체가 빈 줄인 경우
                item = QStandardItem(line)
                self.model.appendRow(item)

        # 빈 줄만 있는 경우 처리
        if not lines and end == '\n':
            item = QStandardItem("")
            self.model.appendRow(item)

        # 스크롤을 맨 아래로 이동
        self.ui.listView.scrollToBottom()

        # 콘솔에도 동시 출력 (디버깅용)
        print(*args, sep=sep, end=end)


    def yangsoo_first_step(self):
        self.printinfo("=" * 100)
        self.printinfo(" execute yangsoo_first_step ... ")
        self.printinfo("=" * 100)

        self.injector.initial_delete_output_file(r"c:/Users/minhwasoo/Documents/")
        self.injector.process_files()


    def yangsoo_final_step(self):
        self.printinfo("=" * 100)
        self.printinfo(" execute yangsoo_final_step ... ")
        self.printinfo("=" * 100)

        self.pump_test.main_processing(Mode=2)

    def on_pushButton3_clicked(self):
        self.close()

    def on_pushButton4_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyle('windows')
    # app.setStyle('fusion')
    # app.setStyle('windows11')
    app.setStyle('vista')

    window = MainWindow()
    window.show()

    app.exec()
