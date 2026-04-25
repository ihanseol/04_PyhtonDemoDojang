import fnmatch
import os
import time

import pandas as pd
from natsort import natsorted

from AqtProjectInfoInjector import AqtProjectInfoInjector


# 기본 Excel 스펙 파일 경로 상수
_YANGSOO_SPEC_PATH = r'd:\05_Send\YanSoo_Spec.xlsx'


class AqtExcelProjectInfoInjector(AqtProjectInfoInjector):
    """
    YanSoo_Spec.xlsx 에서 공번·주소·회사명을 읽어
    SEND 폴더의 AQT 파일에 프로젝트 정보를 일괄 입력한다.

    Parameters
    ----------
    directory : 작업 디렉터리 경로
    company   : 프로젝트 회사명 (Excel 로드 후 덮어쓰임)
    """

    def __init__(self, directory: str, company: str) -> None:
        super().__init__(directory, company)
        self.df           = pd.DataFrame()
        self.project_name = ''
        self.is_jiyeol    = False   # 지열공이면 단계파일 포함 필요

    # ── DataFrame 관리 ────────────────────────
    def set_dataframe(self, df: pd.DataFrame) -> None:
        """DataFrame 을 설정하고 프로젝트명·지열 여부를 파악한다."""
        self.df           = df
        self.project_name = str(self.df.loc[0, 'Project Name'])
        self.is_jiyeol    = '지열' in self.project_name

    def _load_spec_if_needed(self, force: bool = False) -> bool:
        """
        YanSoo_Spec.xlsx 를 로드한다.

        Parameters
        ----------
        force : True 이면 df 가 비어 있지 않아도 다시 로드한다.

        Returns
        -------
        로드 성공 여부
        """
        if not force and not self.df.empty:
            return True

        if not self.is_exist(_YANGSOO_SPEC_PATH):
            print(f'[_load_spec_if_needed] 파일 없음: {_YANGSOO_SPEC_PATH}')
            return False

        df = pd.read_excel(_YANGSOO_SPEC_PATH)
        self.set_dataframe(df)
        return True

    def _load_spec_sheet(
        self,
        file_path: str = _YANGSOO_SPEC_PATH,
        sheet_name: str = 'Data',
    ) -> pd.DataFrame:
        """
        Excel 파일의 특정 시트를 DataFrame 으로 반환한다.
        이미 self.df 에 'gong' 컬럼이 있으면 재로드 없이 캐시를 반환한다.
        실패 시 빈 DataFrame 을 반환한다.
        """
        # 이미 로드된 df 에 gong 컬럼이 있으면 재사용 (루프 중 반복 로드 방지)
        if not self.df.empty and 'gong' in self.df.columns:
            return self.df

        try:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        except FileNotFoundError:
            print(f'[_load_spec_sheet] 파일 없음: {file_path}')
        except Exception as e:
            print(f'[_load_spec_sheet] 로드 오류: {e}')
        return pd.DataFrame()

    # ── 공번·주소 조회 ────────────────────────
    def get_gong_n_address(self, row_index: int) -> tuple[str | None, str]:
        """
        row_index 번째 행의 공번(gong)과 주소(address)를 반환한다.
        (1-based 인덱스)

        Returns
        -------
        (공번 문자열, 주소 문자열) / 실패 시 (None, 'None')
        """
        self._load_spec_if_needed()

        try:
            row      = self.df.loc[row_index - 1]
            str_gong = row['gong']
            address  = row['address']
            time.sleep(1)
        except Exception as e:
            print(f'[get_gong_n_address] 오류 (row={row_index}): {e}')
            return None, 'None'

        print(f'gong={str_gong}, address={address}')
        return str_gong, address

    def get_gong_n_address2(
        self,
        well_no: int,
        file_path: str = _YANGSOO_SPEC_PATH,
    ) -> pd.DataFrame:
        """
        Excel 'Data' 시트에서 공번 'W-{well_no}' 에 해당하는 행을 반환한다.

        Returns
        -------
        일치하는 행의 DataFrame / 실패 시 빈 DataFrame
        """
        df = self._load_spec_sheet(file_path)
        if df.empty:
            return df

        if 'gong' not in df.columns:
            print("[get_gong_n_address2] 'gong' 컬럼이 없습니다.")
            return pd.DataFrame()

        result = df[df['gong'] == f'W-{well_no}']
        if result.empty:
            print(f'[get_gong_n_address2] W-{well_no} 데이터 없음.')
        return result

    def get_last_gong(self) -> int | None:
        """Excel 마지막 행의 공번을 정수로 반환한다."""
        self._load_spec_if_needed()
        try:
            str_gong = self.df.iloc[-1, 0]
            return self.extract_number(str_gong)
        except Exception as e:
            print(f'[get_last_gong] 오류: {e}')
            return None

    def get_gong_list(self) -> list[int]:
        """
        Excel 'gong' 컬럼의 공번을 정수 리스트로 반환한다.

        Returns
        -------
        [1, 2, 3, ...] 형태의 공번 리스트
        """
        self._load_spec_if_needed()

        cleaned = pd.Series(self.df['gong'].tolist()).dropna().tolist()
        g_list  = [self.extract_number(item) for item in cleaned]
        print(f'g_list: {g_list}')
        return g_list

    # ── 파일 정리 ─────────────────────────────
    def delete_difference(self, file_list: list[int]) -> None:
        """
        SEND 폴더에서 Excel 목록에 없는 공번의 AQT 파일을 삭제한다.

        Parameters
        ----------
        file_list : 삭제할 공번 정수 리스트 (예: [3, 4, 5])
        """
        aqtfiles = natsorted(self.get_aqt_files())
        for well_no in file_list:
            targets = fnmatch.filter(aqtfiles, f'w{well_no}_*.aqt')
            for filename in targets:
                try:
                    os.remove(filename)
                    print(f'[delete_difference] 삭제: {filename}')
                except Exception as e:
                    print(f'[delete_difference] 삭제 실패 ({filename}): {e}')

    # ── 공통 준비 로직 ────────────────────────
    def _prepare_common(self, force_reload: bool = True) -> tuple[list[int], list[str]]:
        """
        Excel 로드 → 회사·주소 설정 → 파일명 정리 → 공번 차집합 삭제까지
        process_projectinfo_* 메서드에 공통으로 필요한 준비 과정을 수행한다.

        Returns
        -------
        (xlsx_gong_list, aqt_file_list)
        """
        self._load_spec_if_needed(force=force_reload)

        company = str(self.df.loc[0, 'Company'])
        address = str(self.df.loc[0, 'address'])
        self.set_company(company)
        self.set_address(address)
        self.change_aqt_filename()

        send_list  = self.get_wellno_list_insend()
        gong_list  = self.get_gong_list()
        difference = list(set(send_list) - set(gong_list))
        if difference:
            self.delete_difference(difference)

        aqtfiles = self.get_aqt_files()
        print(f'aqtfiles: {aqtfiles}')
        return gong_list, aqtfiles

    # ── 메인 처리 메서드 ──────────────────────
    def process_projectinfo_byexcel(self, addOne: bool = False) -> None:
        """
        Excel 의 공번 순서대로 AQT 파일에 프로젝트 정보를 입력한다.

        Parameters
        ----------
        addOne : True 이면 모든 공에 1번 행의 정보를 사용한다.
                 (공번이 Excel 에 없는 추가 공 처리용)
        """
        gong_list, aqtfiles = self._prepare_common()

        try:
            for i in gong_list:
                row_idx           = 1 if addOne else i
                gong, raw_address = self.get_gong_n_address(row_idx)

                if gong is None:
                    self.close_aqt()
                    return

                processed = self.process_address(raw_address)
                print(f'gong={gong}, address="{processed}"')

                wfiles = fnmatch.filter(aqtfiles, f'w{i}_*.aqt')
                print(f'wfiles: {wfiles}')

                if wfiles:
                    self.aqt_mainaction(self.extract_number(gong), processed, wfiles)

        finally:
            self.unblock_user_input()
            if self.DEBUG:
                print('[process_projectinfo_byexcel] 완료.')

    def process_projectinfo_byexcel2(self, addOne: bool = False) -> None:
        """
        get_gong_n_address2 (Data 시트 직접 조회) 를 사용해
        AQT 파일에 프로젝트 정보를 입력한다.

        addOne 파라미터는 향후 확장을 위해 시그니처 유지.
        """
        gong_list, aqtfiles = self._prepare_common()

        try:
            for i in gong_list:
                print('=' * 80)
                print(f'공 {i} 처리 시작 ...')
                print('=' * 80)

                result_df = self.get_gong_n_address2(i)
                if result_df.empty:
                    print(f'[process_projectinfo_byexcel2] 공 {i} 데이터 없음 → 건너뜀')
                    continue

                gong        = str(result_df['gong'].iloc[0])
                raw_address = str(result_df['address'].iloc[0])
                print(f'gong={gong}, address="{raw_address}"')

                processed = self.process_address(raw_address)
                print(f'처리된 주소: "{processed}"')

                wfiles = fnmatch.filter(aqtfiles, f'w{i}_*.aqt')
                print(f'wfiles: {wfiles}')

                if wfiles:
                    self.aqt_mainaction(i, processed, wfiles)

        finally:
            self.unblock_user_input()
            if self.DEBUG:
                print('[process_projectinfo_byexcel2] 완료.')

    def process_projectinfo_likesejong(self, company: str) -> None:
        """
        세종시처럼 공마다 주소가 다른 경우를 처리한다.
        회사명은 인자로 받고, 주소는 Excel 에서 공마다 읽어온다.

        Parameters
        ----------
        company : 고정 회사명
        """
        self._load_spec_if_needed()
        self.set_company(company)
        self.change_aqt_filename()

        send_list  = self.get_wellno_list_insend()
        gong_list  = self.get_gong_list()
        difference = list(set(send_list) - set(gong_list))
        if difference:
            self.delete_difference(difference)

        aqtfiles = self.get_aqt_files()
        if not aqtfiles:
            print('[process_projectinfo_likesejong] AQT 파일 없음.')
            return

        print(f'aqtfiles: {aqtfiles}')

        try:
            for i in gong_list:
                gong, raw_address = self.get_gong_n_address(i)

                if gong is None:
                    self.close_aqt()
                    return

                processed = self.process_address(raw_address)
                self.set_address(processed)
                print(f'gong={gong}, address="{processed}"')

                wfiles = fnmatch.filter(aqtfiles, f'w{i}_*.aqt')
                print(f'wfiles: {wfiles}')

                if wfiles:
                    self.aqt_mainaction(self.extract_number(gong), processed, wfiles)

        finally:
            self.unblock_user_input()
            if self.DEBUG:
                print('[process_projectinfo_likesejong] 완료.')


# ──────────────────────────────────────────────
if __name__ == '__main__':
    injector = AqtExcelProjectInfoInjector(r'd:\05_Send', '')
    injector.process_projectinfo_byexcel()
