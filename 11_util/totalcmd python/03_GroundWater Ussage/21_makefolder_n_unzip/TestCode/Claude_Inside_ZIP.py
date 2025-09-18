import zipfile
import tarfile
import rarfile
import py7zr
import os
from pathlib import Path


def get_archive_contents(archive_path):
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
            return _get_zip_contents(archive_path)
        elif extension in ['.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tar.xz']:
            return _get_tar_contents(archive_path)
        elif extension == '.rar':
            return _get_rar_contents(archive_path)
        elif extension == '.7z':
            return _get_7z_contents(archive_path)
        else:
            raise ValueError(f"지원하지 않는 압축 형식입니다: {extension}")

    except Exception as e:
        print(f"압축파일 읽기 오류: {e}")
        return {'files': [], 'folders': []}


def _get_zip_contents(zip_path):
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


def _get_tar_contents(tar_path):
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


def _get_rar_contents(rar_path):
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


def _get_7z_contents(sevenz_path):
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


def print_archive_contents(archive_path):
    """압축파일 내용을 보기 좋게 출력"""
    print(f"\n📁 압축파일: {archive_path}")
    print("=" * 50)

    contents = get_archive_contents(archive_path)

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

    print(f"\n총 {len(contents['folders'])}개 폴더, {len(contents['files'])}개 파일")


# 사용 예제
if __name__ == "__main__":
    # 예제 사용법
    archive_files = [
        "d:\\05_Send\\02_롯데부여리조트 - 전일.rar",
        "d:\\11_exaData\\06_util\99_Game\\01_ToatalCommander Plugin\\00_Program Data\\25_Editor.rar",
        "d:\\05_Send\\02_롯데부여리조트 - 전일.rar"
    ]

    for archive_file in archive_files:
        if os.path.exists(archive_file):
            try:
                print_archive_contents(archive_file)
            except Exception as e:
                print(f"❌ {archive_file}: {e}")
        else:
            print(f"⚠️  파일이 존재하지 않습니다: {archive_file}")

    # 직접 딕셔너리로 결과 받기
    try:
        contents = get_archive_contents("your_archive.zip")
        print(f"폴더: {contents['folders']}")
        print(f"파일: {contents['files']}")
    except FileNotFoundError:
        print("예제 파일을 찾을 수 없습니다.")