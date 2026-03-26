# -*- coding: utf-8 -*-
"""
기상청 강우량 데이터 스크래퍼 - Playwright 비동기 버전
원본 Selenium 코드를 Playwright 로 대체하여 안정성 향상

변경 이유:
  - Selenium + ChromeDriverManager 조합은 Chrome 버전 불일치로 자주 죽음
  - Playwright 는 자체 브라우저 바이너리를 관리하므로 버전 충돌 없음
  - async/await 로 QThread 에서도 안전하게 사용 가능

설치:
  pip install playwright pandas
  playwright install chromium
"""

import asyncio
import os
import glob
import time
from datetime import datetime
from typing import List, Optional, Tuple

import pandas as pd
from playwright.async_api import async_playwright, Page, Browser, BrowserContext, TimeoutError as PWTimeoutError


class RainfallDataScraper:
    """기상청 강우량 데이터를 자동으로 다운로드하는 클래스 (Playwright 버전)"""

    # ── 전체 지역 데이터 (원본과 동일) ─────────────────────────────────────────
    DEFAULT_AREA_DATA = [
        {"area": "관악산",      "name": "GwanAkSan",      "Code": 116, "aCode": 15,  "switch": 14},
        {"area": "서울",        "name": "Seoul",           "Code": 108, "aCode": 16,  "switch": 14},
        {"area": "강화",        "name": "GangHwa",         "Code": 201, "aCode": 24,  "switch": 23},
        {"area": "백령도",      "name": "BaengNyeongDo",   "Code": 102, "aCode": 25,  "switch": 23},
        {"area": "인천",        "name": "InCheon",         "Code": 112, "aCode": 26,  "switch": 23},
        {"area": "동두천",      "name": "DongDuCheon",     "Code": 98,  "aCode": 34,  "switch": 33},
        {"area": "수원",        "name": "SuWon",           "Code": 119, "aCode": 35,  "switch": 33},
        {"area": "양평",        "name": "YangPyung",       "Code": 202, "aCode": 36,  "switch": 33},
        {"area": "이천",        "name": "LeeCheon",        "Code": 203, "aCode": 37,  "switch": 33},
        {"area": "파주",        "name": "PaJu",            "Code": 99,  "aCode": 38,  "switch": 33},
        {"area": "강릉",        "name": "GangNeung",       "Code": 105, "aCode": 40,  "switch": 39},
        {"area": "대관령",      "name": "DaeGwallYeong",   "Code": 100, "aCode": 41,  "switch": 39},
        {"area": "동해",        "name": "DongHae",         "Code": 106, "aCode": 42,  "switch": 39},
        {"area": "북강릉",      "name": "NorthGangNeung",  "Code": 104, "aCode": 43,  "switch": 39},
        {"area": "북춘천",      "name": "BukChunCheon",    "Code": 93,  "aCode": 44,  "switch": 39},
        {"area": "삼척",        "name": "Samcheok",        "Code": 214, "aCode": 45,  "switch": 39},
        {"area": "속초",        "name": "SokCho",          "Code": 90,  "aCode": 46,  "switch": 39},
        {"area": "영월",        "name": "YoungWol",        "Code": 121, "aCode": 47,  "switch": 39},
        {"area": "원주",        "name": "WonJu",           "Code": 114, "aCode": 48,  "switch": 39},
        {"area": "인제",        "name": "InJae",           "Code": 211, "aCode": 49,  "switch": 39},
        {"area": "정선군",      "name": "JungSeonGun",     "Code": 217, "aCode": 50,  "switch": 39},
        {"area": "철원",        "name": "CheolWon",        "Code": 95,  "aCode": 51,  "switch": 39},
        {"area": "춘천",        "name": "ChunCheon",       "Code": 101, "aCode": 52,  "switch": 39},
        {"area": "태백",        "name": "TaeBaeg",         "Code": 216, "aCode": 53,  "switch": 39},
        {"area": "홍천",        "name": "HongCheon",       "Code": 212, "aCode": 54,  "switch": 39},
        {"area": "보은",        "name": "BoEun",           "Code": 226, "aCode": 56,  "switch": 55},
        {"area": "서청주",      "name": "SeoCheongJu",     "Code": 181, "aCode": 57,  "switch": 55},
        {"area": "제천",        "name": "JaeCheon",        "Code": 221, "aCode": 58,  "switch": 55},
        {"area": "청주",        "name": "CheongJu",        "Code": 131, "aCode": 59,  "switch": 55},
        {"area": "추풍령",      "name": "ChuPungNyeong",   "Code": 135, "aCode": 60,  "switch": 55},
        {"area": "충주",        "name": "ChungJu",         "Code": 127, "aCode": 61,  "switch": 55},
        {"area": "대전",        "name": "DaeJeon",         "Code": 133, "aCode": 30,  "switch": 29},
        {"area": "세종",        "name": "SeJong",          "Code": 239, "aCode": 135, "switch": 134},
        {"area": "금산",        "name": "GeumSan",         "Code": 238, "aCode": 63,  "switch": 62},
        {"area": "보령",        "name": "BoRyoung",        "Code": 235, "aCode": 64,  "switch": 62},
        {"area": "부여",        "name": "BuYeo",           "Code": 236, "aCode": 65,  "switch": 62},
        {"area": "서산",        "name": "SeoSan",          "Code": 129, "aCode": 66,  "switch": 62},
        {"area": "천안",        "name": "CheonAn",         "Code": 232, "aCode": 67,  "switch": 62},
        {"area": "홍성",        "name": "HongSung",        "Code": 177, "aCode": 68,  "switch": 62},
        {"area": "광주",        "name": "GwangJu",         "Code": 156, "aCode": 28,  "switch": 27},
        {"area": "고창",        "name": "GoChang",         "Code": 172, "aCode": 70,  "switch": 69},
        {"area": "고창군",      "name": "GochangGun",      "Code": 251, "aCode": 71,  "switch": 69},
        {"area": "군산",        "name": "GunSan",          "Code": 140, "aCode": 72,  "switch": 69},
        {"area": "남원",        "name": "NamWon",          "Code": 247, "aCode": 73,  "switch": 69},
        {"area": "부안",        "name": "BuAn",            "Code": 243, "aCode": 74,  "switch": 69},
        {"area": "순창군",      "name": "SunchangGun",     "Code": 254, "aCode": 75,  "switch": 69},
        {"area": "임실",        "name": "ImSil",           "Code": 244, "aCode": 76,  "switch": 69},
        {"area": "장수",        "name": "JangSoo",         "Code": 248, "aCode": 77,  "switch": 69},
        {"area": "전주",        "name": "JeonJu",          "Code": 146, "aCode": 78,  "switch": 69},
        {"area": "정읍",        "name": "Jungeup",         "Code": 245, "aCode": 79,  "switch": 69},
        {"area": "강진군",      "name": "GangjinGun",      "Code": 259, "aCode": 81,  "switch": 80},
        {"area": "고흥",        "name": "Goheung",         "Code": 262, "aCode": 82,  "switch": 80},
        {"area": "광양시",      "name": "Gwangyang",       "Code": 266, "aCode": 83,  "switch": 80},
        {"area": "목포",        "name": "MokPo",           "Code": 165, "aCode": 84,  "switch": 80},
        {"area": "무안",        "name": "MuAn",            "Code": 164, "aCode": 85,  "switch": 80},
        {"area": "보성군",      "name": "BosungGun",       "Code": 258, "aCode": 86,  "switch": 80},
        {"area": "순천",        "name": "Suncheon",        "Code": 174, "aCode": 87,  "switch": 80},
        {"area": "여수",        "name": "Yeosu",           "Code": 168, "aCode": 88,  "switch": 80},
        {"area": "영광군",      "name": "YeongGwangGun",   "Code": 252, "aCode": 89,  "switch": 80},
        {"area": "완도",        "name": "WanDo",           "Code": 170, "aCode": 90,  "switch": 80},
        {"area": "장흥",        "name": "JangHeung",       "Code": 260, "aCode": 91,  "switch": 80},
        {"area": "주암",        "name": "JuAm",            "Code": 256, "aCode": 92,  "switch": 80},
        {"area": "진도(첨찰산)", "name": "JinDo",          "Code": 175, "aCode": 93,  "switch": 80},
        {"area": "진도군",      "name": "JinDoGun",        "Code": 268, "aCode": 94,  "switch": 80},
        {"area": "해남",        "name": "HaeNam",          "Code": 261, "aCode": 95,  "switch": 80},
        {"area": "흑산도",      "name": "HeukSanDo",       "Code": 169, "aCode": 96,  "switch": 80},
        {"area": "대구",        "name": "DaeGu",           "Code": 143, "aCode": 21,  "switch": 20},
        {"area": "대구(기)",    "name": "DaeGuGi",         "Code": 176, "aCode": 22,  "switch": 20},
        {"area": "울산",        "name": "WoolSan",         "Code": 152, "aCode": 32,  "switch": 31},
        {"area": "부산",        "name": "BuSan",           "Code": 159, "aCode": 18,  "switch": 17},
        {"area": "경주시",      "name": "GyungJuSi",       "Code": 283, "aCode": 98,  "switch": 97},
        {"area": "구미",        "name": "GuMi",            "Code": 279, "aCode": 99,  "switch": 97},
        {"area": "문경",        "name": "MunGyung",        "Code": 273, "aCode": 100, "switch": 97},
        {"area": "봉화",        "name": "BongHwa",         "Code": 271, "aCode": 101, "switch": 97},
        {"area": "상주",        "name": "SangJu",          "Code": 137, "aCode": 102, "switch": 97},
        {"area": "안동",        "name": "AnDong",          "Code": 136, "aCode": 103, "switch": 97},
        {"area": "영덕",        "name": "YeongDeok",       "Code": 277, "aCode": 104, "switch": 97},
        {"area": "영주",        "name": "YeongJu",         "Code": 272, "aCode": 105, "switch": 97},
        {"area": "영천",        "name": "YeongCheon",      "Code": 281, "aCode": 106, "switch": 97},
        {"area": "울릉도",      "name": "UlLeungDo",       "Code": 115, "aCode": 107, "switch": 97},
        {"area": "울진",        "name": "UlJin",           "Code": 130, "aCode": 108, "switch": 97},
        {"area": "의성",        "name": "UiSeong",         "Code": 278, "aCode": 109, "switch": 97},
        {"area": "청송군",      "name": "CheongSongGun",   "Code": 276, "aCode": 110, "switch": 97},
        {"area": "포항",        "name": "PoHang",          "Code": 138, "aCode": 111, "switch": 97},
        {"area": "거제",        "name": "GeoJae",          "Code": 294, "aCode": 113, "switch": 112},
        {"area": "거창",        "name": "GeoChang",        "Code": 284, "aCode": 114, "switch": 112},
        {"area": "김해시",      "name": "KimHaeSi",        "Code": 253, "aCode": 115, "switch": 112},
        {"area": "남해",        "name": "NamHae",          "Code": 295, "aCode": 116, "switch": 112},
        {"area": "밀양",        "name": "MilYang",         "Code": 288, "aCode": 117, "switch": 112},
        {"area": "북창원",      "name": "BukChangWon",     "Code": 255, "aCode": 118, "switch": 112},
        {"area": "산청",        "name": "SanCheong",       "Code": 289, "aCode": 119, "switch": 112},
        {"area": "양산시",      "name": "YangSan",         "Code": 257, "aCode": 120, "switch": 112},
        {"area": "의령군",      "name": "UiRyoung",        "Code": 263, "aCode": 121, "switch": 112},
        {"area": "진주",        "name": "JinJu",           "Code": 192, "aCode": 122, "switch": 112},
        {"area": "창원",        "name": "ChangWon",        "Code": 155, "aCode": 123, "switch": 112},
        {"area": "통영",        "name": "TongYeong",       "Code": 162, "aCode": 124, "switch": 112},
        {"area": "함양군",      "name": "HamYang",         "Code": 264, "aCode": 125, "switch": 112},
        {"area": "합천",        "name": "HapCheon",        "Code": 285, "aCode": 126, "switch": 112},
        {"area": "고산",        "name": "GoSan",           "Code": 185, "aCode": 128, "switch": 127},
        {"area": "서귀포",      "name": "SeoGuiPo",        "Code": 189, "aCode": 129, "switch": 127},
        {"area": "성산",        "name": "SungSan",         "Code": 188, "aCode": 130, "switch": 127},
        {"area": "성산2",       "name": "SungSan2",        "Code": 187, "aCode": 131, "switch": 127},
        {"area": "성산포",      "name": "SungSanPo",       "Code": 265, "aCode": 132, "switch": 127},
        {"area": "제주",        "name": "JaeJu",           "Code": 184, "aCode": 133, "switch": 127},
        {"area": "전국",        "name": "JeonKook",        "Code": 0,   "aCode": 3,   "switch": 2},
        {"area": "서울경기",    "name": "SeoulGyungi",     "Code": 0,   "aCode": 4,   "switch": 2},
        {"area": "강원영동",    "name": "GangWonEast",     "Code": 0,   "aCode": 5,   "switch": 2},
        {"area": "강원영서",    "name": "GangWonWest",     "Code": 0,   "aCode": 6,   "switch": 2},
        {"area": "충북",        "name": "ChungBook",       "Code": 0,   "aCode": 7,   "switch": 2},
        {"area": "충남",        "name": "ChungNam",        "Code": 0,   "aCode": 8,   "switch": 2},
        {"area": "경북",        "name": "GyungBook",       "Code": 0,   "aCode": 9,   "switch": 2},
        {"area": "경남",        "name": "GyungNam",        "Code": 0,   "aCode": 10,  "switch": 2},
        {"area": "전북",        "name": "JeonBook",        "Code": 0,   "aCode": 11,  "switch": 2},
        {"area": "전남",        "name": "JeonNam",         "Code": 0,   "aCode": 12,  "switch": 2},
        {"area": "제주도",      "name": "Jejudo",          "Code": 0,   "aCode": 13,  "switch": 2},
    ]

    DEFAULT_AREAS = [
        "대전", "보령", "부여", "서산", "천안", "금산",
        "청주", "보은", "제천", "추풍령", "서울", "인천", "수원"
    ]

    # ── 초기화 ──────────────────────────────────────────────────────────────────
    def __init__(self, login_id: str, password: str, download_path: Optional[str] = None):
        self.login_id    = login_id
        self.password    = password
        self.download_path = download_path or os.path.join(os.path.expanduser("~"), "Downloads")
        self.df_areas    = pd.DataFrame(self.DEFAULT_AREA_DATA)
        self.url         = "https://data.kma.go.kr/stcs/grnd/grndRnList.do?pgmNo=69"

        # Playwright 객체 (download_rainfall_data 안에서 생성/해제)
        self._browser: Optional[Browser]        = None
        self._context: Optional[BrowserContext] = None
        self._page:    Optional[Page]           = None

    # ── 유틸리티 ────────────────────────────────────────────────────────────────
    def get_available_areas(self) -> List[str]:
        return self.df_areas["area"].tolist()

    def _rename_file_with_date(self, area_name: str, old_filename: str) -> str:
        """파일명을 '지역명_YYYY-MM-DD.csv' 형식으로 변경 (원본 로직 유지)"""
        full_old = os.path.join(self.download_path, old_filename)
        _, ext   = os.path.splitext(old_filename)        # ext 예: ".csv"
        ext      = ext.lstrip(".")                       # "csv"

        current_date = datetime.now().strftime("%Y-%m-%d")
        new_filename = f"{area_name}_{current_date}.{ext}"
        full_new     = os.path.join(self.download_path, new_filename)

        if os.path.exists(full_new):
            print(f"기존 파일 '{new_filename}'을 덮어씁니다.")
            os.remove(full_new)

        os.rename(full_old, full_new)
        print("-----------------------------------------------------------------------")
        print(f"파일명 변경: '{old_filename}' → '{new_filename}'")
        print("-----------------------------------------------------------------------")
        return new_filename

    # ── Playwright 내부 헬퍼 ────────────────────────────────────────────────────
    async def _login(self) -> None:
        """기상청 로그인 (Playwright)"""
        print("로그인 시작...")
        page = self._page

        # 로그인 버튼 → 팝업/폼 대기
        await page.click("#loginBtn")
        await page.wait_for_selector("#loginId", timeout=10_000)

        # ID / PW 입력 후 제출
        await page.fill("#loginId",    self.login_id)
        await page.fill("#passwordNo", self.password)
        await page.click("#loginbtn")

        # 로그인 후 페이지 안정화 대기 (원본과 동일한 1.5 초)
        await asyncio.sleep(1.5)
        print("로그인 완료")

    async def _select_option_by_text(self, selector: str, text: str) -> None:
        """<select> 요소에서 보이는 텍스트로 옵션 선택 (Playwright 전용)"""
        await self._page.select_option(selector, label=text)

    async def _download_area_data(self, area_name: str) -> str:
        """
        특정 지역의 30년 강우량 데이터를 다운로드하고 임시 파일명을 반환.
        원본 Selenium 로직을 그대로 이식.
        """
        print(f"'{area_name}' 데이터 다운로드 시작...")
        page = self._page

        # ── 지역 코드 조회 ─────────────────────────────────────────────────────
        area_info = self.df_areas[self.df_areas["area"] == area_name]
        if area_info.empty:
            raise ValueError(f"지역 '{area_name}'을 찾을 수 없습니다.")

        # 성산2 는 원본과 동일하게 하드코딩
        if area_name == "성산2":
            my_code   = 187
            my_switch = 127
        else:
            my_code   = int(area_info["Code"].values[0])
            my_switch = int(area_info["switch"].values[0])

        # CSS ID (원본: "ztree_{switch}_switch")
        switch_css = f"#ztree_{my_switch}_switch"

        # 화면에 표시되는 지역명 (원본 로직 동일)
        if my_code == 0:
            two_string = "제주" if area_name == "제주도" else area_name
        else:
            two_string = f"성산 ({my_code})" if area_name == "성산2" else f"{area_name} ({my_code})"

        print(f"Switch CSS : {switch_css}")
        print(f"지역 선택  : {two_string}")

        # ── 월 데이터 선택 ────────────────────────────────────────────────────
        await self._select_option_by_text("#dataFormCd", "월")
        await asyncio.sleep(1)

        # ── 지역 선택 팝업 ────────────────────────────────────────────────────
        await page.click("#btnStn")
        await asyncio.sleep(1)

        # 트리에서 상위 노드(switch) 클릭 → 펼치기
        await page.wait_for_selector(switch_css, timeout=10_000)
        await page.click(switch_css)
        await asyncio.sleep(1)

        # 지역명 링크 클릭 (LINK_TEXT 방식 → get_by_text + exact)
        await page.get_by_role("link", name=two_string, exact=True).click()
        await asyncio.sleep(1)

        # 선택완료
        await page.get_by_role("link", name="선택완료", exact=True).click()
        await asyncio.sleep(1)

        # ── 기간 설정: 작년까지 30년 ─────────────────────────────────────────
        end_year   = datetime.now().year - 1
        start_year = end_year - 29

        await self._select_option_by_text("#startYear", str(start_year))
        await asyncio.sleep(0.5)
        await self._select_option_by_text("#endYear",   str(end_year))
        await asyncio.sleep(0.5)

        print(f"기간: {start_year}년 ~ {end_year}년")

        # ── 검색 ──────────────────────────────────────────────────────────────
        await page.click("button.SEARCH_BTN")
        # 전국/광역 데이터는 서버 처리가 오래 걸림 (원본 동일)
        wait_sec = 8 if my_code == 0 else 3
        await asyncio.sleep(wait_sec)

        # ── 다운로드 ──────────────────────────────────────────────────────────
        # expect_download() 로 실제 파일 저장까지 대기
        async with page.expect_download(timeout=60_000) as dl_info:
            await page.click("a.DOWNLOAD_BTN")

        download     = await dl_info.value
        suggested    = download.suggested_filename
        save_path    = os.path.join(self.download_path, suggested)

        await download.save_as(save_path)
        print(f"임시 저장: {save_path}")
        return suggested

    # ── 공개 메서드: 메인 다운로드 프로세스 ────────────────────────────────────
    async def download_rainfall_data(
        self,
        area_list: Optional[List[str]] = None
    ) -> Tuple[List[str], str]:
        """
        강우량 데이터 다운로드 (비동기 메인 메서드)

        Returns:
            (다운로드된 파일명 목록, 결과 메시지 문자열)
        """
        if area_list is None:
            area_list = self.DEFAULT_AREAS.copy()

        # 유효하지 않은 지역 사전 체크
        available = self.get_available_areas()
        invalid   = [a for a in area_list if a not in available]
        if invalid:
            raise ValueError(f"유효하지 않은 지역: {invalid}")

        downloaded_files: List[str] = []
        message = "=" * 60 + "\n"

        async with async_playwright() as pw:
            # ── 브라우저 시작 ────────────────────────────────────────────────
            self._browser = await pw.chromium.launch(
                headless=False,          # 눈으로 확인하려면 False, 자동화 시 True
                args=["--start-maximized"]
            )
            # 다운로드 디렉터리 설정
            self._context = await self._browser.new_context(
                accept_downloads=True,
                viewport=None            # --start-maximized 와 함께 사용
            )
            self._page = await self._context.new_page()

            try:
                # 페이지 진입 및 로딩 대기
                await self._page.goto(self.url, wait_until="networkidle", timeout=30_000)
                await self._page.wait_for_selector("#dataFormCd", timeout=15_000)
                print("페이지 로딩 완료")
                message += "페이지 로딩 완료\n"

                # 로그인
                await self._login()

                # 지역별 순차 다운로드
                for area in area_list:
                    try:
                        temp_name  = await self._download_area_data(area)
                        final_name = self._rename_file_with_date(area, temp_name)
                        downloaded_files.append(final_name)
                        ok_msg = f"'{area}' 다운로드 완료: {final_name}\n"
                        print(ok_msg)
                        message += ok_msg

                    except PWTimeoutError as e:
                        err_msg = f"'{area}' 타임아웃 오류: {e}\n"
                        print(err_msg)
                        message += err_msg
                        # 팝업이 열린 채로 멈출 수 있으므로 ESC 로 닫기 시도
                        try:
                            await self._page.keyboard.press("Escape")
                            await asyncio.sleep(0.5)
                        except Exception:
                            pass

                    except Exception as e:
                        err_msg = f"'{area}' 오류: {e}\n"
                        print(err_msg)
                        message += err_msg

                final_msg = f"\n전체 완료! 총 {len(downloaded_files)}개 파일 다운로드\n"
                print(final_msg)
                message += final_msg

            except Exception as e:
                fatal_msg = f"치명적 오류 발생: {e}\n"
                print(fatal_msg)
                message += fatal_msg

            finally:
                await self._browser.close()
                print("브라우저 종료")

        return downloaded_files, message


# ── 단독 실행 예시 ─────────────────────────────────────────────────────────────
async def _main():
    scraper = RainfallDataScraper(
        login_id="hanseol33@naver.com",
        password="dseq%z8^feyham^"
    )

    # area_list = ["전국"]
    area_list = ["대전", "서울", "인천"]

    downloaded, msg = await scraper.download_rainfall_data(area_list)
    print(msg)
    print(f"다운로드된 파일: {downloaded}")


if __name__ == "__main__":
    asyncio.run(_main())
