# -*- coding: utf-8 -*-
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui_file import Ui_MainWindow
from web_scraper import get_rainfall_data
import convert_to_bas as cb


class WeatherDataApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 탭별 체크박스 그룹 정의 (setup_connections 호출 전에 정의)
        self.tab_checkboxes = {
            0: [self.ui.checkBox_1, self.ui.checkBox_2, self.ui.checkBox_3, self.ui.checkBox_4,
                self.ui.checkBox_5, self.ui.checkBox_6, self.ui.checkBox_7],
            1: [self.ui.checkBox_8, self.ui.checkBox_9, self.ui.checkBox_10, self.ui.checkBox_11,
                self.ui.checkBox_13, self.ui.checkBox_14, self.ui.checkBox_15, self.ui.checkBox_16,
                self.ui.checkBox_17, self.ui.checkBox_18, self.ui.checkBox_19, self.ui.checkBox_20,
                self.ui.checkBox_21, self.ui.checkBox_22, self.ui.checkBox_23, self.ui.checkBox_24],
            2: [self.ui.checkBox_25, self.ui.checkBox_26, self.ui.checkBox_27, self.ui.checkBox_28,
                self.ui.checkBox_29, self.ui.checkBox_30, self.ui.checkBox_31, self.ui.checkBox_32,
                self.ui.checkBox_33, self.ui.checkBox_34, self.ui.checkBox_35, self.ui.checkBox_36,
                self.ui.checkBox_37, self.ui.checkBox_38],
            3: [self.ui.checkBox_39, self.ui.checkBox_40, self.ui.checkBox_41, self.ui.checkBox_42,
                self.ui.checkBox_43, self.ui.checkBox_44, self.ui.checkBox_45, self.ui.checkBox_46,
                self.ui.checkBox_47, self.ui.checkBox_48, self.ui.checkBox_49, self.ui.checkBox_50,
                self.ui.checkBox_51, self.ui.checkBox_52, self.ui.checkBox_53, self.ui.checkBox_54,
                self.ui.checkBox_55, self.ui.checkBox_56, self.ui.checkBox_57, self.ui.checkBox_58,
                self.ui.checkBox_59, self.ui.checkBox_60, self.ui.checkBox_61, self.ui.checkBox_62,
                self.ui.checkBox_63, self.ui.checkBox_64, self.ui.checkBox_65],
            4: [self.ui.checkBox_66, self.ui.checkBox_67, self.ui.checkBox_68, self.ui.checkBox_69,
                self.ui.checkBox_70, self.ui.checkBox_71, self.ui.checkBox_72, self.ui.checkBox_73,
                self.ui.checkBox_74, self.ui.checkBox_75, self.ui.checkBox_76, self.ui.checkBox_77,
                self.ui.checkBox_78, self.ui.checkBox_79, self.ui.checkBox_80, self.ui.checkBox_81,
                self.ui.checkBox_82, self.ui.checkBox_83, self.ui.checkBox_84, self.ui.checkBox_85,
                self.ui.checkBox_86, self.ui.checkBox_87, self.ui.checkBox_88, self.ui.checkBox_89,
                self.ui.checkBox_90, self.ui.checkBox_91, self.ui.checkBox_92, self.ui.checkBox_93,
                self.ui.checkBox_94, self.ui.checkBox_95, self.ui.checkBox_96, self.ui.checkBox_97],
            5: [self.ui.checkBox_98, self.ui.checkBox_99, self.ui.checkBox_100, self.ui.checkBox_101,
                self.ui.checkBox_102, self.ui.checkBox_103]
        }

        self.setup_connections()
        self.setup_listview()

    def setup_listview(self):
        """ListView 설정"""
        # 선택된 지역 리스트뷰
        self.model = QStandardItemModel()
        self.ui.listView.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["선택된 지역"])

        # 정보 출력 리스트뷰
        self.info_model = QStandardItemModel()
        self.ui.listView_info.setModel(self.info_model)
        self.info_model.setHorizontalHeaderLabels(["프로그램 정보"])

    def setup_connections(self):
        """시그널-슬롯 연결"""
        # 버튼 연결
        self.ui.pushButton_1.clicked.connect(self.collect_weather_data)
        self.ui.pushButton_2.clicked.connect(self.select_all)
        self.ui.pushButton_3.clicked.connect(self.unselect_all)
        self.ui.pushButton_4.clicked.connect(self.exit_button)
        self.ui.pushButton_5.clicked.connect(self.convert_to_all)

        # 모든 체크박스에 대해 상태 변경 시그널 연결
        all_checkboxes = []
        for tab_checkboxes in self.tab_checkboxes.values():
            all_checkboxes.extend(tab_checkboxes)

        for checkbox in all_checkboxes:
            checkbox.stateChanged.connect(self.update_listview)

    def update_listview(self):
        """체크박스 상태가 변경될 때 ListView 업데이트"""
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["선택된 지역"])

        # 모든 체크박스를 확인하여 체크된 것들만 리스트에 추가
        all_checkboxes = []
        for tab_checkboxes in self.tab_checkboxes.values():
            all_checkboxes.extend(tab_checkboxes)

        for checkbox in all_checkboxes:
            if checkbox.isChecked():
                item = QStandardItem(checkbox.text())
                self.model.appendRow(item)

    def select_all(self):
        """현재 탭의 모든 체크박스 선택"""
        current_tab = self.ui.tabWidget.currentIndex()
        if current_tab in self.tab_checkboxes:
            for checkbox in self.tab_checkboxes[current_tab]:
                checkbox.setChecked(True)

    def unselect_all(self):
        """현재 탭의 모든 체크박스 선택 해제"""
        current_tab = self.ui.tabWidget.currentIndex()
        if current_tab in self.tab_checkboxes:
            for checkbox in self.tab_checkboxes[current_tab]:
                checkbox.setChecked(False)

    def exit_button(self):
        self.close()

    def convert_to_all(self):
        self.printinfo("=" * 100)
        self.printinfo("Excel VBA 코드로 변환시작 ")
        slist = cb.convert_to_vbacode()
        self.printinfo(f"성공적으로 {len(slist)}갯수의 파일을 변환하였습니다.")
        self.printinfo("=" * 100)
        self.printinfo(slist)
        self.printinfo("=" * 100)
        self.printinfo(" 수고하셨습니다. ! ")


    def collect_weather_data(self):
        """날씨 데이터 수집 (예제 함수)"""
        selected_locations = []

        # 모든 체크박스를 확인하여 선택된 지역 수집
        all_checkboxes = []
        for tab_checkboxes in self.tab_checkboxes.values():
            all_checkboxes.extend(tab_checkboxes)

        for checkbox in all_checkboxes:
            if checkbox.isChecked():
                selected_locations.append(checkbox.text())

        if selected_locations:
            # printinfo 함수 사용 예제
            self.printinfo("=" * 50)
            self.printinfo("날씨 데이터 수집 시작")
            self.printinfo("=" * 50)
            self.printinfo(f"선택된 지역 수: {len(selected_locations)}개")
            self.printinfo()

            for i, location in enumerate(selected_locations, 1):
                self.printinfo(f"{i:2d}. {location}")

            self.printinfo()
            self.printinfo("데이터 수집을 시작합니다...")

            # 메시지박스도 표시
            message = f"선택된 지역 ({len(selected_locations)}개):\n"
            message += "\n".join(f"• {location}" for location in selected_locations)
            message += "\n\n날씨 데이터 수집을 시작합니다."
            QMessageBox.information(self, "날씨 데이터 수집", message)

            get_rainfall_data(selected_locations)

            # 여기에 실제 날씨 데이터 수집 로직을 구현할 수 있습니다
            print(f"수집할 지역: {selected_locations}")
        else:
            self.printinfo("경고: 수집할 지역이 선택되지 않았습니다.")
            QMessageBox.warning(self, "알림", "수집할 지역을 선택해주세요.")

    def get_selected_locations(self):
        """선택된 지역 목록을 반환하는 유틸리티 함수"""
        selected_locations = []
        all_checkboxes = []
        for tab_checkboxes in self.tab_checkboxes.values():
            all_checkboxes.extend(tab_checkboxes)

        for checkbox in all_checkboxes:
            if checkbox.isChecked():
                selected_locations.append(checkbox.text())

        return selected_locations

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
                self.info_model.appendRow(item)

        # 빈 줄만 있는 경우 처리
        if not lines and end == '\n':
            item = QStandardItem("")
            self.info_model.appendRow(item)

        # 스크롤을 맨 아래로 이동
        self.ui.listView_info.scrollToBottom()

        # 콘솔에도 동시 출력 (디버깅용)
        print(*args, sep=sep, end=end)


def main():
    app = QApplication(sys.argv)
    window = WeatherDataApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
