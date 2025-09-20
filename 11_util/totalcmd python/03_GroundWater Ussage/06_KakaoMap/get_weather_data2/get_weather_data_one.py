# -*- coding: utf-8 -*-
import sys
import time
import os
import pandas as pd
from datetime import datetime
from typing import List, Optional

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui_file import Ui_MainWindow
import convert_to_bas as cb

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager


class WeatherDataApp(QMainWindow):
    # 기본 지역 데이터
    DEFAULT_AREA_DATA = [
        {"area": "관악산", "name": "GwanAkSan", "Code": 116, "aCode": 15, "switch": 14},
        {"area": "서울", "name": "Seoul", "Code": 108, "aCode": 16, "switch": 14},
        {"area": "강화", "name": "GangHwa", "Code": 201, "aCode": 24, "switch": 23},
        {"area": "백령도", "name": "BaengNyeongDo", "Code": 102, "aCode": 25, "switch": 23},
        {"area": "인천", "name": "InCheon", "Code": 112, "aCode": 26, "switch": 23},
        {"area": "동두천", "name": "DongDuCheon", "Code": 98, "aCode": 34, "switch": 33},
        {"area": "수원", "name": "SuWon", "Code": 119, "aCode": 35, "switch": 33},
        {"area": "양평", "name": "YangPyung", "Code": 202, "aCode": 36, "switch": 33},
        {"area": "이천", "name": "LeeCheon", "Code": 203, "aCode": 37, "switch": 33},
        {"area": "파주", "name": "PaJu", "Code": 99, "aCode": 38, "switch": 33},
        {"area": "강릉", "name": "GangNeung", "Code": 105, "aCode": 40, "switch": 39},
        {"area": "대관령", "name": "DaeGwallYeong", "Code": 100, "aCode": 41, "switch": 39},
        {"area": "동해", "name": "DongHae", "Code": 106, "aCode": 42, "switch": 39},
        {"area": "북강릉", "name": "NorthGangNeung", "Code": 104, "aCode": 43, "switch": 39},
        {"area": "북춘천", "name": "BukChunCheon", "Code": 93, "aCode": 44, "switch": 39},
        {"area": "삼척", "name": "Samcheok", "Code": 214, "aCode": 45, "switch": 39},
        {"area": "속초", "name": "SokCho", "Code": 90, "aCode": 46, "switch": 39},
        {"area": "영월", "name": "YoungWol", "Code": 121, "aCode": 47, "switch": 39},
        {"area": "원주", "name": "WonJu", "Code": 114, "aCode": 48, "switch": 39},
        {"area": "인제", "name": "InJae", "Code": 211, "aCode": 49, "switch": 39},
        {"area": "정선군", "name": "JungSeonGun", "Code": 217, "aCode": 50, "switch": 39},
        {"area": "철원", "name": "CheolWon", "Code": 95, "aCode": 51, "switch": 39},
        {"area": "춘천", "name": "ChunCheon", "Code": 101, "aCode": 52, "switch": 39},
        {"area": "태백", "name": "TaeBaeg", "Code": 216, "aCode": 53, "switch": 39},
        {"area": "홍천", "name": "HongCheon", "Code": 212, "aCode": 54, "switch": 39},
        {"area": "보은", "name": "BoEun", "Code": 226, "aCode": 56, "switch": 55},
        {"area": "서청주", "name": "SeoCheongJu", "Code": 181, "aCode": 57, "switch": 55},
        {"area": "제천", "name": "JaeCheon", "Code": 221, "aCode": 58, "switch": 55},
        {"area": "청주", "name": "CheongJu", "Code": 131, "aCode": 59, "switch": 55},
        {"area": "추풍령", "name": "ChuPungNyeong", "Code": 135, "aCode": 60, "switch": 55},
        {"area": "충주", "name": "ChungJu", "Code": 127, "aCode": 61, "switch": 55},
        {"area": "대전", "name": "DaeJeon", "Code": 133, "aCode": 30, "switch": 29},
        {"area": "세종", "name": "SeJong", "Code": 239, "aCode": 135, "switch": 134},
        {"area": "금산", "name": "GeumSan", "Code": 238, "aCode": 63, "switch": 62},
        {"area": "보령", "name": "BoRyoung", "Code": 235, "aCode": 64, "switch": 62},
        {"area": "부여", "name": "BuYeo", "Code": 236, "aCode": 65, "switch": 62},
        {"area": "서산", "name": "SeoSan", "Code": 129, "aCode": 66, "switch": 62},
        {"area": "천안", "name": "CheonAn", "Code": 232, "aCode": 67, "switch": 62},
        {"area": "홍성", "name": "HongSung", "Code": 177, "aCode": 68, "switch": 62},
        {"area": "광주", "name": "GwangJu", "Code": 156, "aCode": 28, "switch": 27},
        {"area": "고창", "name": "GoChang", "Code": 172, "aCode": 70, "switch": 69},
        {"area": "고창군", "name": "GochangGun", "Code": 251, "aCode": 71, "switch": 69},
        {"area": "군산", "name": "GunSan", "Code": 140, "aCode": 72, "switch": 69},
        {"area": "남원", "name": "NamWon", "Code": 247, "aCode": 73, "switch": 69},
        {"area": "부안", "name": "BuAn", "Code": 243, "aCode": 74, "switch": 69},
        {"area": "순창군", "name": "SunchangGun", "Code": 254, "aCode": 75, "switch": 69},
        {"area": "임실", "name": "ImSil", "Code": 244, "aCode": 76, "switch": 69},
        {"area": "장수", "name": "JangSoo", "Code": 248, "aCode": 77, "switch": 69},
        {"area": "전주", "name": "JeonJu", "Code": 146, "aCode": 78, "switch": 69},
        {"area": "정읍", "name": "Jungeup", "Code": 245, "aCode": 79, "switch": 69},
        {"area": "강진군", "name": "GangjinGun", "Code": 259, "aCode": 81, "switch": 80},
        {"area": "고흥", "name": "Goheung", "Code": 262, "aCode": 82, "switch": 80},
        {"area": "광양시", "name": "Gwangyang", "Code": 266, "aCode": 83, "switch": 80},
        {"area": "목포", "name": "MokPo", "Code": 165, "aCode": 84, "switch": 80},
        {"area": "무안", "name": "MuAn", "Code": 164, "aCode": 85, "switch": 80},
        {"area": "보성군", "name": "BosungGun", "Code": 258, "aCode": 86, "switch": 80},
        {"area": "순천", "name": "Suncheon", "Code": 174, "aCode": 87, "switch": 80},
        {"area": "여수", "name": "Yeosu", "Code": 168, "aCode": 88, "switch": 80},
        {"area": "영광군", "name": "YeongGwangGun", "Code": 252, "aCode": 89, "switch": 80},
        {"area": "완도", "name": "WanDo", "Code": 170, "aCode": 90, "switch": 80},
        {"area": "장흥", "name": "JangHeung", "Code": 260, "aCode": 91, "switch": 80},
        {"area": "주암", "name": "JuAm", "Code": 256, "aCode": 92, "switch": 80},
        {"area": "진도(첨찰산)", "name": "JinDo", "Code": 175, "aCode": 93, "switch": 80},
        {"area": "진도군", "name": "JinDoGun", "Code": 268, "aCode": 94, "switch": 80},
        {"area": "해남", "name": "HaeNam", "Code": 261, "aCode": 95, "switch": 80},
        {"area": "흑산도", "name": "HeukSanDo", "Code": 169, "aCode": 96, "switch": 80},
        {"area": "대구", "name": "DaeGu", "Code": 143, "aCode": 21, "switch": 20},
        {"area": "대구(기)", "name": "DaeGuGi", "Code": 176, "aCode": 22, "switch": 20},
        {"area": "울산", "name": "WoolSan", "Code": 152, "aCode": 32, "switch": 31},
        {"area": "부산", "name": "BuSan", "Code": 159, "aCode": 18, "switch": 17},
        {"area": "경주시", "name": "GyungJuSi", "Code": 283, "aCode": 98, "switch": 97},
        {"area": "구미", "name": "GuMi", "Code": 279, "aCode": 99, "switch": 97},
        {"area": "문경", "name": "MunGyung", "Code": 273, "aCode": 100, "switch": 97},
        {"area": "봉화", "name": "BongHwa", "Code": 271, "aCode": 101, "switch": 97},
        {"area": "상주", "name": "SangJu", "Code": 137, "aCode": 102, "switch": 97},
        {"area": "안동", "name": "AnDong", "Code": 136, "aCode": 103, "switch": 97},
        {"area": "영덕", "name": "YeongDeok", "Code": 277, "aCode": 104, "switch": 97},
        {"area": "영주", "name": "YeongJu", "Code": 272, "aCode": 105, "switch": 97},
        {"area": "영천", "name": "YeongCheon", "Code": 281, "aCode": 106, "switch": 97},
        {"area": "울릉도", "name": "UlLeungDo", "Code": 115, "aCode": 107, "switch": 97},
        {"area": "울진", "name": "UlJin", "Code": 130, "aCode": 108, "switch": 97},
        {"area": "의성", "name": "UiSeong", "Code": 278, "aCode": 109, "switch": 97},
        {"area": "청송군", "name": "CheongSongGun", "Code": 276, "aCode": 110, "switch": 97},
        {"area": "포항", "name": "PoHang", "Code": 138, "aCode": 111, "switch": 97},
        {"area": "거제", "name": "GeoJae", "Code": 294, "aCode": 113, "switch": 112},
        {"area": "거창", "name": "GeoChang", "Code": 284, "aCode": 114, "switch": 112},
        {"area": "김해시", "name": "KimHaeSi", "Code": 253, "aCode": 115, "switch": 112},
        {"area": "남해", "name": "NamHae", "Code": 295, "aCode": 116, "switch": 112},
        {"area": "밀양", "name": "MilYang", "Code": 288, "aCode": 117, "switch": 112},
        {"area": "북창원", "name": "BukChangWon", "Code": 255, "aCode": 118, "switch": 112},
        {"area": "산청", "name": "SanCheong", "Code": 289, "aCode": 119, "switch": 112},
        {"area": "양산시", "name": "YangSan", "Code": 257, "aCode": 120, "switch": 112},
        {"area": "의령군", "name": "UiRyoung", "Code": 263, "aCode": 121, "switch": 112},
        {"area": "진주", "name": "JinJu", "Code": 192, "aCode": 122, "switch": 112},
        {"area": "창원", "name": "ChangWon", "Code": 155, "aCode": 123, "switch": 112},
        {"area": "통영", "name": "TongYeong", "Code": 162, "aCode": 124, "switch": 112},
        {"area": "함양군", "name": "HamYang", "Code": 264, "aCode": 125, "switch": 112},
        {"area": "합천", "name": "HapCheon", "Code": 285, "aCode": 126, "switch": 112},
        {"area": "고산", "name": "GoSan", "Code": 185, "aCode": 128, "switch": 127},
        {"area": "서귀포", "name": "SeoGuiPo", "Code": 189, "aCode": 129, "switch": 127},
        {"area": "성산", "name": "SungSan", "Code": 188, "aCode": 130, "switch": 127},
        {"area": "성산", "name": "SungSan2", "Code": 187, "aCode": 131, "switch": 127},
        {"area": "성산포", "name": "SungSanPo", "Code": 265, "aCode": 132, "switch": 127},
        {"area": "제주", "name": "JaeJu", "Code": 184, "aCode": 133, "switch": 127}
    ]

    DEFAULT_AREAS = ["대전", "보령", "부여", "서산", "천안", "금산", "청주", "보은", "제천", "추풍령", "서울", "인천", "수원"]

    def __init__(self, login_id: str, password: str, download_path: Optional[str] = None):

        """
        RainfallDataScraper 초기화

        Args:
            login_id: 기상청 사이트 로그인 ID
            password: 기상청 사이트 로그인 패스워드
            download_path: 다운로드 경로 (기본값: 사용자 다운로드 폴더)
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.login_id = login_id
        self.password = password
        self.download_path = download_path or os.path.expanduser("~\\Downloads\\")
        self.driver = None
        self.df_areas = pd.DataFrame(self.DEFAULT_AREA_DATA)
        self.url = 'https://data.kma.go.kr/stcs/grnd/grndRnList.do?pgmNo=69'

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
            self.printinfo("=" * 100)
            self.printinfo("날씨 데이터 수집 시작")
            self.printinfo("=" * 100)
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
            # 여기에 실제 날씨 데이터 수집 로직을 구현할 수 있습니다
            # print(f"수집할 지역: {selected_locations}")

            self.download_rainfall_data(selected_locations)

            # for i, location in enumerate(selected_locations):
            #     get_rainfall_data(location)

            self.printinfo("=" * 100)
            self.printinfo("모든 데이터 수집을 완료했습니다...")
            self.printinfo(f"수집할 지역: {selected_locations}")
            self.printinfo("=" * 100)

        else:
            self.printinfo("경고: 수집할 지역이 선택되지 않았습니다.")
            QMessageBox.warning(self, "알림", "수집할 지역을 선택해주세요.")

    def get_selected_locations(self):
        self.printinfo()
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

    def convert_to_all(self):
        self.printinfo("=" * 100)
        self.printinfo("Excel VBA 코드로 변환시작 ")
        try:
            slist = cb.convert_to_vbacode()

            self.printinfo(f"성공적으로 {len(slist)}갯수의 파일을 변환하였습니다.")
            self.printinfo("=" * 100)
            for i, _ in enumerate(slist):
                self.printinfo(f" {i} : {_}")

            self.printinfo("=" * 100)
            self.printinfo(" 수고하셨습니다. ! ")

        except Exception as e:
            self.printinfo(f"오류가 발생했습니다: {e}")
            self.printinfo("=" * 100)

        self.combine_bas_files()

    def find_bas_files(self, downloads_path=None):
        self.printinfo()
        # Default path for Downloads (Windows)
        if downloads_path is None:
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

        bas_files = [
            f for f in os.listdir(downloads_path)
            if f.lower().endswith(".bas") and os.path.isfile(os.path.join(downloads_path, f))
        ]
        return bas_files

    def combine_bas_files(self):
        source_folder = os.path.expanduser('~/Downloads')
        output_file = r'd:\05_Send\combined.bas'

        if len(self.find_bas_files()) == 0:
            self.printinfo("=" * 100)
            self.printinfo(f" .bas 파일이 존재하지 않습니다.")
            self.printinfo("=" * 100)
            return

        self.printinfo("=" * 100)

        if not os.path.isdir('d:\\05_Send\\'):
            self.printinfo(f"오류: 'd:\\05_Send\\' 폴더를 찾을 수 없습니다.")
            os.mkdir('d:\\05_Send\\')
            self.printinfo(f"폴더를 생성하였습니다. ")

        # 소스 폴더가 존재하는지 확인합니다.
        if not os.path.isdir(source_folder):
            self.printinfo(f"오류: '{source_folder}' 폴더를 찾을 수 없습니다.")
            return

        # 합쳐진 내용을 저장할 파일을 쓰기 모드로 엽니다.
        with open(output_file, 'w', encoding='utf-8') as outfile:
            self.printinfo(f"'{source_folder}' 폴더의 .bas 파일을 합치는 중...")
            self.printinfo("=" * 100)

            # 폴더 내 모든 파일 목록을 가져옵니다.
            for filename in os.listdir(source_folder):
                # 파일 확장자가 '.bas'인지 확인합니다.
                if filename.endswith('.bas'):
                    file_path = os.path.join(source_folder, filename)

                    # 파일인지 확인하고 내용을 읽습니다.
                    if os.path.isfile(file_path):
                        self.printinfo(f"  - '{filename}' 파일 추가...")
                        try:
                            with open(file_path, 'r', encoding='utf-8') as infile:
                                content = infile.read()
                                # 파일 내용을 합쳐진 파일에 씁니다.
                                outfile.write(f"\n'--- 시작: {filename} ---\n")
                                outfile.write(content)
                                outfile.write(f"\n'--- 끝: {filename} ---\n\n")
                        except Exception as e:
                            self.printinfo(f"    경고: '{filename}' 파일을 읽는 중 오류가 발생했습니다: {e}")

        self.printinfo("=" * 100)
        self.printinfo(f"\n모든 .bas 파일이 '{output_file}'에 성공적으로 합쳐졌습니다.")
        self.printinfo("=" * 100)

    # ---------------------------------------------------------------------------------------------
    # 여기서 부터는 강우자료 획득 하는 클래스 멤버
    # ---------------------------------------------------------------------------------------------

    def _setup_driver(self) -> webdriver.Chrome:
        """Chrome 드라이버 설정"""
        service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_argument('--start-maximized')
        return webdriver.Chrome(service=service, options=options)

    def _get_last_downloaded_file(self) -> str:
        """다운로드 폴더에서 가장 최근에 다운로드된 파일명 반환"""
        files = [f for f in os.listdir(self.download_path)
                 if os.path.isfile(os.path.join(self.download_path, f))]

        if not files:
            raise FileNotFoundError("다운로드 폴더에 파일이 없습니다.")

        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.download_path, f)))
        return latest_file

    def _rename_file_with_date(self, area_name: str, old_filename: str) -> str:
        """파일명을 지역명과 날짜로 변경"""
        os.chdir(self.download_path)

        base_name, extension = os.path.splitext(old_filename)
        extension = extension[1:]  # 점(.) 제거

        current_date = datetime.now().strftime("%Y-%m-%d")
        new_filename = f'{area_name}_{current_date}.{extension}'

        # 이미 같은 이름의 파일이 있으면 삭제
        if os.path.exists(new_filename):
            print(f"기존 파일 '{new_filename}'을 덮어씁니다.")
            os.remove(new_filename)

        os.rename(old_filename, new_filename)

        print('-----------------------------------------------------------------------')
        print(f"파일명 변경: '{old_filename}' → '{new_filename}'")
        print('-----------------------------------------------------------------------')

        return new_filename

    def _login(self):
        """기상청 사이트 로그인"""
        print("로그인 시작...")

        # 로그인 버튼 클릭
        self.driver.find_element(By.CSS_SELECTOR, "#loginBtn").click()
        time.sleep(1.5)

        # ID 입력
        elem_loginid = self.driver.find_element(By.CSS_SELECTOR, "#loginId")
        elem_loginid.send_keys(self.login_id)
        time.sleep(1.5)

        # 비밀번호 입력
        elem_passwd = self.driver.find_element(By.CSS_SELECTOR, "#passwordNo")
        elem_passwd.send_keys(self.password)
        time.sleep(1.5)

        # 로그인 버튼 클릭
        self.driver.find_element(By.CSS_SELECTOR, "#loginbtn").click()
        time.sleep(1.5)

        print("로그인 완료")

    def _download_area_data(self, area_name: str) -> str:
        """특정 지역의 30년 강우량 데이터 다운로드"""
        self.printinfo(f"'{area_name}' 데이터 다운로드 시작...")

        # 지역 정보 가져오기
        area_info = self.df_areas[self.df_areas['area'] == area_name]
        if area_info.empty:
            raise ValueError(f"지역 '{area_name}'을 찾을 수 없습니다.")

        my_code = area_info['Code'].values[0]
        my_switch = area_info['switch'].values[0]

        one_string = f"ztree_{my_switch}_switch"
        two_string = f"{area_name} ({my_code})"

        self.printinfo(f"Switch ID: {one_string}")
        self.printinfo(f"지역 선택: {two_string}")

        # 월 데이터 선택
        ddl = self.driver.find_element(By.CSS_SELECTOR, "#dataFormCd")
        select = Select(ddl)
        select.select_by_visible_text("월")
        time.sleep(1)

        # 지역 선택
        self.driver.find_element(By.ID, "btnStn").click()
        time.sleep(1)

        self.driver.find_element(By.CSS_SELECTOR, f"#{one_string}").click()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, two_string).click()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, "선택완료").click()
        time.sleep(1)

        # 30년간 데이터 설정 (작년까지 30년)
        end_year = datetime.now().year - 1
        start_year = end_year - 29

        # 시작년도 선택
        ddl = self.driver.find_element(By.CSS_SELECTOR, "#startYear")
        select = Select(ddl)
        select.select_by_visible_text(str(start_year))
        time.sleep(0.5)

        # 끝년도 선택
        ddl = self.driver.find_element(By.CSS_SELECTOR, "#endYear")
        select = Select(ddl)
        select.select_by_visible_text(str(end_year))
        time.sleep(0.5)

        self.printinfo(f"기간: {start_year}년 ~ {end_year}년")

        # 검색 버튼 클릭
        self.driver.find_element(By.CSS_SELECTOR, "button.SEARCH_BTN").click()
        time.sleep(2)

        # 다운로드 버튼 클릭
        self.driver.find_element(By.CSS_SELECTOR, "a.DOWNLOAD_BTN").click()
        time.sleep(3)

        # 다운로드된 파일명 반환
        return self._get_last_downloaded_file()

    def get_available_areas(self) -> List[str]:
        """사용 가능한 지역 목록 반환"""
        return self.df_areas['area'].tolist()

    def download_rainfall_data(self, area_list: Optional[List[str]] = None) -> List[str]:
        if area_list is None:
            area_list = self.DEFAULT_AREAS.copy()

        # 유효하지 않은 지역 체크
        available_areas = self.get_available_areas()
        invalid_areas = [area for area in area_list if area not in available_areas]

        if invalid_areas:
            raise ValueError(f"유효하지 않은 지역: {invalid_areas}")

        downloaded_files = []

        try:
            # 드라이버 설정
            self.driver = self._setup_driver()

            # 웹사이트 접속
            self.driver.get(self.url)
            self.driver.implicitly_wait(20)

            # 페이지 로딩 대기
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#dataFormCd"))
            )
            self.printinfo("페이지 로딩 완료")

            # 로그인
            self._login()

            # 각 지역별 데이터 다운로드
            for area in area_list:
                try:
                    old_filename = self._download_area_data(area)
                    new_filename = self._rename_file_with_date(area, old_filename)

                    downloaded_files.append(new_filename)

                    self.printinfo(f"{area} 다운로드 완료: {new_filename}")
                    self.printinfo("\n\n")

                except Exception as e:
                    self.printinfo(f"'{area}' 다운로드 중 오류 발생: {e}")
                    continue

            self.printinfo(f"\n전체 다운로드 완료! 총 {len(downloaded_files)}개 파일")
            return downloaded_files

        except Exception as e:
            print(f"다운로드 프로세스 중 오류 발생: {e}")
            raise

        finally:
            if self.driver:
                self.driver.quit()
                self.printinfo("브라우저 종료")


def main():
    app = QApplication(sys.argv)
    window = WeatherDataApp(
        login_id="hanseol33@naver.com",
        password="dseq%z8^feyham^"
    )

    # 기본 지역 목록으로 다운로드
    area_list = ["대전", "보령", "부여", "서산", "천안", "금산", "청주", "보은", "제천", "추풍령", "서울", "인천", "수원"]

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
