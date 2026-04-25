"""
양수파일 생성 프로그램
────────────────────────────────────────────────────────────
2024-12-12 최초 작성
2025     리팩토링

[주의]
파일이름이 GitHub 폴더의 최신 엑셀과 일치하는지 확인 후
Total Commander 디렉터리에서 파일이름을 맞추어 사용할 것.
"""

import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from ui_for_yangsoo_file_generator import Ui_MainWindow

from PrepareYangsoo import PrepareYangsoofile, PrepareYangsooExcel
from AqtProjectInfoInjector import AqtProjectInfoInjector
from AqtExcelProjectInfoInjector import AqtExcelProjectInfoInjector


# ──────────────────────────────────────────────
# 상수
# ──────────────────────────────────────────────
_SEND_DIR       = r'd:\05_Send' + '\\'
_DEFAULT_COMPANY = '주식회사 현우건설'
_RADIO_COUNT    = 16   # radio1 ~ radio16


# ──────────────────────────────────────────────
# MainWindow
# ──────────────────────────────────────────────
class MainWindow(QMainWindow, Ui_MainWindow):
    """
    양수시험 파일 생성·프로젝트 정보 입력 메인 윈도우.

    탭 1 (pushButton)  : 공 수·주소를 직접 입력해 파일 생성 + 정보 입력
    탭 2 (pushButton_3): AQT 파일 유무와 스펙 Excel 유무에 따라 자동 분기
    """

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # ── 상태 ──────────────────────────────
        self.Company = _DEFAULT_COMPANY
        self.Address = ''

        # ── 서비스 객체 ───────────────────────
        self.file_processing = PrepareYangsoofile()
        self.pxel            = PrepareYangsooExcel()
        self.spi             = AqtProjectInfoInjector(_SEND_DIR, '')
        self.spiexcel        = AqtExcelProjectInfoInjector(_SEND_DIR, '')

        # ── UI 초기화 ─────────────────────────
        self._connect_signals()
        self.textEdit_2.setText(f'항목: {_DEFAULT_COMPANY}')

    def _connect_signals(self) -> None:
        """버튼·라디오 시그널을 슬롯에 연결한다."""
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.on_pushButton3_clicked)
        self.pushButton_4.clicked.connect(self.close)

        for i in range(1, _RADIO_COUNT + 1):
            getattr(self, f'radio{i}').toggled.connect(self._on_radio_toggled)

    # ── 헬퍼 ──────────────────────────────────
    def _current_company(self) -> str:
        """radio16(직접 입력)이 선택되어 있으면 텍스트 박스 값을 반환한다."""
        if self.radio16.isChecked():
            return self.textEdit_company.toPlainText()
        return self.Company

    def _current_address(self) -> str:
        return self.textEdit.toPlainText()

    def _has_spec_file(self) -> bool:
        return self.file_processing.is_exist(self.file_processing.YANSOO_SPEC)

    def _spin_value(self) -> int:
        return self.spinBox.value()

    def _checkbox_state(self) -> bool:
        return self.checkBox.isChecked()

    def _log(self, message: str) -> None:
        """textEdit_3 에 상태 메시지를 출력한다."""
        self.textEdit_3.setText(message)

    # ── 슬롯 ──────────────────────────────────
    def _on_radio_toggled(self) -> None:
        """라디오 버튼 선택 시 회사명을 갱신한다."""
        radio = self.sender()
        if not radio.isChecked():
            return
        self.textEdit_2.setText(f'항목: {radio.text()}')
        self.Company = (
            self.textEdit_company.toPlainText()
            if radio.objectName() == 'radio16'
            else radio.text()
        )
        print(f'[radio] Company = {self.Company}')

    def on_pushButton_clicked(self) -> None:
        """
        탭 1 실행 버튼.
        공 수만큼 양수 Excel·AQT 파일을 생성하고 프로젝트 정보를 입력한다.
        """
        spin_value = self._spin_value()
        address    = self._current_address()
        company    = self._current_company()
        step_mode  = self._checkbox_state()

        if not address:
            self._log('주소를 입력해 주세요.')
            return

        self._log(f'{spin_value}개 파일 생성 | 회사: {company} / 주소: {address}')

        self.file_processing.duplicate_yangsoo_excel(spin_value)
        for i in range(1, spin_value + 1):
            self.file_processing.aqtfile_to_send(i, step_mode)

        self.spi.set_project_info(company, address)

    def on_pushButton3_clicked(self) -> None:
        """
        탭 2 실행 버튼.
        스펙 Excel·AQT 파일 유무에 따라 아래 세 경우로 분기한다.

        ① 스펙 O + AQT O  : Excel 기준으로 프로젝트 정보만 입력
        ② 스펙 O + AQT X  : Excel 에서 공 리스트를 읽어 파일 생성 → 정보 입력
        ③ 스펙 X + AQT O  : 직접 입력한 회사·주소로 정보 입력
        ④ 스펙 X + AQT X  : AQT 파일도 복사한 뒤 정보 입력
        """
        self._log('프로젝트 정보 입력 실행 중 ...')
        self.file_processing.set_directory(self.file_processing.SEND)
        aqt_files  = self.file_processing.get_aqt_files()
        has_spec   = self._has_spec_file()
        has_aqt    = len(aqt_files) > 0
        step_mode  = self._checkbox_state()

        if has_spec:
            if has_aqt:
                # ① 스펙 O + AQT O
                self.spiexcel.process_projectinfo_byexcel()
            else:
                # ② 스펙 O + AQT X
                gong_list = self.spiexcel.get_gong_list()
                self.pxel.copy_and_get_yangsoo_file2(gong_list)

                for i in gong_list:
                    self.file_processing.aqtfile_to_send(
                        i,
                        step_mode or self.spiexcel.is_jiyeol,
                    )

                add_one = self.checkBox_addOne.isChecked()
                self.spiexcel.process_projectinfo_byexcel2(addOne=add_one)
        else:
            company = self._current_company()
            address = self._current_address()

            if has_aqt:
                # ③ 스펙 X + AQT O
                print(f'[탭2] 직접 입력 | company={company}, address={address}')
                self.spi.set_project_info(company, address)
            else:
                # ④ 스펙 X + AQT X
                print(f'[탭2] AQT 복사 후 입력 | company={company}, address={address}')
                self._copyaqt_and_set(company, address)

    def _copyaqt_and_set(self, company: str, address: str) -> None:
        """
        AQT 파일을 SEND 폴더로 복사한 뒤 프로젝트 정보를 입력한다.
        (스펙 파일도, AQT 파일도 없는 경우의 fallback)
        """
        spin_value = self._spin_value()
        step_mode  = self._checkbox_state()

        if not address:
            self._log('주소를 입력해 주세요.')
            return

        self._log(f'{spin_value}개 파일 복사 | 회사: {company} / 주소: {address}')

        for i in range(1, spin_value + 1):
            self.file_processing.aqtfile_to_send(i, step_mode)

        self.spi.set_project_info(company, address)


# ──────────────────────────────────────────────
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('windows')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
