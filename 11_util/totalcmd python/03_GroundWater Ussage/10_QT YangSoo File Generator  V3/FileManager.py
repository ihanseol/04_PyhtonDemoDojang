import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime

import fnmatch
import os
import ctypes
from natsort import natsorted


# ──────────────────────────────────────────────
# 상수 정의
# ──────────────────────────────────────────────
class PathResult:
    """check_path() 반환값 상수."""
    FILE    = 1
    DIR     = 2
    NOTHING = 0


# ──────────────────────────────────────────────
# AQTBASE : 프로젝트 전역 설정값
# ──────────────────────────────────────────────
class AQTBASE:
    """AQTEsolv 프로젝트에서 공통으로 사용하는 경로·상수 모음."""

    # 주요 경로
    AQTESOLV_PATH  = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
    DOCUMENTS      = os.path.expanduser(r'~\Documents')
    SEND           = r'D:\05_Send' + '\\'
    SEND2          = r'D:\06_Send2' + '\\'

    # 양수 Excel 파일명
    YANGSOO_EXCEL  = 'A1_ge_OriginalSaveFile.xlsm'
    YANGSOO_REST   = '_ge_OriginalSaveFile.xlsm'
    YANSOO_SPEC    = r'd:\05_Send\YanSoo_Spec.xlsx'

    # GitHub 연동 폴더 (2025-09-28 추가)
    YANGSOO_GITHUB = r'd:\12_dev\02_Excel4\01_Acquifer Pumping Test\01_양수시험'

    # Total Commander AQT 폴더
    TC_DIR         = r'C:\Program Files\totalcmd\AqtSolv' + '\\'

    # AQT 파일명 접미어
    STEP_FILE      = '_01_step.aqt'
    LONG_FILE      = '_02_long.aqt'
    RECOVER_FILE   = '_03_recover.aqt'

    # 디버그·동작 플래그
    DEBUG_YES = True
    DELAY     = 0.2
    # IS_BLOCK=False : 프로그램 실행 중 사용자 입력을 막으면 아무것도 못 하므로 False 유지
    IS_BLOCK  = False

    def print_debug(self, message: str) -> None:
        """DEBUG_YES가 True일 때만 메시지를 출력한다."""
        if self.DEBUG_YES:
            print(message)

    # ── 사용자 입력 차단/해제 ──────────────────
    @staticmethod
    def block_user_input() -> None:
        ctypes.windll.user32.BlockInput(True)

    @staticmethod
    def unblock_user_input() -> None:
        ctypes.windll.user32.BlockInput(False)


# ──────────────────────────────────────────────
# PathChecker : 경로 존재 여부 확인 유틸리티
# ──────────────────────────────────────────────
class PathChecker:
    """경로가 파일인지, 디렉터리인지, 없는지 판별하는 정적 유틸리티."""

    # 하위 호환을 위해 클래스 속성으로도 노출
    RET_FILE    = PathResult.FILE
    RET_DIR     = PathResult.DIR
    RET_NOTHING = PathResult.NOTHING

    @staticmethod
    def check_path(path: str = '') -> int:
        """
        경로 종류를 반환한다.

        Returns
        -------
        PathResult.FILE    : 파일
        PathResult.DIR     : 디렉터리
        PathResult.NOTHING : 존재하지 않음 또는 None
        """
        if not path or not os.path.exists(path):
            return PathResult.NOTHING
        if os.path.isfile(path):
            return PathResult.FILE
        if os.path.isdir(path):
            return PathResult.DIR
        return PathResult.NOTHING

    def resolve_path(self, path: str = '') -> int:
        """check_path 결과를 콘솔에 출력하고 반환한다."""
        result = self.check_path(path)
        labels = {
            PathResult.FILE:    'File',
            PathResult.DIR:     'DIR',
            PathResult.NOTHING: 'NOTHING',
        }
        print(f"Given Path is {labels.get(result, 'NOTHING')}")
        return result


