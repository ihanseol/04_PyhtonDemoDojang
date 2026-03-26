# -*- coding: utf-8 -*-
import sys
import os
import asyncio
import threading

from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui_file import Ui_MainWindow
import convert_to_bas as cb
from web_scraper_class_using_playwright import RainfallDataScraper


# ── ① 백그라운드 워커: 별도 스레드에서 asyncio 이벤트 루프를 돌린다 ──────────────
class ScraperWorker(QObject):
    """
    QThread 안에서 asyncio 코루틴을 실행하고,
    결과를 Signal로 메인 스레드(UI)에 전달하는 워커.
    """
    # (다운로드된 파일 목록, 결과 메시지) 두 값을 동시에 전달
    finished = Signal(list, str)
    # 진행 상황 한 줄 메시지
    progress = Signal(str)
    # 에러 발생 시
    error = Signal(str)

    def __init__(self, scraper: RainfallDataScraper, area_list: list):
        super().__init__()
        self.scraper = scraper
        self.area_list = area_list

    def run(self):
        """QThread.start() 시 자동 호출되는 진입점"""
        try:
            # 새 이벤트 루프를 이 스레드 전용으로 생성
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Playwright async 코루틴 실행
            downloaded_files, message = loop.run_until_complete(
                self.scraper.download_rainfall_data(self.area_list)
            )
            loop.close()

            self.finished.emit(downloaded_files, message)

        except Exception as e:
            self.error.emit(f"스크래퍼 오류: {e}")


