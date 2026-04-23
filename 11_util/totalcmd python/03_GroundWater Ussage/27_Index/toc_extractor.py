# 2026/04/21
# 목적 : 목차를 찾아서, 목차파일을 생성해주는데 목적이 있다.

import sys
import glob
import os
import shutil
import time

from pyhwpx import Hwp
from pathlib import Path
import psutil


# ──────────────────────────────────────────────
# 유틸리티 함수 (클래스 외부 독립 함수)
# ──────────────────────────────────────────────

def terminate_all_hwp():
    """실행 중인 모든 HWP 프로세스를 종료한다."""
    for proc in psutil.process_iter(['name']):
        try:
            if 'hwp' in proc.info['name'].lower():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


def progress_bar(iteration, total, prefix='', suffix='', length=30, fill='█'):
    """터미널에 진행률 바를 출력한다."""
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}   ')
    sys.stdout.flush()


# ──────────────────────────────────────────────
# HwpFileManager : 파일 복사 / 경로 탐색
# ──────────────────────────────────────────────

class HwpFileManager:
    """HWP 파일의 경로 탐색과 복사를 담당한다."""

    @staticmethod
    def get_first_file(path: str, extension: str) -> str | None:
        """지정 디렉터리에서 특정 확장자 파일 중 첫 번째를 반환한다."""
        pattern = os.path.join(path, f"*{extension}")
        files = glob.glob(pattern)
        for f in files:
            if os.path.isfile(f):
                return f
        return None

    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """파일을 복사한다. 성공 시 True, 실패 시 False를 반환한다."""
        try:
            shutil.copy2(source, destination)
            print(f"Success: {source} -> {destination}")
            return True
        except FileNotFoundError:
            print("Error: 원본 파일을 찾을 수 없습니다.")
        except PermissionError:
            print("Error: 권한이 없습니다.")
        except Exception as e:
            print(f"Error: {e}")
        return False


# ──────────────────────────────────────────────
# TocExtractor : 목차 페이지 번호 추출
# ──────────────────────────────────────────────

class TocExtractor:
    """HWP 문서를 열어 목차 항목별 페이지 번호를 추출한다."""

    def __init__(self, file_path: str, visible: bool = False):
        self.file_path = file_path
        self.visible = visible
        self._hwp: Hwp | None = None

    # ── 공개 인터페이스 ──────────────────────────

    def extract(self, target_list: list[str]) -> dict[str, int]:
        """
        target_list 를 순회하며 각 텍스트가 위치한 페이지 번호를 반환한다.

        Returns:
            {검색텍스트: 페이지번호} 딕셔너리
        """
        self._open()
        results: dict[str, int] = {}
        total = len(target_list)

        print(f"--- 파일 분석 시작: {self.file_path} ---")
        try:
            for i, target in enumerate(target_list):
                self._scan_text(target)
                progress_bar(i + 1, total, prefix='Progress:', suffix='Complete', length=50)
                results[target] = self._current_page()
        finally:
            self._close()

        return results

    # ── 내부 메서드 ──────────────────────────────

    def _open(self):
        self._hwp = Hwp(visible=self.visible)
        self._hwp.open(self.file_path)

    def _close(self):
        if self._hwp:
            self._hwp.quit()
            self._hwp = None

    def _current_page(self) -> int:
        return self._hwp.KeyIndicator()[3]

    def _scan_text(self, search_text: str) -> set[int]:
        """문서에서 search_text 를 스캔하고 발견 위치로 커서를 이동한다."""
        pages: set[int] = set()
        if not self._hwp.init_scan():
            return pages
        try:
            while True:
                state, text = self._hwp.get_text()
                if state <= 1:
                    break
                if search_text in text:
                    self._hwp.move_pos(201)
                    pages.add(self._current_page())
        finally:
            self._hwp.release_scan()
        return pages


# ──────────────────────────────────────────────
# TocWriter : 목차 HWP 파일에 페이지 번호 기입
# ──────────────────────────────────────────────