# ──────────────────────────────────────────────
# FileBase : 파일/디렉터리 조작의 핵심 클래스
# ──────────────────────────────────────────────
class FileBase(AQTBASE, PathChecker):
    """
    파일 목록 조회·복사·이동·삭제 등 파일 시스템 작업을 담당한다.

    Parameters
    ----------
    directory : str
        작업 기본 디렉터리. 유효하지 않으면 SEND 경로로 대체된다.
    """

    def __init__(self, directory: str = r'D:\05_Send' + '\\') -> None:
        AQTBASE.__init__(self)

        fallback = self.SEND
        target   = directory if self.check_path(directory) == PathResult.DIR else fallback

        if directory and self.check_path(directory) != PathResult.DIR:
            print(f'[FileBase] 유효하지 않은 경로 → 기본값 사용: {fallback}')

        self.files: list[str] = []
        self._directory: str  = ''
        self._set_directory(target)

    # ── 디렉터리 관리 ─────────────────────────
    def _set_directory(self, directory: str) -> None:
        """작업 디렉터리를 변경하고 파일 목록을 갱신한다."""
        self._directory = directory
        os.chdir(self._directory)
        self.files = os.listdir(directory)

    @property
    def directory(self) -> str:
        return self._directory

    @directory.setter
    def directory(self, value: str) -> None:
        if self._directory != value:
            self._set_directory(value)

    def set_directory(self, directory: str) -> None:
        """외부에서 디렉터리를 재설정할 때 사용한다."""
        self._set_directory(directory)

    # ── 파일 목록 조회 ────────────────────────
    def _get_files_by_extension(self, extension: str) -> list[str]:
        """지정한 확장자를 가진 파일 목록을 반환한다."""
        self.files = os.listdir(self._directory)
        return [f for f in self.files if f.lower().endswith(extension.lower())]

    def get_xlsm_files(self)  -> list[str]: return self._get_files_by_extension('.xlsm')
    def get_xlsx_files(self)  -> list[str]: return self._get_files_by_extension('.xlsx')
    def get_aqt_files(self)   -> list[str]: return self._get_files_by_extension('.aqt')
    def get_dat_files(self)   -> list[str]: return self._get_files_by_extension('.dat')
    def get_prn_files(self)   -> list[str]: return self._get_files_by_extension('.prn')  # 버그 수정: .dat → .prn
    def get_pdf_files(self)   -> list[str]: return self._get_files_by_extension('.pdf')
    def get_jpg_files(self)   -> list[str]: return self._get_files_by_extension('.jpg')

    def get_image_files(self) -> list[str]:
        """jpg / jpeg / png 파일 목록을 반환한다."""
        return self.get_list_files(['.jpg', '.jpeg', '.png'])

    def get_list_files(self, extensions: list[str]) -> list[str]:
        """
        여러 확장자에 해당하는 파일 목록을 합쳐 반환한다.

        Parameters
        ----------
        extensions : ['.dat', '.jpg', '.xlsm']
        """
        result: list[str] = []
        for ext in extensions:
            result.extend(self._get_files_by_extension(ext))
        return result

    # ── 필터링 조회 ───────────────────────────
    def _get_filtered(
        self,
        getter,
        path: str | None = None,
        sfilter: str = '*',
    ) -> list[str]:
        """공통 필터 로직: 경로를 선택적으로 변경한 뒤 패턴으로 필터링한다."""
        if path:
            self.set_directory(path)
        return natsorted(fnmatch.filter(getter(), sfilter))

    def get_xlsm_filter(self, path=None, sfilter='*_ge_OriginalSaveFile.xlsm') -> list[str]:
        return self._get_filtered(self.get_xlsm_files, path, sfilter)

    def get_xlsmlist_filter(self, path=None, sfilter='*.xlsm') -> list[str]:
        return self._get_filtered(self.get_xlsm_files, path, sfilter)

    def get_jpg_filter(self, path=None, sfilter='*page1.jpg') -> list[str]:
        return self._get_filtered(self.get_jpg_files, path, sfilter)

    def get_file_filter(self, path=None, sfilter='*.hwp') -> list[str]:
        """임의 확장자 패턴으로 파일을 필터링한다."""
        if path:
            self.set_directory(path)
        self.files = os.listdir(self._directory)
        return natsorted(fnmatch.filter(self.files, sfilter))

    # ── 경로 분석 ─────────────────────────────
    @staticmethod
    def has_path(file_name: str) -> bool:
        """파일명에 디렉터리 경로가 포함되어 있으면 True."""
        head, tail = os.path.split(file_name)
        print(f"head: '{head}'  tail: '{tail}'")
        return bool(head)

    @staticmethod
    def separate_filename(filename: str) -> tuple[str, str]:
        """파일명을 이름과 확장자로 분리한다. (오타 수정: seperate → separate)"""
        return os.path.splitext(filename)

    # 하위 호환을 위한 별칭
    seperate_filename = separate_filename

    @staticmethod
    def separate_path(file_path: str) -> tuple[str, str]:
        """(디렉터리, 파일명) 튜플을 반환한다."""
        return os.path.dirname(file_path), os.path.basename(file_path)

    @staticmethod
    def last_one(path: str) -> str:
        """경로의 마지막 구성 요소(폴더명 또는 파일명)를 반환한다."""
        return os.path.basename(path.rstrip('\\/'))

    # ── 숨김 파일·폴더 ────────────────────────
    @staticmethod
    def is_hidden(filepath: str) -> bool:
        """Windows에서 숨김 속성이 설정된 경로면 True."""
        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(filepath))
            assert attrs != -1
            return bool(attrs & 2)  # FILE_ATTRIBUTE_HIDDEN
        except (AssertionError, AttributeError):
            return False

    @staticmethod
    def list_directory_contents(path: str) -> list[str] | str:
        """디렉터리의 모든 항목(숨김 포함)을 반환한다."""
        try:
            return os.listdir(path)
        except FileNotFoundError:
            return f"디렉터리 '{path}'가 존재하지 않습니다."
        except PermissionError:
            return f"'{path}'에 대한 접근 권한이 없습니다."
        except Exception as e:
            return f"오류 발생: {e}"

    @staticmethod
    def list_non_hidden_directories(path: str) -> list[str] | str:
        """숨김이 아닌 하위 디렉터리 목록을 반환한다."""
        try:
            return [
                entry for entry in os.listdir(path)
                if os.path.isdir(os.path.join(path, entry))
                and not entry.startswith('.')
            ]
        except FileNotFoundError:
            return f"디렉터리 '{path}'가 존재하지 않습니다."
        except PermissionError:
            return f"'{path}'에 대한 접근 권한이 없습니다."
        except Exception as e:
            return f"오류 발생: {e}"

    def list_hidden_directories(self, path: str) -> list[str] | str:
        """숨김 하위 디렉터리 목록을 반환한다."""
        try:
            entries = os.listdir(path)
            return [
                os.path.basename(os.path.join(path, entry))
                for entry in entries
                if os.path.isdir(os.path.join(path, entry))
                and self.is_hidden(os.path.join(path, entry))
            ]
        except FileNotFoundError:
            return f"디렉터리 '{path}'가 존재하지 않습니다."
        except PermissionError:
            return f"'{path}'에 대한 접근 권한이 없습니다."
        except Exception as e:
            return f"오류 발생: {e}"

    def list_directories_only(self, path: str) -> list[str] | str:
        """비숨김 디렉터리만 반환한다."""
        non_hidden = self.list_non_hidden_directories(path)
        hidden     = self.list_hidden_directories(path)

        if isinstance(non_hidden, str) or isinstance(hidden, str):
            return "디렉터리 목록을 가져오는 중 오류가 발생했습니다."

        hidden_set = set(hidden)
        return [d for d in non_hidden if d not in hidden_set]

    # ── 경로 결합 ─────────────────────────────
    @staticmethod
    def set_pathstring_to_slash(file_path: str) -> str:
        r"""경로의 역슬래시(\)를 슬래시(/)로 통일한다."""
        return file_path.replace('\\', '/')

    def join_path_from_list(self, file_path_list: list[str]) -> str:
        """
        경로 조각 리스트를 하나의 경로 문자열로 합친다.

        Example
        -------
        ['d:/send/', 'path1', 'path2'] → 'd:/send/path1/path2'
        """
        parts = [self.set_pathstring_to_slash(p) for p in file_path_list]
        result = ''.join(parts)
        print('join_path_from_list:', result)
        return result

    def join_path_tofilename(self, folder_path: str, file_name: str) -> str:
        """폴더 경로와 파일명을 결합해 전체 경로를 반환한다."""
        if self.check_path(folder_path) == PathResult.DIR:
            source = os.path.join(folder_path, file_name).replace('/', '\\')
        else:
            source = folder_path
        print('join_path:', source)
        return source

    def unfold_path(self, folder_path: str) -> list[str]:
        """경로를 구분자로 분리해 리스트로 반환한다."""
        if not self.check_path(folder_path):
            folder_path = self.SEND
        parts = folder_path.replace('/', '\\').split('\\')
        for part in parts:
            print(part)
        return parts

    @staticmethod
    def join_path_reverse(folder_list: list[str], n: int = 0) -> str | None:
        """
        경로 리스트를 결합한다. n > 0이면 끝에서 n개를 제외한다.

        Example
        -------
        (['D:', 'a', 'b', 'c'], n=1) → 'D:\\a\\b'
        """
        if not isinstance(folder_list, list):
            return None
        if n == 0:
            return '\\'.join(folder_list)
        elif n > 0:
            return '\\'.join(folder_list[:-n])
        else:
            return '\\'.join(folder_list[:n])

    @staticmethod
    def join_path_forward(folder_list: list[str], n: int = 0) -> str | None:
        """
        경로 리스트의 앞에서 n개만 결합한다.

        Example
        -------
        (['D:', 'a', 'b', 'c'], n=2) → 'D:\\a'
        """
        if not folder_list:
            return None
        n = abs(n)
        return '\\'.join(folder_list[:n]) if n else '\\'.join(folder_list)

    # ── 경로 속성 조회 ────────────────────────
    def get_dirname(self, file_path: str) -> str | None:
        """파일 경로에서 디렉터리 부분을 반환한다."""
        if self.check_path(file_path) == PathResult.NOTHING:
            print('get_dirname: 유효하지 않은 경로 →', file_path)
            return None
        return os.path.dirname(file_path) + '\\'

    def get_basename(self, file_path: str) -> str | None:
        """파일 경로에서 파일명 부분을 반환한다."""
        if self.check_path(file_path) == PathResult.NOTHING:
            print('get_basename: 유효하지 않은 경로 →', file_path)
            return None
        return os.path.basename(file_path)

    def is_exist(self, file_path: str) -> bool:
        """파일 또는 디렉터리가 존재하면 True."""
        return self.check_path(file_path) != PathResult.NOTHING

    # is_valid는 is_exist의 별칭
    is_valid = is_exist

    # ── 파일 조작 ─────────────────────────────
    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """source → destination 으로 파일을 복사한다."""
        try:
            shutil.copy(source, destination)
            print(f"복사 완료: '{source}' → '{destination}'")
            return True
        except Exception as e:
            print(f"복사 실패: {e}")
            return False

    @staticmethod
    def move_file(source: str, destination: str) -> bool:
        """source → destination 으로 파일을 이동한다. 목적지에 파일이 있으면 덮어쓴다."""
        try:
            if os.path.exists(destination):
                os.remove(destination)
                print(f"기존 파일 삭제: {destination}")
            shutil.move(source, destination)
            print(f"이동 완료: '{source}' → '{destination}'")
            return True
        except Exception as e:
            print(f"이동 실패: {e}")
            return False

    def delete_file(self, file_path: str) -> bool:
        """단일 파일을 삭제한다."""
        if self.check_path(file_path) != PathResult.FILE:
            print(f"파일이 아니거나 존재하지 않음: {file_path}")
            return False
        try:
            os.remove(file_path)
            print(f"삭제 완료: {file_path}")
            return True
        except Exception as e:
            print(f"삭제 실패 ({file_path}): {e}")
            return False

    def delete_files(self, folder_path: str, files: list[str]) -> bool:
        """
        지정한 폴더에서 파일 목록을 삭제한다.

        Parameters
        ----------
        folder_path : 파일이 위치한 폴더 경로
        files       : 삭제할 파일명 리스트
        """
        # folder_path가 파일 경로이면 폴더로 변환
        if self.check_path(folder_path) == PathResult.FILE:
            folder_path = os.path.dirname(folder_path)

        try:
            for file_name in files:
                file_path = os.path.join(folder_path, file_name)
                if self.check_path(file_path) == PathResult.FILE:
                    try:
                        os.remove(file_path)
                        print(f"삭제 완료: {file_name} ({folder_path})")
                    except Exception as e:
                        print(f"삭제 실패 ({file_name}): {e}")
                        return False
                else:
                    print(f"파일 없음 또는 디렉터리: {file_name} ({folder_path})")
            return True
        except Exception as e:
            print(f"delete_files 오류: {e}")
            return False

    def delete_files_in_directory(self, folder_path: str) -> bool:
        """디렉터리 내 모든 파일을 삭제한다."""
        if self.check_path(folder_path) != PathResult.DIR:
            print(f"디렉터리가 아님: {folder_path}")
            return False
        files = os.listdir(folder_path)
        print(f"delete_files_in_directory → {files}")
        return self.delete_files(folder_path, files)

    @staticmethod
    def erase_all_yangsoo_test_files(directory: str) -> None:
        """디렉터리 안의 파일과 하위 폴더를 모두 삭제한다."""
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"삭제 실패 ({file_path}): {e}")

    # ── UI 헬퍼 ──────────────────────────────
    @staticmethod
    def ask_yes_no_question(directory: str = '') -> bool:
        """Yes/No 다이얼로그를 띄우고 사용자 응답을 반환한다."""
        root = tk.Tk()
        root.withdraw()
        try:
            response = messagebox.askyesno('확인', f"진행하겠습니까? {directory}")
            print("사용자 선택: " + ("Yes" if response else "No"))
            return response
        finally:
            root.destroy()

    def select_folder(self, initial_dir: str = '') -> str:
        """tkinter 폴더 선택 다이얼로그를 열고 선택된 경로를 반환한다."""
        root = tk.Tk()
        root.withdraw()

        initial_dir = initial_dir or self.SEND
        folder_path = filedialog.askdirectory(initialdir=initial_dir)

        if folder_path:
            print("선택한 폴더:", folder_path)
        else:
            print("폴더를 선택하지 않았습니다.")

        return folder_path


# ──────────────────────────────────────────────
# 모듈 단독 실행 시 간단한 동작 테스트
# ──────────────────────────────────────────────
if __name__ == '__main__':
    fb = FileBase()
    print('현재 디렉터리:', fb.directory)
    print('xlsm 파일:', fb.get_xlsm_files())