# ── ② 메인 윈도우 ───────────────────────────────────────────────────────────────
class WeatherDataApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Scraper 인스턴스 (로그인 정보는 여기서 설정)
        self.scraper = RainfallDataScraper(
            login_id="hanseol33@naver.com",
            password="dseq%z8^feyham^"
        )

        # QThread / 워커 참조 보관용 (GC 방지)
        self._thread = None
        self._worker = None

        # 모델 초기화
        self.model = QStandardItemModel()
        self.info_model = QStandardItemModel()

        # 탭별 체크박스 그룹 정의
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
                self.ui.checkBox_102, self.ui.checkBox_103],
            6: [self.ui.checkBox_104, self.ui.checkBox_105, self.ui.checkBox_106, self.ui.checkBox_107,
                self.ui.checkBox_108, self.ui.checkBox_109, self.ui.checkBox_110, self.ui.checkBox_111,
                self.ui.checkBox_112, self.ui.checkBox_113, self.ui.checkBox_114]
        }

        self.setup_connections()
        self.setup_listview()

    # ── ListView 초기화 ──────────────────────────────────────────────────────
    def setup_listview(self):
        self.ui.listView.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["선택된 지역"])

        self.ui.listView_info.setModel(self.info_model)
        self.info_model.setHorizontalHeaderLabels(["프로그램 정보"])

    # ── 시그널-슬롯 연결 ─────────────────────────────────────────────────────
    def setup_connections(self):
        self.ui.pushButton_1.clicked.connect(self.collect_weather_data)
        self.ui.pushButton_2.clicked.connect(self.select_all)
        self.ui.pushButton_3.clicked.connect(self.unselect_all)
        self.ui.pushButton_4.clicked.connect(self.exit_button)
        self.ui.pushButton_5.clicked.connect(self.convert_to_all)

        for tab_checkboxes in self.tab_checkboxes.values():
            for checkbox in tab_checkboxes:
                checkbox.stateChanged.connect(self.update_listview)

    # ── 체크박스 → ListView 업데이트 ─────────────────────────────────────────
    def update_listview(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["선택된 지역"])

        for tab_checkboxes in self.tab_checkboxes.values():
            for checkbox in tab_checkboxes:
                if checkbox.isChecked():
                    self.model.appendRow(QStandardItem(checkbox.text()))

    # ── 전체 선택 / 해제 ──────────────────────────────────────────────────────
    def select_all(self):
        current_tab = self.ui.tabWidget.currentIndex()
        if current_tab in self.tab_checkboxes:
            for cb_item in self.tab_checkboxes[current_tab]:
                cb_item.setChecked(True)

    def unselect_all(self):
        current_tab = self.ui.tabWidget.currentIndex()
        if current_tab in self.tab_checkboxes:
            for cb_item in self.tab_checkboxes[current_tab]:
                cb_item.setChecked(False)

    def exit_button(self):
        self.close()

    # ── ③ 날씨 데이터 수집: QThread 로 비동기 실행 ───────────────────────────
    def collect_weather_data(self):
        selected_locations = self.get_selected_locations()

        if not selected_locations:
            self.printinfo("경고: 수집할 지역이 선택되지 않았습니다.")
            QMessageBox.warning(self, "알림", "수집할 지역을 선택해주세요.")
            return

        # 이전 작업이 아직 돌고 있으면 중복 실행 방지
        if self._thread and self._thread.isRunning():
            QMessageBox.warning(self, "알림", "현재 데이터 수집 중입니다. 잠시 후 다시 시도하세요.")
            return

        # UI 로그 출력
        self.printinfo("=" * 100)
        self.printinfo("날씨 데이터 수집 시작")
        self.printinfo("=" * 100)
        self.printinfo(f"선택된 지역 수: {len(selected_locations)}개")
        self.printinfo()
        for i, loc in enumerate(selected_locations, 1):
            self.printinfo(f"{i:2d}. {loc}")
        self.printinfo()
        self.printinfo("데이터 수집을 시작합니다...")

        # 버튼 비활성화 (수집 중 중복 클릭 방지)
        self.ui.pushButton_1.setEnabled(False)

        # ── QThread + Worker 생성 ──
        self._thread = QThread(self)
        self._worker = ScraperWorker(self.scraper, selected_locations)
        self._worker.moveToThread(self._thread)

        # 시그널 연결
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_scraping_finished)
        self._worker.error.connect(self._on_scraping_error)

        # 워커 종료 시 스레드도 종료
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._on_thread_finished)

        self._thread.start()

    # ── ④ 수집 완료 콜백 (메인 스레드에서 실행됨) ────────────────────────────
    def _on_scraping_finished(self, downloaded_files: list, message: str):
        self.printinfo()
        self.printinfo("── 다운로드 결과 ──")
        for i, file_name in enumerate(downloaded_files, 1):
            self.printinfo(f"{i:2d}. {file_name}")
        self.printinfo(message)
        self.printinfo("=" * 100)
        self.printinfo("모든 데이터 수집을 완료했습니다.")
        self.printinfo("=" * 100)

    # ── ⑤ 에러 콜백 ─────────────────────────────────────────────────────────
    def _on_scraping_error(self, error_msg: str):
        self.printinfo(f"[오류] {error_msg}")
        QMessageBox.critical(self, "오류", error_msg)

    # ── ⑥ 스레드 종료 후 버튼 재활성화 ──────────────────────────────────────
    def _on_thread_finished(self):
        self.ui.pushButton_1.setEnabled(True)
        self.printinfo("(수집 작업 스레드 종료)")

    # ── 선택된 지역 목록 반환 ─────────────────────────────────────────────────
    def get_selected_locations(self):
        selected_locations = []
        for tab_checkboxes in self.tab_checkboxes.values():
            for checkbox in tab_checkboxes:
                if checkbox.isChecked():
                    selected_locations.append(checkbox.text())
        return selected_locations

    # ── printinfo: listView_info + 콘솔 동시 출력 ────────────────────────────
    def printinfo(self, *args, sep=' ', end='\n'):
        text = sep.join(str(arg) for arg in args) + end
        lines = text.splitlines()

        for line in lines:
            self.info_model.appendRow(QStandardItem(line))

        if not lines and end == '\n':
            self.info_model.appendRow(QStandardItem(""))

        self.ui.listView_info.scrollToBottom()
        print(*args, sep=sep, end=end)

    # ── BAS 파일 변환 ──────────────────────────────────────────────────────────
    def convert_to_all(self):
        self.printinfo("=" * 100)
        self.printinfo("Excel VBA 코드로 변환 시작")
        try:
            slist = cb.convert_to_vbacode()
            self.printinfo(f"성공적으로 {len(slist)}개의 파일을 변환하였습니다.")
            self.printinfo("=" * 100)
            for i, item in enumerate(slist):
                self.printinfo(f" {i} : {item}")
            self.printinfo("=" * 100)
            self.printinfo(" 수고하셨습니다. !")
        except Exception as e:
            self.printinfo(f"오류가 발생했습니다: {e}")
            self.printinfo("=" * 100)

        self.combine_bas_files()

    def find_bas_files(self, downloads_path=None):
        self.printinfo()
        if downloads_path is None:
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        return [
            f for f in os.listdir(downloads_path)
            if f.lower().endswith(".bas") and os.path.isfile(os.path.join(downloads_path, f))
        ]

    def combine_bas_files(self):
        source_folder = os.path.expanduser('~/Downloads')
        output_file = r'd:\05_Send\combined.bas'

        if len(self.find_bas_files()) == 0:
            self.printinfo("=" * 100)
            self.printinfo(" .bas 파일이 존재하지 않습니다.")
            self.printinfo("=" * 100)
            return

        self.printinfo("=" * 100)

        if not os.path.isdir('d:\\05_Send\\'):
            self.printinfo(f"오류: 'd:\\05_Send\\' 폴더를 찾을 수 없습니다.")
            os.mkdir('d:\\05_Send\\')
            self.printinfo(f"폴더를 생성하였습니다.")

        if not os.path.isdir(source_folder):
            self.printinfo(f"오류: '{source_folder}' 폴더를 찾을 수 없습니다.")
            return

        with open(output_file, 'w', encoding='utf-8') as outfile:
            self.printinfo(f"'{source_folder}' 폴더의 .bas 파일을 합치는 중...")
            self.printinfo("=" * 100)
            for filename in os.listdir(source_folder):
                if filename.endswith('.bas'):
                    file_path = os.path.join(source_folder, filename)
                    if os.path.isfile(file_path):
                        self.printinfo(f"  - '{filename}' 파일 추가...")
                        try:
                            with open(file_path, 'r', encoding='utf-8') as infile:
                                content = infile.read()
                                outfile.write(f"\n'--- 시작: {filename} ---\n")
                                outfile.write(content)
                                outfile.write(f"\n'--- 끝: {filename} ---\n\n")
                        except Exception as e:
                            self.printinfo(f"    경고: '{filename}' 읽기 오류: {e}")

        self.printinfo("=" * 100)
        self.printinfo(f"\n모든 .bas 파일이 '{output_file}'에 성공적으로 합쳐졌습니다.")
        self.printinfo("=" * 100)


# ── 진입점 ────────────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    window = WeatherDataApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
