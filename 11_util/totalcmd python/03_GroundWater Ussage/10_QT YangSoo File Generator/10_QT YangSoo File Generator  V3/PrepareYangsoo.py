from tkinter import messagebox
from datetime import datetime
import os

from FileManager import FileBase, PathChecker, PathResult


"""
클래스 구조:
    PrepareYangsoofile  – AQT/엑셀 파일을 SEND 폴더에 준비한다.
    PrepareYangsooExcel – GitHub 폴더의 원본 엑셀을 복제한다.
    TransferYangSooFile – SEND(또는 SEND2) 폴더의 파일을 양수시험 디렉터리로 이동한다.
"""


# ──────────────────────────────────────────────
# PrepareYangsoofile
# ──────────────────────────────────────────────
class PrepareYangsoofile(FileBase):
    """
    AQT 파일과 Yangsoo Excel 파일을 SEND 폴더에 준비한다.

    Parameters
    ----------
    directory : 작업 기본 디렉터리 (기본값: SEND)
    """

    def __init__(self, directory: str = r'D:\05_Send' + '\\') -> None:
        resolved = directory if self.check_path(directory) == PathResult.DIR else r'd:\05_Send' + '\\'
        if resolved != directory:
            print(f'[PrepareYangsoofile] 유효하지 않은 경로 → 기본값 사용: {resolved}')
        super().__init__(resolved)

    # ── 초기 엑셀 파일 설정 ───────────────────
    def initial_set_yangsoo_excel(self) -> None:
        """TC_DIR의 최신 xlsm 파일을 SEND 디렉터리에 A1 엑셀로 복사한다."""
        xlsm_list = self.get_xlsmlist_filter(self.TC_DIR)
        if not xlsm_list:
            print('[initial_set_yangsoo_excel] xlsm 파일을 찾을 수 없습니다.')
            return
        filename = xlsm_list[0]
        print('initial_set_yangsoo_excel:', filename)
        self.copy_file(self.TC_DIR + filename, self.SEND + self.YANGSOO_EXCEL)

    # ── AQT 파일 복사 ─────────────────────────
    def aqtfile_to_send(self, well_no: int = 1, aqtstep_include: bool = False) -> None:
        """
        지정한 공번(well_no)의 AQT 파일을 SEND 폴더로 복사한다.

        Parameters
        ----------
        well_no         : 공 번호 (파일명 접두어 w{no} 에 사용)
        aqtstep_include : True이면 step 파일도 함께 복사
        """
        prefix = f'w{well_no}'
        if aqtstep_include:
            self.copy_file(self.TC_DIR + self.STEP_FILE,    self.SEND + prefix + self.STEP_FILE)
        self.copy_file(self.TC_DIR + self.LONG_FILE,    self.SEND + prefix + self.LONG_FILE)
        self.copy_file(self.TC_DIR + self.RECOVER_FILE, self.SEND + prefix + self.RECOVER_FILE)

    # ── 엑셀 복제 ─────────────────────────────
    def duplicate_yangsoo_excel(self, cnt: int) -> None:
        """
        A1 엑셀 파일을 기준으로 A2~A{cnt} 까지 복제한다.

        Parameters
        ----------
        cnt : 총 공 개수
        """
        self.delete_files_in_directory(self.SEND)
        self.initial_set_yangsoo_excel()

        source = self.SEND + self.YANGSOO_EXCEL
        for i in range(2, cnt + 1):
            destination = self.join_path_tofilename(self.SEND, f'A{i}{self.YANGSOO_REST}')
            self.copy_file(source, destination)


