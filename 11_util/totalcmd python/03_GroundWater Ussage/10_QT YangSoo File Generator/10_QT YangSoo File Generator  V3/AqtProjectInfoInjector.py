import fnmatch
import os
import re
import time

import pyautogui
import pyperclip

from FileManager import FileBase, PathResult


class AqtProjectInfoInjector(FileBase):
    """
    AQTEsolv 프로그램에 프로젝트 정보(회사명, 주소, 공번)를 자동으로 입력한다.

    GUI 자동화(pyautogui)를 사용하므로 실행 중 마우스·키보드 조작을 삼가야 한다.

    Parameters
    ----------
    directory : 작업 디렉터리 경로
    company   : 프로젝트 회사명
    """

    # AQTEsolv 주소 필드 최대 글자 수
    _ADDRESS_MAX_LEN = 20

    def __init__(self, directory: str, company: str) -> None:
        super().__init__(directory)
        self.COMPANY   = company
        self.ADDRESS   = ''
        self.ISAQTOPEN = False
        self.DEBUG     = True

    # ── Setter ────────────────────────────────
    def set_address(self, value: str) -> None:
        self.ADDRESS = value

    def set_company(self, value: str) -> None:
        self.COMPANY = value

    # ── AQTEsolv 열기 / 닫기 ──────────────────
    def open_aqt(self, filename: str) -> None:
        """
        AQTEsolv 를 실행한 뒤 Ctrl+O 로 파일을 연다.
        이미 열려 있으면 실행 단계를 건너뛴다.
        """
        if not self.ISAQTOPEN:
            print(f'open_aqt: {filename}')
            os.startfile(self.AQTESOLV_PATH)
            self.ISAQTOPEN = True
            time.sleep(self.DELAY)

        pyautogui.hotkey('ctrl', 'o')
        pyautogui.press('backspace')
        pyautogui.typewrite(self.SEND + filename)
        time.sleep(self.DELAY)
        pyautogui.press('enter')
        time.sleep(self.DELAY)

    def open_aqt_file(self, filename: str) -> None:
        """
        AQT 파일을 직접 실행해 AQTEsolv 를 연다.
        이미 열려 있으면 건너뛴다.
        """
        if not self.ISAQTOPEN:
            full_path = self.SEND + filename
            print(f'open_aqt_file: {full_path}')
            os.startfile(full_path)
            self.ISAQTOPEN = True
            time.sleep(self.DELAY)

    def close_aqt(self) -> None:
        """열린 AQTEsolv 를 저장(Ctrl+S) 후 종료(Alt+F4)한다."""
        if self.ISAQTOPEN:
            pyautogui.hotkey('ctrl', 's')
            time.sleep(self.DELAY)
            pyautogui.hotkey('alt', 'f4')
            time.sleep(self.DELAY)
        self.ISAQTOPEN = False

    # ── 프로젝트 정보 입력 ────────────────────
    def _input_project_info(self, well: str, address: str) -> None:
        """
        AQTEsolv 의 Project Info 다이얼로그에 회사명·주소·공번을 입력한다.
        (Alt+E → R 로 다이얼로그 열기)

        Parameters
        ----------
        well    : 공번 문자열 (예: 'W-1')
        address : 처리된 주소 문자열
        """
        if not self.ISAQTOPEN:
            return

        time.sleep(0.2)

        # 회사명 입력
        pyperclip.copy(self.COMPANY)
        pyautogui.hotkey('alt', 'e')
        pyautogui.press('r')
        pyautogui.hotkey('ctrl', 'v')

        # 탭 3번 → 주소 필드
        for _ in range(3):
            pyautogui.press('tab')

        # 주소 입력
        pyperclip.copy(address)
        pyautogui.hotkey('ctrl', 'v')

        # 탭 → 공번 필드 (두 칸에 동일하게 입력)
        pyautogui.press('tab')
        pyperclip.copy(well)
        pyautogui.hotkey('ctrl', 'v')

        pyautogui.press('tab')
        pyautogui.hotkey('ctrl', 'v')

        # 확인 후 저장
        pyautogui.press('enter')
        pyautogui.hotkey('ctrl', 's')
        time.sleep(self.DELAY)

    def aqt_mainaction(self, well_no: int, address: str, wfiles: list[str]) -> None:
        """
        파일 리스트를 순회하며 각각 열기 → 정보 입력 → 닫기를 수행한다.

        Parameters
        ----------
        well_no : 공번 정수 (예: 1  →  'W-1' 로 변환)
        address : 처리된 주소 문자열
        wfiles  : 처리할 AQT 파일명 리스트
        """
        for filename in wfiles:
            self.open_aqt_file(filename)
            self._input_project_info(f'W-{well_no}', address)
            self.close_aqt()

    # ── 주소 처리 ─────────────────────────────
    @staticmethod
    def process_address(input_str: str) -> str:
        """
        AQTEsolv Project Info 주소 필드(최대 20자)에 맞도록 주소를 가공한다.

        처리 순서
        ---------
        1. '특별 / 광역 / 자치' 제거  (예: 세종특별자치시 → 세종시)
        2. 연속 공백 정리
        3. ',' 이후 제거
        4. '(' 이후 제거
        5. 20자 초과 시: 시·구·동 단위 이후 부분만 남기고 아파트명 제거

        Returns
        -------
        가공된 주소 문자열
        """
        # 1. 행정구역 수식어 제거
        for word in ('특별', '광역', '자치'):
            input_str = input_str.replace(word, '')
        input_str = re.sub(r'\s+', ' ', input_str).strip()
        print(f'[process_address] 수식어 제거 후: "{input_str}" ({len(input_str)}자)')

        # 2. 쉼표 이후 제거
        if ',' in input_str:
            input_str = input_str.split(',')[0].strip()
            print(f'[process_address] 쉼표 이후 제거: "{input_str}"')

        # 3. 괄호 이후 제거
        if '(' in input_str:
            input_str = input_str.split('(')[0].strip()
            print(f'[process_address] 괄호 이후 제거: "{input_str}"')

        # 4. 20자 초과 시 단축
        if len(input_str) >= 18:
            # '호'로 끝나면 '번지 '를 '-'로 바꾸고 '호' 제거
            if input_str.endswith('호'):
                input_str = input_str.replace('번지 ', '-')[:-1]
            else:
                input_str = input_str.replace('번지', '')

            # 시·구·동 단위 이후만 남기기
            _AREA_SUFFIXES = ('도', '시', '구', '동')
            parts = input_str.split(' ')
            split_idx = 0
            for idx, part in enumerate(parts):
                if part.endswith(_AREA_SUFFIXES):
                    split_idx = idx
                    break

            remaining = parts[split_idx + 1:]
            # 아파트명 및 쉼표 항목 제거
            filtered = [p for p in remaining if not p.endswith('아파트') and p != ',']
            input_str = ' '.join(filtered)
            print(f'[process_address] 단축 결과: "{input_str}" ({len(input_str)}자)')

        return input_str

    # ── 유틸리티 ──────────────────────────────
    @staticmethod
    def extract_number(s) -> int:
        """
        문자열에서 숫자만 추출해 정수로 반환한다.
        숫자가 없거나 변환 실패 시 0을 반환한다.

        Example
        -------
        'w3_02_long.aqt' → 3
        """
        try:
            numbers = re.findall(r'\d+', str(s))
            return int(''.join(numbers)) if numbers else 0
        except (ValueError, Exception) as e:
            print(f'[extract_number] 오류: {e}')
            return 0

    def change_aqt_filename(self) -> None:
        """
        SEND 폴더의 AQT 파일 중 '복사본' 또는 'Copy' 접미어가 붙은 파일을
        '_01' 접미어로 변경한다.
        """
        _COPY_SUFFIXES = (' - 복사본', ' - Copy')

        for filename in self.get_aqt_files():
            name, ext = self.separate_filename(filename)
            if ext != '.aqt' or '_01' in name:
                continue
            for suffix in _COPY_SUFFIXES:
                if suffix in name:
                    new_name = name.replace(suffix, '_01') + ext
                    os.rename(
                        os.path.join(self.SEND, filename),
                        os.path.join(self.SEND, new_name),
                    )
                    print(f'[change_aqt_filename] {filename} → {new_name}')
                    break

    def get_wellno_list_insend(self) -> list[int]:
        """
        SEND 폴더의 AQT 파일에서 공번(정수)을 추출해 중복 없이 반환한다.

        Example
        -------
        ['w1_02_long.aqt', 'w1_03_recover.aqt', 'w2_02_long.aqt'] → [1, 2]
        """
        from natsort import natsorted
        aqtfiles = natsorted(self.get_aqt_files())
        well_nos = {self.extract_number(f.split('_')[0]) for f in aqtfiles}
        return sorted(well_nos)

    # ── 메인 진입점 ───────────────────────────
    def set_project_info(self, company: str, address: str) -> None:
        """
        SEND 폴더의 모든 AQT 파일에 프로젝트 정보를 일괄 입력한다.

        Parameters
        ----------
        company : 회사명
        address : 원본 주소 문자열 (자동으로 가공됨)
        """
        print(f'[set_project_info] company={company!r} / address={address!r}')

        # 1. 파일명 정리
        self.change_aqt_filename()

        # 2. 주소 가공 및 길이 경고
        processed_address = self.process_address(address)
        self.set_company(company)
        self.set_address(processed_address)

        addr_len = len(processed_address)
        print(f'[set_project_info] 처리된 주소: "{processed_address}" ({addr_len}자)')
        if addr_len > self._ADDRESS_MAX_LEN + 1:
            print(f'[set_project_info] ⚠ 주소가 최대 길이({self._ADDRESS_MAX_LEN}자)를 초과합니다.')

        # 3. GUI 자동화 (사용자 입력 차단)
        aqtfiles = self.get_aqt_files()
        print(f'[set_project_info] AQT 파일 목록: {aqtfiles}')

        self.block_user_input()
        try:
            if self.ISAQTOPEN:
                # 이미 열려 있는 상태면 초기화 후 재시도
                self.ISAQTOPEN = False
                return

            if not aqtfiles:
                print('[set_project_info] AQT 파일이 없습니다.')
                return

            for well_no in self.get_wellno_list_insend():
                wfiles = fnmatch.filter(aqtfiles, f'w{well_no}_*.aqt')
                print(f'[set_project_info] well_no={well_no}, 파일={wfiles}')
                if wfiles:
                    self.aqt_mainaction(well_no, processed_address, wfiles)

        finally:
            # 예외 발생 여부와 관계없이 반드시 입력 차단 해제
            time.sleep(0.5)
            self.unblock_user_input()

    # 하위 호환을 위한 별칭
    Set_Projectinfo = set_project_info


# ──────────────────────────────────────────────
if __name__ == '__main__':
    spi = AqtProjectInfoInjector(r'd:\05_Send', '테스트회사')
    print(spi.process_address('충청남도 당진시 송악읍 신평로 1469'))
