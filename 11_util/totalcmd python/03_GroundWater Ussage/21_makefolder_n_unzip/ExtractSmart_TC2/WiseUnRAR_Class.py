import os
import sys
import re
import subprocess
import tkinter as tk
from tkinter import messagebox
import shutil
import zipfile
import tarfile
import rarfile
import py7zr
from pathlib import Path


class ExtractSmart:
    """
    압축 파일 추출 및 분석을 위한 통합 클래스
    """

    def __init__(self, send_path="d:\\05_Send\\", winrar_path=r"C:\Program Files\WinRAR\WinRar.exe"):
        """
        ExtractSmart 초기화

        Args:
            send_path (str): 임시 파일이 저장될 경로
            winrar_path (str): WinRAR 실행 파일 경로
        """
        self.SEND_PATH = send_path
        self.winrar_path = winrar_path

    def print_debug(self, msg='', chr='*', length=180):
        """디버그 메시지 출력"""
        print(chr * length)
        print(msg)
        print(chr * length)

    def show_message_box(self, message):
        """메시지 박스 표시"""
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Notice", message)

    def copy_file(self, source_file, target_file):
        """
        파일 복사

        Args:
            source_file (str): 원본 파일 경로
            target_file (str): 대상 파일 경로

        Returns:
            bool: 복사 성공 여부
        """
        try:
            shutil.copy(source_file, target_file)
            print(f"File copied successfully from {source_file} to {target_file}")
            return True
        except FileNotFoundError:
            print(f"Source file not found: {source_file}")
            return False
        except PermissionError:
            print(f"Permission denied. Could not copy to {target_file}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def get_archive_contents(self, archive_path):
        """
        압축파일의 최상위 경로에 있는 파일/폴더 리스트를 반환

        Args:
            archive_path (str): 압축파일 경로

        Returns:
            dict: {'files': [], 'folders': []} 형태의 딕셔너리
        """
        archive_path = Path(archive_path)

        if not archive_path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {archive_path}")

        extension = archive_path.suffix.lower()

        try:
            if extension == '.zip':
                return self._get_zip_contents(archive_path)
            elif extension in ['.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tar.xz']:
                return self._get_tar_contents(archive_path)
            elif extension == '.rar':
                return self._get_rar_contents(archive_path)
            elif extension == '.7z':
                return self._get_7z_contents(archive_path)
            else:
                raise ValueError(f"지원하지 않는 압축 형식입니다: {extension}")

        except Exception as e:
            print(f"압축파일 읽기 오류: {e}")
            return {'files': [], 'folders': []}

    def _get_zip_contents(self, zip_path):
        """ZIP 파일 내용 조회"""
        files = []
        folders = set()

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_info in zip_ref.filelist:
                path_parts = file_info.filename.split('/')

                if len(path_parts) == 1 and not file_info.filename.endswith('/'):
                    # 최상위 파일
                    files.append(file_info.filename)
                elif len(path_parts) >= 1:
                    # 최상위 폴더
                    top_folder = path_parts[0]
                    if top_folder and top_folder not in files:
                        folders.add(top_folder)

        return {'files': files, 'folders': sorted(list(folders))}

    def _get_tar_contents(self, tar_path):
        """TAR 파일 내용 조회"""
        files = []
        folders = set()

        with tarfile.open(tar_path, 'r') as tar_ref:
            for member in tar_ref.getmembers():
                path_parts = member.name.split('/')

                if len(path_parts) == 1 and member.isfile():
                    # 최상위 파일
                    files.append(member.name)
                elif len(path_parts) >= 1:
                    # 최상위 폴더
                    top_folder = path_parts[0]
                    if top_folder and top_folder not in files:
                        folders.add(top_folder)

        return {'files': files, 'folders': sorted(list(folders))}

    def _get_rar_contents(self, rar_path):
        """RAR 파일 내용 조회 (rarfile 라이브러리 필요)"""
        files = []
        folders = set()

        with rarfile.RarFile(rar_path, 'r') as rar_ref:
            for file_info in rar_ref.infolist():
                path_parts = file_info.filename.split('/')

                if len(path_parts) == 1 and not file_info.is_dir():
                    # 최상위 파일
                    files.append(file_info.filename)
                elif len(path_parts) >= 1:
                    # 최상위 폴더
                    top_folder = path_parts[0]
                    if top_folder and top_folder not in files:
                        folders.add(top_folder)

        return {'files': files, 'folders': sorted(list(folders))}

    def _get_7z_contents(self, sevenz_path):
        """7Z 파일 내용 조회 (py7zr 라이브러리 필요)"""
        files = []
        folders = set()

        with py7zr.SevenZipFile(sevenz_path, 'r') as sevenz_ref:
            for file_info in sevenz_ref.list():
                path_parts = file_info.filename.split('/')

                if len(path_parts) == 1 and not file_info.is_directory:
                    # 최상위 파일
                    files.append(file_info.filename)
                elif len(path_parts) >= 1:
                    # 최상위 폴더
                    top_folder = path_parts[0]
                    if top_folder and top_folder not in files:
                        folders.add(top_folder)

        return {'files': files, 'folders': sorted(list(folders))}

    def print_archive_contents(self, archive_path):
        """
        압축파일 내용을 보기 좋게 출력하고 총 파일/폴더 수를 반환

        Args:
            archive_path (str): 압축파일 경로

        Returns:
            int: 총 파일과 폴더 개수
        """
        print(f"\n📁 압축파일: {archive_path}")
        print("=" * 50)

        contents = self.get_archive_contents(archive_path)

        if contents['folders']:
            print("📂 폴더:")
            for folder in contents['folders']:
                print(f"  └── {folder}/")

        if contents['files']:
            print("📄 파일:")
            for file in contents['files']:
                print(f"  └── {file}")

        if not contents['folders'] and not contents['files']:
            print("빈 압축파일이거나 읽을 수 없습니다.")

        total_count = len(contents['folders']) + len(contents['files'])
        print(f"\n총 {len(contents['folders'])}개 폴더, {len(contents['files'])}개 파일")

        if total_count == 1:
            if len(contents['folders']) == 0:
                total_count = 99
                return total_count

        return total_count

    def extract_archive(self, archive_path, target_dir):
        """
        압축 파일을 대상 디렉터리로 추출

        Args:
            archive_path (str): 압축파일 경로
            target_dir (str): 추출할 대상 디렉터리

        Returns:
            bool: 추출 성공 여부
        """
        try:
            # 압축파일 내용 분석
            num_files = self.print_archive_contents(archive_path)
            is_single_folder = (num_files == 1)

            # WinRAR 추출 명령어 구성
            if is_single_folder:
                extract_command = [self.winrar_path, 'x', "-Y", archive_path, target_dir]
            else:
                extract_command = [self.winrar_path, 'x', '-ad', "-Y", archive_path, target_dir]

            # 추출 실행
            subprocess.run(extract_command, check=True)
            print("압축 해제가 완료되었습니다.")
            return True

        except subprocess.CalledProcessError as e:
            print(f"압축 해제 중 오류 발생: {e}")
            return False
        except Exception as e:
            print(f"예기치 않은 오류 발생: {e}")
            return False

    def process_archive_list(self, list_file_path, target_dir):
        """
        파일 목록에서 압축 파일들을 순차적으로 처리

        Args:
            list_file_path (str): 압축파일 목록이 있는 텍스트 파일 경로
            target_dir (str): 추출할 대상 디렉터리
        """
        os.chdir(target_dir)
        print(f"작업 디렉터리: {os.getcwd()}")

        try:
            with open(list_file_path, 'r', encoding='cp949') as file:
                for line in file:
                    clean_path = line.replace("\n", "").replace("\\", "\\\\")
                    print(f"처리 중: {clean_path}")

                    self.extract_archive(clean_path, target_dir)

        except Exception as e:
            print(f"파일 목록 처리 중 오류 발생, {list_file_path}: {e}")
            self.show_message_box(f"파일을 찾을 수 없습니다: {list_file_path}")

    def run_main_process(self):
        """
        메인 실행 프로세스 (기존 main() 함수 기능)
        """
        print(f"인수 개수: {len(sys.argv)}")
        print(f"스크립트 이름: {sys.argv[0]}")

        for i, arg in enumerate(sys.argv[1:], start=1):
            print(f"인수 {i}: {arg}")

        if len(sys.argv) < 3:
            print("사용법: python script.py <source_file> <target_dir>")
            return

        local_appdata = os.getenv('LOCALAPPDATA')
        source_file = local_appdata + "\\Temp\\" + os.path.basename(sys.argv[1])
        target_dir = sys.argv[2]

        # 파일 복사
        self.copy_file(source_file, self.SEND_PATH + "dir_list.txt")
        source_file = self.SEND_PATH + "dir_list.txt"

        print(f"1. 원본: {source_file}")
        print(f"2. 대상: {target_dir}")

        # 압축파일 목록 처리
        self.process_archive_list(source_file, target_dir)

        # 임시 파일 삭제
        try:
            os.remove(source_file)
            print(f"임시 파일 삭제됨: {source_file}")
        except Exception as e:
            print(f"임시 파일 삭제 실패: {e}")


# 사용 예제 및 메인 실행부
if __name__ == "__main__":
    # ExtractSmart 인스턴스 생성
    extractor = ExtractSmart()

    # 명령행 인수가 있는 경우 메인 프로세스 실행
    if len(sys.argv) > 1:
        extractor.run_main_process()
    else:
        # 테스트 실행 예제
        print("ExtractSmart 테스트 모드")

        # 예제 압축파일들
        test_archives = [
            "d:\\05_Send\\02_롯데부여리조트 - 전일.rar",
            "d:\\11_exaData\\06_util\\99_Game\\01_ToatalCommander Plugin\\00_Program Data\\25_Editor.rar"
        ]

        for archive_file in test_archives:
            if os.path.exists(archive_file):
                try:
                    extractor.print_archive_contents(archive_file)
                except Exception as e:
                    print(f"❌ {archive_file}: {e}")
            else:
                print(f"⚠️ 파일이 존재하지 않습니다: {archive_file}")

        print("\n클래스 기반 ExtractSmart가 준비되었습니다.")
        print("사용법:")
        print("1. 명령행에서: python ExtractSmart_TC2_Unified.py <source_file> <target_dir>")
        print("2. 코드에서: extractor = ExtractSmart(); extractor.extract_archive(archive_path, target_dir)")