# ──────────────────────────────────────────────
# PrepareYangsooExcel  (2025-09-28 추가)
# ──────────────────────────────────────────────
class PrepareYangsooExcel(FileBase):
    """
    GitHub 폴더의 원본 Yangsoo Excel 을 SEND 폴더에 복제한다.

    Notes
    -----
    원본 파일은 YANGSOO_GITHUB 에서 'A1*집수정*.xlsm' 패턴으로 탐색한다.
    """

    _DEFAULT_SEND = 'd:/05_Send/'

    def __init__(self, directory: str = r'D:\05_Send' + '\\') -> None:
        super().__init__(directory)

    # ── 내부 헬퍼 ────────────────────────────
    def _find_source_file(self) -> str | None:
        """GitHub 폴더에서 원본 파일 경로를 탐색한다."""
        matches = self.get_file_filter(self.YANGSOO_GITHUB, 'A1*집수정*.xlsm')
        if not matches:
            print('[PrepareYangsooExcel] 원본 파일을 찾을 수 없습니다.')
            return None
        return os.path.join(self.YANGSOO_GITHUB, matches[-1])

    def _ensure_directory(self, path: str) -> None:
        """경로가 없으면 생성한다."""
        if not os.path.exists(path):
            os.makedirs(path)
            print(f'폴더 생성됨: {path}')

    def _duplicate_to(self, source: str, dest_folder: str, label: str) -> str:
        """
        source 파일을 dest_folder 에 A{label}_ge_OriginalSaveFile.xlsm 으로 복사한다.

        Returns
        -------
        복사된 파일의 전체 경로
        """
        filename = f'A{label}_ge_OriginalSaveFile.xlsm'
        dest_path = os.path.join(dest_folder, filename).replace('\\', '/')
        self.copy_file(source, dest_path)
        return dest_path

    # ── 공개 메서드 ───────────────────────────
    def copy_and_get_yangsoo_file(self, nof_well: int) -> None:
        """
        원본 파일을 A1로 복사한 뒤 A2~A{nof_well} 까지 복제한다.

        Parameters
        ----------
        nof_well : 총 공 개수
        """
        source = self._find_source_file()
        if source is None:
            return

        dest_folder  = self._DEFAULT_SEND
        original_a1  = os.path.join(dest_folder, 'A1_ge_OriginalSaveFile.xlsm')

        self._ensure_directory(dest_folder)
        self.copy_file(source, original_a1)

        for i in range(2, nof_well + 1):
            new_path = self._duplicate_to(original_a1, dest_folder, i)
            print(f'복제 완료: {new_path}')

    def copy_and_get_yangsoo_file2(self, gong_list: list) -> bool:
        """
        공 리스트(gong_list)를 순회하며 각 공의 엑셀 파일을 복제한다.

        Parameters
        ----------
        gong_list : 공 식별자 리스트 (예: ['A', 'B', 3])

        Returns
        -------
        모든 복제 성공 시 True, 하나라도 실패하면 False
        """
        dest_folder = self._DEFAULT_SEND

        try:
            source = self._find_source_file()
            if source is None:
                return False

            self._ensure_directory(dest_folder)

            for gong in gong_list:
                dest_path = os.path.join(dest_folder, f'A{gong}_ge_OriginalSaveFile.xlsm')
                if not self.copy_file(source, dest_path):
                    print(f'파일 생성 실패 (공 {gong})')
                    return False
                print(f'파일 생성 성공: {dest_path}')

            return True

        except PermissionError:
            messagebox.showerror('에러', '파일이 열려 있거나 접근 권한이 없습니다.')
            return False
        except FileNotFoundError:
            messagebox.showerror('에러', '지정된 경로를 찾을 수 없습니다.')
            return False
        except Exception as e:
            messagebox.showerror('에러', f'예기치 못한 오류: {e}')
            return False


