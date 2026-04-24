# 2026/04/21
# 목적: HWP 문서의 목차를 자동 생성하는 클래스 기반 리팩토링
# 기능: 특정 텍스트 검색 → 페이지 번호 추출 → 목차 템플릿에 자동 기입

import sys
import glob
import os
import shutil
import time
from pathlib import Path
from typing import Optional, List, Dict, Set

import psutil
from pyhwpx import Hwp


# =============================================================================
# 유틸리티 클래스
# =============================================================================
class HwpUtils:
    """HWP 작업에 필요한 공통 유틸리티 메서드"""

    @staticmethod
    def terminate_all_hwp() -> None:
        """실행 중인 모든 HWP 프로세스 강제 종료"""
        for proc in psutil.process_iter(['name']):
            try:
                if 'hwp' in proc.info['name'].lower():
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    @staticmethod
    def get_first_file(path: str, extension: str) -> Optional[str]:
        """지정된 경로에서 확장자에 해당하는 첫 번째 파일 반환"""
        pattern = os.path.join(path, f"*{extension}")
        for f in glob.glob(pattern):
            if os.path.isfile(f):
                return f
        return None

    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """파일 복사 (메타데이터 포함), 성공 시 True 반환"""
        try:
            shutil.copy2(source, destination)
            print(f"✓ 복사 완료: {source} -> {destination}")
            return True
        except FileNotFoundError:
            print("✗ 오류: 원본 파일을 찾을 수 없습니다.")
        except PermissionError:
            print("✗ 오류: 파일 복사 권한이 없습니다.")
        except Exception as e:
            print(f"✗ 오류: {e}")
        return False

    @staticmethod
    def progress_bar(iteration: int, total: int, prefix: str = '', 
                     suffix: str = '', length: int = 30, fill: str = '█') -> None:
        """콘솔 진행률 표시"""
        percent = f"{100 * (iteration / float(total)):.1f}"
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}   ')
        sys.stdout.flush()
        if iteration == total:
            print()  # 완료 시 줄바꿈


# =============================================================================
# HWP 문서 조작 클래스
# =============================================================================
class HwpDocument:
    """HWP 문서의 읽기/쓰기/조작을 캡슐화한 클래스"""

    # HWP 액션 상수
    ACTION_DELETE_CTRLS = "DeleteCtrls"
    CTRL_TYPE_INSERT_FIELD = 17  # 삽입 필드 타입

    def __init__(self, visible: bool = False):
        self.hwp = Hwp(visible=visible)
        self._is_open = False

    def open(self, file_path: str) -> bool:
        """문서 열기"""
        try:
            self.hwp.open(file_path)
            self._is_open = True
            return True
        except Exception as e:
            print(f"✗ 문서 열기 실패: {file_path} - {e}")
            return False

    def close(self) -> None:
        """문서 닫기 및 리소스 정리"""
        if self._is_open:
            self.hwp.quit()
            self._is_open = False

    def save(self, path: Optional[str] = None) -> bool:
        """문서 저장"""
        try:
            if path:
                self.hwp.save_as(path)
            else:
                self.hwp.save()
            return True
        except Exception as e:
            print(f"✗ 저장 실패: {e}")
            return False

    def get_current_page(self) -> int:
        """현재 페이지 번호 반환"""
        return self.hwp.KeyIndicator()[3]

    def delete_insert_fields(self) -> None:
        """문서 내 모든 삽입 필드(누름틀) 삭제"""
        pset = self.hwp.HParameterSet.HDeleteCtrls
        self.hwp.HAction.GetDefault(self.ACTION_DELETE_CTRLS, pset.HSet)
        pset.CreateItemArray("DeleteCtrlType", 1)
        pset.DeleteCtrlType.SetItem(0, self.CTRL_TYPE_INSERT_FIELD)
        self.hwp.HAction.Execute(self.ACTION_DELETE_CTRLS, pset.HSet)

    def get_field_list(self, start: int = 0, flag: int = 0x02) -> List[str]:
        """문서의 필드 리스트 반환"""
        raw = self.hwp.get_field_list(start, flag)
        return [i for i in raw.split("\x02")] if raw else []

    def move_to_field(self, field_tag: str) -> bool:
        """지정된 필드로 이동"""
        try:
            self.hwp.MoveToField(field_tag)
            return True
        except Exception as e:
            print(f"✗ 필드 이동 실패: {field_tag} - {e}")
            return False

    def put_field_text(self, field_tag: str, text: str) -> bool:
        """필드에 텍스트 기입"""
        try:
            self.hwp.PutFieldText(field_tag, text)
            return True
        except Exception as e:
            print(f"✗ 필드 기입 실패: {field_tag} - {e}")
            return False

    def find_pages_with_text(self, search_text: str) -> List[int]:
        """문서 내 특정 텍스트가 포함된 모든 페이지 번호 반환"""
        pages = set()
        
        if not self.hwp.init_scan():
            return []

        try:
            while True:
                state, text = self.hwp.get_text()
                if state <= 1:  # 문서 끝 또는 오류
                    break
                if search_text in text:
                    self.hwp.move_pos(201)  # 텍스트 위치로 캐럿 이동
                    pages.add(self.get_current_page())
            return sorted(pages)
        finally:
            self.hwp.release_scan()


