# import os
# import zipfile

# zip_folder = r"d:\05_Send"
# extract_base_folder = r"d:\06_Send3"

# # d:\05_Send\ 에 있는 모든 zip 파일 리스트 가져오기
# for file_name in os.listdir(zip_folder):
#     if file_name.lower().endswith('.zip'):
#         zip_path = os.path.join(zip_folder, file_name)
#         folder_name = os.path.splitext(file_name)[0]
#         extract_folder = os.path.join(extract_base_folder, folder_name)

#         if not os.path.exists(extract_folder):
#             os.makedirs(extract_folder)
        
#         with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#             zip_ref.extractall(extract_folder)
        
#         print(f"압축해제 완료: {zip_path} -> {extract_folder}")

import os
import zipfile
import rarfile
import py7zr # py7zr 라이브러리 추가

zip_folder = r"d:\05_Send"
extract_base_folder = r"d:\06_Send3"

for file_name in os.listdir(zip_folder):
    file_path = os.path.join(zip_folder, file_name)
    
    # Check if the file is a .zip file
    if file_name.lower().endswith('.zip'):
        folder_name = os.path.splitext(file_name)[0]
        extract_folder = os.path.join(extract_base_folder, folder_name)

        if not os.path.exists(extract_folder):
            os.makedirs(extract_folder)
        
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
        
        print(f"압축해제 완료: {file_path} -> {extract_folder}")

    # Check if the file is a .rar file
    elif file_name.lower().endswith('.rar'):
        folder_name = os.path.splitext(file_name)[0]
        extract_folder = os.path.join(extract_base_folder, folder_name)

        if not os.path.exists(extract_folder):
            os.makedirs(extract_folder)
        
        try:
            with rarfile.RarFile(file_path, 'r') as rar_ref:
                rar_ref.extractall(extract_folder)
            print(f"압축해제 완료: {file_path} -> {extract_folder}")
        except rarfile.RarError as e:
            print(f"오류 발생: {file_path} 압축 해제 실패 - {e}")

    # Check if the file is a .7z file
    elif file_name.lower().endswith('.7z'):
        folder_name = os.path.splitext(file_name)[0]
        extract_folder = os.path.join(extract_base_folder, folder_name)

        if not os.path.exists(extract_folder):
            os.makedirs(extract_folder)

        try:
            with py7zr.SevenZipFile(file_path, mode='r') as sz_ref:
                sz_ref.extractall(path=extract_folder)
            print(f"압축해제 완료: {file_path} -> {extract_folder}")
        except py7zr.Bad7zFile as e:
            print(f"오류 발생: {file_path} 압축 해제 실패 - {e}")