# ──────────────────────────────────────────────
# TransferYangSooFile
# ──────────────────────────────────────────────
class TransferYangSooFile(FileBase):
    """
    SEND / SEND2 / DOCUMENTS 폴더의 파일을 양수시험 디렉터리 구조로 이동한다.

    디렉터리 구조
    -------------
    BASEDIR/
        04_양수시험/
            01_Prn Save File/
            02_AQTEver3.4(170414)/
            03_양수일보/
    """

    _YANGSOO_BASE    = '\\04_양수시험'
    _PRN_BASE        = '\\01_Prn Save File\\'
    _AQT_BASE        = '\\02_AQTEver3.4(170414)\\'
    _YANGSOOILBO_BASE = '\\03_양수일보\\'

    def __init__(self, directory: str = '') -> None:
        super().__init__()
        self.BASEDIR         = directory
        self.DIR_YANGSOO_TEST = ''
        self.DIR_PRN          = ''
        self.DIR_AQT          = ''
        self.DIR_YANGSOOILBO  = ''
        self.isDIRSET         = False

    # ── 폴더 유효성 검사 ──────────────────────
    def isit_yangsoo_folder(self, folder_name: str) -> str:
        """
        선택된 폴더가 양수시험 대상 폴더인지 판별한다.

        Returns
        -------
        유효한 경로 문자열  : 양수시험 폴더
        'MORE'             : 하위 폴더 선택 필요
        'FALSE'            : 양수시험 폴더가 아님
        """
        current_year = datetime.now().year
        dirlist = self.unfold_path(folder_name)

        if len(dirlist) < 4 or '개소' in dirlist[3]:
            return 'MORE'

        if dirlist[1] == '09_hardRain' and dirlist[2].endswith(str(current_year)):
            return self.join_path_forward(dirlist, 4)

        return 'FALSE'

    def isit_yangsoo_inside(self, folder_name: str) -> bool:
        """해당 폴더 안에 '04_양수시험' 폴더가 있으면 True."""
        return '04_양수시험' in self.list_directories_only(folder_name)

    # ── 하위 디렉터리 lazy 생성 ───────────────
    def _ensure_subdir(self, attr: str, parts: list[str]) -> str:
        """
        self.{attr}이 비어 있으면 parts를 결합해 경로를 만들고,
        존재하지 않으면 디렉터리를 생성한 뒤 반환한다.
        """
        if not getattr(self, attr):
            path = self.join_path_from_list(parts)
            if self.check_path(path) != PathResult.DIR:
                os.mkdir(path)
            setattr(self, attr, path)
        return getattr(self, attr)

    def dir_yangsoo_test(self) -> str:
        return self._ensure_subdir(
            'DIR_YANGSOO_TEST',
            [self.BASEDIR, self._YANGSOO_BASE]
        )

    def dir_prn(self) -> str:
        return self._ensure_subdir(
            'DIR_PRN',
            [self.BASEDIR, self._YANGSOO_BASE, self._PRN_BASE]
        )

    def dir_aqt(self) -> str:
        return self._ensure_subdir(
            'DIR_AQT',
            [self.BASEDIR, self._YANGSOO_BASE, self._AQT_BASE]
        )

    def dir_yangsoo_ilbo(self) -> str:
        return self._ensure_subdir(
            'DIR_YANGSOOILBO',
            [self.BASEDIR, self._YANGSOO_BASE, self._YANGSOOILBO_BASE]
        )

    # ── 내부 디렉터리 세팅 ───────────────────
    def setdir_inside_yangsootest(self) -> None:
        """
        04_양수시험 안에서 01/02/03 으로 시작하는 폴더를 탐색해
        DIR_PRN / DIR_AQT / DIR_YANGSOOILBO 를 설정한다.
        폴더가 없으면 새로 만든다.
        """
        yangsoo_test = self.dir_yangsoo_test()
        os.chdir(yangsoo_test)

        if self.check_path(yangsoo_test) != PathResult.DIR:
            os.makedirs(yangsoo_test)
            self._create_default_subdirs()
            return

        inside = self.list_directories_only(yangsoo_test)
        if not inside:
            self._create_default_subdirs()
            return

        print(inside)
        arg_01 = next((d for d in inside if d.startswith('01')), '')
        arg_02 = next((d for d in inside if d.startswith('02')), '')
        arg_03 = next((d for d in inside if d.startswith('03')), '')

        if arg_01 and arg_02 and arg_03:
            self.DIR_PRN         = self.join_path_from_list([yangsoo_test, '\\', arg_01])
            self.DIR_AQT         = self.join_path_from_list([yangsoo_test, '\\', arg_02])
            self.DIR_YANGSOOILBO = self.join_path_from_list([yangsoo_test, '\\', arg_03])
        else:
            self._create_default_subdirs()

    def _create_default_subdirs(self) -> None:
        """기본 하위 디렉터리 3개를 생성한다."""
        self.print_debug(self.dir_prn())
        self.print_debug(self.dir_aqt())
        self.print_debug(self.dir_yangsoo_ilbo())

    # ── BASEDIR 세팅 ──────────────────────────
    def setBASEDIR(self, directory: str = '') -> str:
        """
        이동 대상 기준 디렉터리(BASEDIR)를 설정한다.

        유효한 경로가 주어지면 그대로 사용하고,
        그렇지 않으면 tkinter 폴더 선택창을 연다.

        Returns
        -------
        설정된 경로 또는 'FALSE'
        """
        print('*' * 55)
        print(directory)
        print('*' * 55)

        current_year = datetime.now().year

        if directory and self.check_path(directory) == PathResult.DIR:
            self.BASEDIR = directory
        else:
            sel_folder   = self.select_folder(f'd:\\09_hardRain\\09_ihanseol - {current_year}\\')
            self.BASEDIR = self.isit_yangsoo_folder(sel_folder)

        if self.BASEDIR in ('FALSE', 'MORE'):
            msg = "양수시험 폴더가 아닙니다." if self.BASEDIR == 'FALSE' \
                  else "더 하위 폴더를 선택해야 합니다."
            self.print_debug(msg)
            self.isDIRSET = False
            return 'FALSE'

        self.setdir_inside_yangsootest()
        self.isDIRSET = True
        return self.BASEDIR

    # ── 파일 이동 ─────────────────────────────
    def move_origin_to_ihanseol(self, folder_path: str) -> None:
        """
        folder_path(SEND / SEND2 / DOCUMENTS) 의 파일을
        양수시험 하위 디렉터리로 분류·이동한다.

        파일 분류 기준
        --------------
        aqt  : w 로 시작         → DIR_AQT
        pdf  : a, w, p 로 시작   → DIR_AQT / DIR_YANGSOOILBO
        jpg  : 패턴별             → DIR_AQT / DIR_YANGSOOILBO
        xlsx/xlsm                → DIR_YANGSOO_TEST
        prn                      → DIR_PRN
        """
        fb = FileBase()
        fb.set_directory(folder_path)

        raw = {
            'aqt':   fb.get_aqt_files(),
            'pdf':   fb.get_pdf_files(),
            'xlsx':  fb.get_xlsx_files(),
            'xlsm':  fb.get_xlsm_files(),
            'prn':   fb.get_prn_files(),
            'jpg_a': fb.get_jpg_filter(sfilter='a*page*'),
            'jpg_p': fb.get_jpg_filter(sfilter='p*page*'),
            'jpg_w': fb.get_jpg_filter(sfilter='w*page*'),
        }

        filtered = {
            'w_aqt': [f for f in raw['aqt'] if f.startswith('w')],
            'a_pdf': [f for f in raw['pdf'] if f.startswith('a')],
            'w_pdf': [f for f in raw['pdf'] if f.startswith('w')],
            'p_pdf': [f for f in raw['pdf'] if f.startswith('p')],
            'jpg_a': raw['jpg_a'],
            'jpg_p': raw['jpg_p'],
            'jpg_w': raw['jpg_w'],
            'xlsx':  raw['xlsx'],
            'xlsm':  raw['xlsm'],
            'prn':   raw['prn'],
        }

        self.print_debug('-' * 40)
        for key, files in filtered.items():
            print(f'{key}: {files}')
        self.print_debug('-' * 40)

        if filtered['prn']:
            self._move_files_to_dir(folder_path, filtered, ['prn'], self.DIR_PRN, 'Prn Files')

        if filtered['xlsx'] or filtered['xlsm']:
            self._move_files_to_dir(folder_path, filtered, ['xlsx', 'xlsm'], self.DIR_YANGSOO_TEST, 'YangSoo Test')

        if any(filtered[k] for k in ('a_pdf', 'p_pdf', 'jpg_a', 'jpg_p', 'w_aqt')):
            self._move_files_to_dir(
                folder_path, filtered,
                ['a_pdf', 'p_pdf', 'jpg_a', 'jpg_p', 'w_aqt'],
                self.DIR_AQT, '02_AQTEver3.4(170414)'
            )

        if filtered['jpg_w'] or filtered['w_pdf']:
            self._move_files_to_dir(
                folder_path, filtered,
                ['jpg_w', 'w_pdf'],
                self.DIR_YANGSOOILBO, 'yangsoo ilbo'
            )

    def _move_files_to_dir(
        self,
        source_path: str,
        filtered_files: dict,
        keys: list[str],
        target_directory: str,
        debug_message: str,
    ) -> None:
        """filtered_files[key] 에 해당하는 파일들을 target_directory 로 이동한다."""
        print(f'→ {debug_message}')
        for key in keys:
            for filename in filtered_files[key]:
                source = self.join_path_tofilename(source_path, filename)
                target = self.join_path_tofilename(target_directory, filename)
                self.move_file(source, target)

    # ── 테스트용 ──────────────────────────────
    def Test(self) -> None:
        fb = FileBase()
        fb.set_directory(self.DOCUMENTS)
        print(fb.get_list_files(['.dat', '.xlsm']))


# ──────────────────────────────────────────────
if __name__ == '__main__':
    py = PrepareYangsoofile()
    py.initial_set_yangsoo_excel()
