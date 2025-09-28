import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime

import fnmatch
import time
import os
import pyperclip
import re
from natsort import natsorted
import pyautogui
import ctypes
import pandas as pd

from .FileManager import FileBase
from .FileManager import PathChecker

"""
    class PrepareYangsoofile(FileBase):
    
    class TransferYangSooFile(FileBase):
    
    2025-9-28, Add Github folder path
    class PrepareYangsooExcel(FileBase):
    처음 양수파일을 준비하는 과정
    가져올 폴더는 깃허브 엑셀 양수폴더
"""


class PrepareYangsoofile(FileBase):
    def __init__(self, directory='D:\\05_Send\\'):
        print('init File_Processing', directory)

        if directory is None:
            print('in File_Processing , directory is None')
            super().__init__(r"d:\05_Send\\")

        if self.check_path(directory) == PathChecker.RET_DIR:
            super().__init__(directory)
        else:
            super().__init__(r"d:\05_Send\\")

    def initial_set_yangsoo_excel(self):
        """Copy the initial Yangsoo Excel file to the SEND directory."""

        list_xlsm = self.get_xlsmlist_filter(self.TC_DIR)
        filename = list_xlsm[0]
        print('initial_set_yangsoo_excel', str(filename))
        self.copy_file(self.TC_DIR + filename, self.SEND + self.YANGSOO_EXCEL)

    def aqtfile_to_send(self, well_no=1, aqtstep_include=False):
        """
        Copy AQT files to the SEND directory for a specific well number.
        :param well_no: Well number to include in the file names.
        :param aqtstep_include: Mode to determine which files to copy.
        """
        if aqtstep_include:
            self.copy_file(self.TC_DIR + self.STEP_FILE, self.SEND + f"w{well_no}" + self.STEP_FILE)
        self.copy_file(self.TC_DIR + self.LONG_FILE, self.SEND + f"w{well_no}" + self.LONG_FILE)
        self.copy_file(self.TC_DIR + self.RECOVER_FILE, self.SEND + f"w{well_no}" + self.RECOVER_FILE)

    def duplicate_yangsoo_excel(self, cnt):
        """
        Duplicate the initial Yangsoo Excel file for multiple wells.
        :param cnt: Number of wells to create duplicates for.
        """
        self.delete_files_in_directory(self.SEND)
        self.initial_set_yangsoo_excel()
        for i in range(2, cnt + 1):
            # destination_path = os.path.join(self.SEND, f"A{i}" + self.YANGSOO_REST)
            destination_path = self.fm.join_path_tofilename(self.SEND, f"A{i}" + self.YANGSOO_REST)

            # shutil.copy(self.SEND + self.YANGSOO_EXCEL, destination_path)
            self.copy_file(self.SEND + self.YANGSOO_EXCEL, destination_path)


"""
    2024년 6월 30일

    BASEDIR --> Prn파일, xlsm파일, aqt파일, pdf파일, jpg파일을 이동할 베이스 디텍토리
    d:\09_hardRain\09_ihanseol - 2024\22_음용수 - 당진, 동진아파트 1개공 - 한일지하수\
    이것이 되고

    YANGSOO_DIR = 04_양수시험\
    PRN_DIR = 04_양수시험\01_Prn Save File\
    AQT_DIR = 04_양수시험\02_AQTEver3.4(170414)\
    YANGSOOILBO_DIR = 04_양수시험\03_양수일보\
"""

"""
    2025-9-28
    class PrepareYangsooExcel(FileBase):
    처음 양수파일을 준비하는 과정
    가져올 폴더는 깃허브 엑셀 양수폴더
"""


class PrepareYangsooExcel(FileBase):
    def __init__(self, directory=''):
        super().__init__()
        self.fm = FileBase()

    def duplicate_and_rename_file(self, original_path, destination_folder, cnt):

        if not self.fm.is_valid(destination_folder):
            os.makedirs(destination_folder)

        destination_path = self.fm.join_path_tofilename(destination_folder, f"A{cnt}_ge_OriginalSaveFile.xlsm")
        self.fm.copy_file(original_path, destination_path)
        return destination_path

    def copy_and_get_yangsoo_file(self, nof_well):
        original_file_path = "d:/05_Send/A1_ge_OriginalSaveFile.xlsm"
        destination_folder = "d:/05_Send/"

        source = self.fm.get_file_filter(self.YANGSOO_GITHUB, 'A1*집수정*.xlsm')[-1:]

        my_source = ''.join(source)
        print(my_source)
        if source:
            self.fm.copy_file(my_source, original_file_path)

        print("You entered:", nof_well)
        for i in range(2, nof_well + 1):
            new_file_path = self.duplicate_and_rename_file(original_file_path, destination_folder, i)
            print(f"File duplicated and renamed to: {new_file_path}")