class TocWriter:
    """목차 HWP 파일을 열어 누름틀에 데이터를 삽입한다."""

    # 중복 삽입이 필요한 항목 인덱스 (1-based)
    DUPLICATE_INDICES: frozenset[int] = frozenset({4, 7, 11, 12})

    def __init__(self, toc_file_path: str, visible: bool = False):
        self.toc_file_path = toc_file_path
        self.visible = visible

    # ── 공개 인터페이스 ──────────────────────────

    def write(self, page_numbers: list[int]):
        """
        page_numbers 를 목차 HWP 의 누름틀 필드에 순서대로 기입한다.
        """
        print("-- Enter TocWriter.write() --", flush=True)
        hwp = Hwp(visible=self.visible)
        hwp.open(self.toc_file_path)

        field_list = [i for i in hwp.get_field_list(0, 0x02).split("\x02")]
        expanded = self._expand_duplicates(page_numbers)
        total = len(expanded)
        previous_field = "save_field"

        try:
            for idx, (field, data) in enumerate(zip(field_list, expanded), 1):
                progress_bar(idx, total, prefix='Progress:', suffix='Writing Data...', length=50)
                time.sleep(0.05)

                suffix = "{{1}}" if field == previous_field else "{{0}}"
                field_tag = f"{field}{suffix}"

                hwp.MoveToField(field_tag)
                hwp.PutFieldText(field_tag, data)
                previous_field = field

            print()  # 진행률 바 줄바꿈
            self._delete_insert_fields(hwp)
            hwp.save()
        finally:
            hwp.quit()

    # ── 내부 메서드 ──────────────────────────────

    def _expand_duplicates(self, data_list: list) -> list:
        """DUPLICATE_INDICES 에 해당하는 항목을 한 번씩 더 삽입한 리스트를 반환한다."""
        expanded = []
        for i, item in enumerate(data_list, start=1):
            expanded.append(item)
            if i in self.DUPLICATE_INDICES:
                expanded.append(item)
        return expanded

    @staticmethod
    def _delete_insert_fields(hwp: Hwp):
        """
        누름틀(DeleteCtrlType=17)을 모두 제거한다.

        HWP 스크립트 원본:
            HAction.GetDefault("DeleteCtrls", HParameterSet.HDeleteCtrls.HSet);
            HParameterSet.HDeleteCtrls.CreateItemArray("DeleteCtrlType", 1);
            HParameterSet.HDeleteCtrls.DeleteCtrlType.Item(0) = 17;
            HAction.Execute("DeleteCtrls", HParameterSet.HDeleteCtrls.HSet);
        """
        pset = hwp.HParameterSet.HDeleteCtrls
        hwp.HAction.GetDefault("DeleteCtrls", pset.HSet)
        pset.CreateItemArray("DeleteCtrlType", 1)
        pset.DeleteCtrlType.SetItem(0, 17)
        hwp.HAction.Execute("DeleteCtrls", pset.HSet)


# ──────────────────────────────────────────────
# TocPipeline : 전체 파이프라인 조율
# ──────────────────────────────────────────────

class TocPipeline:
    """
    파일 준비 → 페이지 번호 추출 → 목차 기입 의 전체 흐름을 조율한다.

    사용 예:
        pipeline = TocPipeline(
            source_toc   = r"c:\\...\\목차.hwp",
            dest_toc     = r"d:\\06_Send2\\목차.hwp",
            source_dir   = r"d:\\05_Send",
            toc_targets  = [...],
        )
        pipeline.run()
    """

    def __init__(
        self,
        source_toc: str,
        dest_toc: str,
        source_dir: str,
        toc_targets: list[str],
        hwp_extension: str = "hwp",
    ):
        self.source_toc = source_toc
        self.dest_toc = dest_toc
        self.source_dir = source_dir
        self.toc_targets = toc_targets
        self.hwp_extension = hwp_extension

    def run(self):
        """파이프라인 전체를 실행한다."""
        # 1) 기존 HWP 프로세스 종료
        terminate_all_hwp()

        # 2) 목차 템플릿 복사
        ok = HwpFileManager.copy_file(self.source_toc, self.dest_toc)
        if not ok:
            print("목차 파일 복사 실패. 종료합니다.")
            return

        # 3) 분석 대상 파일 탐색
        target_file = HwpFileManager.get_first_file(self.source_dir, self.hwp_extension)
        if not target_file:
            print(f"대상 HWP 파일을 찾을 수 없습니다: {self.source_dir}")
            return

        # 4) 페이지 번호 추출
        extractor = TocExtractor(target_file)
        toc_results = extractor.extract(self.toc_targets)

        # 5) 결과 출력
        print("\n--- 최종 목차 요약 ---")
        for text, pg in toc_results.items():
            print(f"  {text}: {pg}")

        # 6) 목차 파일에 기입
        writer = TocWriter(self.dest_toc)
        writer.write(list(toc_results.values()))


# ──────────────────────────────────────────────
# 진입점
# ──────────────────────────────────────────────

if __name__ == "__main__":

    TOC_TARGETS = [
        "영향조사 결과의 요약",
        "지하수 이용방안",
        "조사서 작성에 관한 사항",
        "II. 수문지질현황 및 원수의 개발가능량",
        "2. 조사지역의 지하수 함양량, 개발가능량 조사",
        "3. 신규 지하수 개발가능량 산정",
        "III. 적정취수량 및 영향범위 산정",
        "2. 적정취수량과 영향반경",
        "3. 잠재오염원과 영향범위",
        "4. 지하수의 개발로 인하여 주변지역에 미치는 영향의 범위 및 정도",
        "IV. 수질의 적정성 평가",
        "Ⅴ. 시설설치계획",
        "2. 사후 관리방안",
        "<  참 고 문 헌  >",
        "<  부    록  >",
    ]

    pipeline = TocPipeline(
        source_toc  = r"c:\Program Files\totalcmd\hwp\목차.hwp",
        dest_toc    = r"d:\06_Send2\목차.hwp",
        source_dir  = r"d:\05_Send",
        toc_targets = TOC_TARGETS,
    )
    pipeline.run()