# =============================================================================
# 목차 생성기 메인 클래스
# =============================================================================
class TableOfContentsGenerator:
    """HWP 문서의 목차를 자동 생성하는 메인 클래스"""

    # 목차 리스트에서 중복이 필요한 인덱스 (1-based)
    DUPLICATE_INDICES: Set[int] = {4, 7, 11, 12}

    def __init__(self, template_path: str, output_dir: str):
        """
        초기화
        :param template_path: 목차 템플릿 HWP 파일 경로
        :param output_dir: 작업 파일이 저장될 출력 디렉토리
        """
        self.template_path = template_path
        self.output_dir = output_dir
        self.output_file = os.path.join(output_dir, "목차.hwp")
        self.toc_results: Dict[str, int] = {}

    def _make_duplicate_list(self, target_list: List[str]) -> List[str]:
        """지정된 인덱스의 항목을 중복하여 새 리스트 반환"""
        new_list = []
        for i, data in enumerate(target_list, start=1):
            new_list.append(data)
            if i in self.DUPLICATE_INDICES:
                new_list.append(data)
        return new_list

    def _search_toc_pages(self, source_file: str, targets: List[str]) -> Dict[str, int]:
        """소스 문서에서 목차 항목별 페이지 번호 검색"""
        results = {}
        doc = HwpDocument(visible=False)
        
        if not doc.open(source_file):
            return results

        try:
            total = len(targets)
            print(f"🔍 목차 검색 시작: {source_file}")
            
            for i, target in enumerate(targets, 1):
                pages = doc.find_pages_with_text(target)
                # 검색된 페이지 중 첫 번째 페이지를 대표값으로 사용
                results[target] = pages[0] if pages else doc.get_current_page()
                HwpUtils.progress_bar(i, total, prefix='  진행:', suffix=f'{target[:10]}...')
                
        finally:
            doc.close()
        
        return results

    def _write_to_template(self, page_numbers: List[int]) -> bool:
        """목차 템플릿에 페이지 번호 기입"""
        doc = HwpDocument(visible=False)
        
        if not doc.open(self.output_file):
            return False

        try:
            field_list = doc.get_field_list()
            data_list = self._make_duplicate_list(page_numbers)
            
            if len(field_list) != len(data_list):
                print(f"⚠ 필드 수({len(field_list)})와 데이터 수({len(data_list)}) 불일치")
                # 불일치 시 가능한 범위까지만 처리
                min_len = min(len(field_list), len(data_list))
                field_list = field_list[:min_len]
                data_list = data_list[:min_len]

            total = len(field_list)
            previous_field = None

            print("✍️ 목차 템플릿 작성 중...")
            for i, (field, data) in enumerate(zip(field_list, data_list), 1):
                HwpUtils.progress_bar(i, total, prefix='  진행:', suffix='Writing...')
                
                # 동일 필드 연속 시 접미사 처리 ({{1}}, {{0}})
                suffix = "{{1}}" if field == previous_field else "{{0}}"
                field_tag = f"{field}{suffix}"

                if doc.move_to_field(field_tag):
                    doc.put_field_text(field_tag, str(data))
                
                previous_field = field
                time.sleep(0.02)  # HWP 액션 간 간격

            # 삽입 필드 정리
            doc.delete_insert_fields()
            return doc.save()
            
        finally:
            doc.close()

    def generate(self, source_file: str, toc_targets: List[str]) -> Optional[Dict[str, int]]:
        """
        목차 생성 메인 메서드
        :param source_file: 분석 대상 HWP 파일 경로
        :param toc_targets: 검색할 목차 항목 리스트
        :return: {목차문자열: 페이지번호} 딕셔너리 또는 실패 시 None
        """
        print(f"\n{'='*60}")
        print(f"📑 목차 자동 생성기 시작")
        print(f"{'='*60}\n")

        # 1. 템플릿 파일 준비
        if not HwpUtils.copy_file(self.template_path, self.output_file):
            print("✗ 템플릿 복사 실패로 작업을 중단합니다.")
            return None

        # 2. 페이지 번호 검색
        self.toc_results = self._search_toc_pages(source_file, toc_targets)
        
        if not self.toc_results:
            print("⚠ 검색된 목차 항목이 없습니다.")
            return {}

        # 3. 결과 출력
        print(f"\n📋 목차 검색 결과 ({len(self.toc_results)} 항목):")
        print("-" * 40)
        for text, page in self.toc_results.items():
            print(f"  {page:3d} 페이지 : {text}")

        # 4. 템플릿에 기입
        page_numbers = list(self.toc_results.values())
        if self._write_to_template(page_numbers):
            print(f"\n✅ 목차 생성 완료: {self.output_file}")
        else:
            print("\n✗ 목차 기입 중 오류가 발생했습니다.")
            return None

        return self.toc_results


# =============================================================================
# 메인 실행 블록
# =============================================================================
if __name__ == "__main__":
    # 설정 상수
    TEMPLATE_SOURCE = r"c:\Program Files\totalcmd\hwp\목차.hwp"
    OUTPUT_DIR = r"d:\06_Send2"
    SOURCE_DIR = r"d:\05_Send"
    
    # 검색할 목차 항목 리스트
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
        "<  부    록  >"
    ]

    # 1. 기존 HWP 프로세스 정리
    HwpUtils.terminate_all_hwp()

    # 2. 소스 파일 확인
    source_file = HwpUtils.get_first_file(SOURCE_DIR, "hwp")
    if not source_file:
        print(f"✗ 대상 파일을 찾을 수 없습니다: {SOURCE_DIR}/*.hwp")
        sys.exit(1)
    
    print(f"📄 분석 대상: {source_file}")

    # 3. 목차 생성기 실행
    generator = TableOfContentsGenerator(
        template_path=TEMPLATE_SOURCE,
        output_dir=OUTPUT_DIR
    )
    
    result = generator.generate(source_file, TOC_TARGETS)
    
    # 4. 종료 처리
    if result is not None:
        print(f"\n🎉 모든 작업이 정상적으로 완료되었습니다.")
    else:
        print(f"\n💥 작업 중 오류가 발생했습니다. 로그를 확인해주세요.")
        sys.exit(1)