class TransferYangSooFile(FileBase):
    def __init__(self, directory=''):
        super().__init__()
        self.BASEDIR = directory
        self.YANGSOO_BASE = "\\04_양수시험"
        self.PRN_BASE = "\\01_Prn Save File\\"
        self.AQT_BASE = "\\02_AQTEver3.4(170414)\\"
        self.YANGSOOILBO_BASE = "\\03_양수일보\\"

        self.DIR_YANGSOO_TEST = ''
        self.DIR_PRN = ''
        self.DIR_AQT = ''
        self.DIR_YANGSOOILBO = ''

        self.isDIRSET = False
        # basic directory seeting is ready, all self.DIR_ series ...

    def isit_yangsoo_folder(self, folder_name):
        """
            ['D:', '09_hardRain', '09_ihanseol - 2024', '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청']
        """
        current_year = datetime.now().year
        dirlist = self.unfold_path(folder_name)

        if len(dirlist) < 4 or "개소" in dirlist[3]:
            return "MORE"

        if dirlist[1] == "09_hardRain" and dirlist[2].endswith(str(current_year)):
            return self.join_path_forward(dirlist, 4)
        else:
            return "FALSE"

    def isit_yangsoo_inside(self, folder_name):
        """
            ['D:', '09_hardRain', '09_ihanseol - 2024', '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청']
        """
        dir_lsit = self.list_directories_only(folder_name)

        for _ in dir_lsit:
            if _ == '04_양수시험':
                return True

        return False

        # return "d:\\09_hardRain\\09_ihanseol - 2024\\00_YangSoo File Move TestBed\\"

    def dir_yangsoo_test(self):
        if self.DIR_YANGSOO_TEST == '':
            self.DIR_YANGSOO_TEST = self.join_path_from_list([self.BASEDIR, self.YANGSOO_BASE])
            if self.check_path(self.DIR_YANGSOO_TEST) != PathChecker.RET_DIR:
                os.mkdir(self.DIR_YANGSOO_TEST)
        return self.DIR_YANGSOO_TEST

    def dir_prn(self):
        if self.DIR_PRN == '':
            self.DIR_PRN = self.join_path_from_list([self.BASEDIR, self.YANGSOO_BASE, self.PRN_BASE])
            if self.check_path(self.DIR_PRN) != PathChecker.RET_DIR:
                os.mkdir(self.DIR_PRN)

        return self.DIR_PRN

    def dir_aqt(self):
        if self.DIR_AQT == '':
            self.DIR_AQT = self.join_path_from_list([self.BASEDIR, self.YANGSOO_BASE, self.AQT_BASE])
            if self.check_path(self.DIR_AQT) != PathChecker.RET_DIR:
                os.mkdir(self.DIR_AQT)

        return self.DIR_AQT

    def dir_yangsoo_ilbo(self):
        if self.DIR_YANGSOOILBO == '':
            self.DIR_YANGSOOILBO = self.join_path_from_list([self.BASEDIR, self.YANGSOO_BASE, self.YANGSOOILBO_BASE])
            if self.check_path(self.DIR_YANGSOOILBO) != PathChecker.RET_DIR:
                os.mkdir(self.DIR_YANGSOOILBO)

        return self.DIR_YANGSOOILBO

    def setdir_inside_yangsootest(self):
        """
            양수시험안의 디렉토리를 검사해서 01, 02, 03 으로 시작하는 폴더를 발견하면
            그 폴더의 경로를,  dir_aqt, dir_yangsoo_ilbo, dir_prn  이렇게 세팅해주고
            없으면, 폴더를 만들어준다.
        :return:
        """
        if self.check_path(self.dir_yangsoo_test()) != PathChecker.RET_DIR:
            os.makedirs(self.DIR_YANGSOO_TEST)
            os.chdir(self.DIR_YANGSOO_TEST)

            self.print_debug(self.dir_prn())
            self.print_debug(self.dir_aqt())
            self.print_debug(self.dir_yangsoo_ilbo())

        else:
            inside_yangsootest = self.list_directories_only(self.DIR_YANGSOO_TEST)
            if inside_yangsootest:
                print(inside_yangsootest)
                os.chdir(self.DIR_YANGSOO_TEST)

                arg_01 = ''.join([item for item in inside_yangsootest if item.startswith('01')])
                arg_02 = ''.join([item for item in inside_yangsootest if item.startswith('02')])
                arg_03 = ''.join([item for item in inside_yangsootest if item.startswith('03')])

                print(arg_01)
                print(arg_02)
                print(arg_03)

                self.DIR_PRN = self.join_path_from_list([self.DIR_YANGSOO_TEST, '\\', arg_01])
                self.DIR_AQT = self.join_path_from_list([self.DIR_YANGSOO_TEST, '\\', arg_02])
                self.DIR_YANGSOOILBO = self.join_path_from_list([self.DIR_YANGSOO_TEST, '\\', arg_03])
            else:
                os.chdir(self.DIR_YANGSOO_TEST)
                self.print_debug(self.dir_prn())
                self.print_debug(self.dir_aqt())
                self.print_debug(self.dir_yangsoo_ilbo())

    def setBASEDIR(self, directory=''):
        """
          여기서 BASEDIR 은, 타겟폴더 그러니까
          양수시험 파일들을 복사해주기 위한 폴더 가 된다.
          d:\09_hardRain\09_ihanseol - 2024\00_YangSoo File Move TestBed\
          ['D:', '09_hardRain', '09_ihanseol - 2024', '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청']
        :return:
        """

        print('***********' * 5)
        print(directory)
        print('***********' * 5)

        current_year = datetime.now().year

        if directory != '' and self.check_path(directory) == PathChecker.RET_DIR:
            self.BASEDIR = directory
        else:
            sel_folder = self.select_folder(f'd:\\09_hardRain\\09_ihanseol - {current_year}\\')
            self.BASEDIR = self.isit_yangsoo_folder(sel_folder)

        match self.BASEDIR:
            case 'FALSE':
                self.print_debug("it\'s not yangsoo folder")
                self.isDIRSET = False
                return "FALSE"

            case 'MORE':
                self.print_debug("it\'s not yangsoo folder, need one more deep ")
                self.isDIRSET = False
                return "FALSE"

        self.setdir_inside_yangsootest()

        if not self.isDIRSET:
            self.isDIRSET = True

        return self.BASEDIR

    def move_origin_to_ihanseol(self, folder_path):
        """
        여기서, folder_path는, 이동의 기준이 되는
        SEND, SEND2, DOCUMENTS 가 된다.

        Move files based on specific start patterns.
        - aqt files start with 'w'
        - pdf files start with 'a', 'w', or 'p'
        - jpg files start with '*page1'
        """
        fb = FileBase()
        fb.set_directory(folder_path)

        # Get the initial lists of files
        file_mappings = {
            'aqt': fb.get_aqt_files(),
            'pdf': fb.get_pdf_files(),
            'xlsx': fb.get_xlsx_files(),
            'xlsm': fb.get_xlsm_files(),
            'prn': fb.get_prn_files(),
            'jpg_a': fb.get_jpg_filter(sfilter='a*page*'),
            'jpg_p': fb.get_jpg_filter(sfilter='p*page*'),
            'jpg_w': fb.get_jpg_filter(sfilter='w*page*')
        }

        # Filter files based on specific start patterns
        filtered_files = {
            'w_aqt': [f for f in file_mappings['aqt'] if f.startswith('w')],
            'a_pdf': [f for f in file_mappings['pdf'] if f.startswith('a')],
            'w_pdf': [f for f in file_mappings['pdf'] if f.startswith('w')],
            'p_pdf': [f for f in file_mappings['pdf'] if f.startswith('p')],
            'jpg_a': file_mappings['jpg_a'],
            'jpg_p': file_mappings['jpg_p'],
            'jpg_w': file_mappings['jpg_w'],
            'xlsx': file_mappings['xlsx'],
            'xlsm': file_mappings['xlsm'],
            'prn': file_mappings['prn']
        }

        self.print_debug('-')
        for key, files in filtered_files.items():
            print(f"{key}: {files}")
        self.print_debug('-')

        if filtered_files['prn']:
            self._move_files_to_dir(folder_path, filtered_files, ['prn'], self.DIR_PRN, "Prn Files")

        if filtered_files['xlsx'] or filtered_files['xlsm']:
            self._move_files_to_dir(folder_path, filtered_files, ['xlsx', 'xlsm'], self.DIR_YANGSOO_TEST,
                                    "YangSoo Test")

        # Move files to the respective directories
        if filtered_files['a_pdf'] or filtered_files['jpg_a'] or filtered_files['w_aqt'] or filtered_files['jpg_w'] or \
                filtered_files['w_pdf']:
            self._move_files_to_dir(folder_path, filtered_files, ['a_pdf', 'p_pdf', 'jpg_a', 'jpg_p', 'w_aqt'],
                                    self.DIR_AQT, "02_AQTEver3.4(170414)")

        if filtered_files['jpg_w'] or filtered_files['w_pdf']:
            self._move_files_to_dir(folder_path, filtered_files, ['jpg_w', 'w_pdf'], self.DIR_YANGSOOILBO,
                                    "yangsoo ilbo")

    def _move_files_to_dir(self, source_path, filtered_files, keys, target_directory, debug_message):
        fb = FileBase()
        # self.erase_all_yangsoo_test_files(target_directory)
        print(f'this is goto {debug_message}')
        for key in keys:
            for f in filtered_files[key]:
                source = self.join_path_tofilename(source_path, f)
                target = self.join_path_tofilename(target_directory, f)
                fb.move_file(source, target)

    def Test(self):
        fb = FileBase()
        fb.set_directory(self.DOCUMENTS)
        print(fb.get_list_files(['.dat', '.xlsm']))


if __name__ == "__main__":
    py = PrepareYangsoofile()
    py.initial_set_yangsoo_excel()
