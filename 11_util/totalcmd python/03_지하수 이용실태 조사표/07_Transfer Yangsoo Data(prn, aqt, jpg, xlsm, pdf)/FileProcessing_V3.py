import os
import shutil
import fnmatch
from natsort import natsorted
import tkinter as tk
from tkinter import filedialog
from datetime import datetime


class AQTBASE:
    def __init__(self):
        self.AQTESOLV_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
        self.DOCUMENTS = r'C:\Users\minhwasoo\Documents\\'
        self.SEND = r'D:\05_Send\\'
        self.SEND2 = r'D:\06_Send2\\'

        self.YANGSOO_EXCEL = r"A1_ge_OriginalSaveFile.xlsm"
        self.YANGSOO_REST = "_ge_OriginalSaveFile.xlsm"
        self.TC_DIR = r'C:\Program Files\totalcmd\AqtSolv\\'

        self.STEP_FILE = "_01_step.aqt"
        self.LONG_FILE = "_02_long.aqt"
        self.RECOVER_FILE = "_03_recover.aqt"

        self.ISAQTOPEN = False
        self.DEBUG_YES = True
        self.DELAY = 0.5
        self.IS_BLOCK = False
        """
        self.IS_BLOCK = False :
         because while running the program causes block or wait for user input
         then can't do anything
         so it must be False, user input allowed ...
        """

    def print_debug(self, message):
        if self.DEBUG_YES:
            print(message)


class PathChecker:
    RET_FILE = 1
    RET_DIR = 2
    RET_NOTHING = 0

    @staticmethod
    def check_path(path=''):
        if path is None:
            return PathChecker.RET_NOTHING

        if os.path.exists(path):
            if os.path.isfile(path):
                return PathChecker.RET_FILE
            elif os.path.isdir(path):
                return PathChecker.RET_DIR
            else:
                return PathChecker.RET_NOTHING
        else:
            return PathChecker.RET_NOTHING

    def resolve_path(self, path=''):
        if path is None:
            return PathChecker.RET_NOTHING

        match self.check_path(path):
            case PathChecker.RET_FILE:
                print("Given Path is File")
                return PathChecker.RET_FILE
            case PathChecker.RET_DIR:
                print("Given Path is DIR")
                return PathChecker.RET_DIR
            case PathChecker.RET_NOTHING:
                print("Given Path is NOTHING")
                return PathChecker.RET_NOTHING
            case _:
                print("Given Path is NOTHING")
                return PathChecker.RET_NOTHING


class FileBase(AQTBASE, PathChecker):
    def __init__(self, directory=r'D:\05_Send\\'):
        AQTBASE.__init__(self)

        if directory is None:
            print('in File Base , directory is None')

        if self.check_path(directory) is False:
            self._set_directory(directory)
        else:
            self._set_directory(r"d:\05_Send\\")

    def _set_directory(self, directory):
        """
            Set the working directory and refresh the file list.
        """
        self._directory = directory
        os.chdir(self._directory)
        self.files = os.listdir(directory)

    @property
    def directory(self):
        """
            Getter for the directory.
        """
        return self._directory

    @directory.setter
    def directory(self, value):
        """
            Setter for the directory. Refreshes file list if the directory changes.
        """
        if self._directory != value:
            self._set_directory(value)

    def set_directory(self, directory):
        """
            Reset the directory and refresh the file list.
        """
        self._set_directory(directory)

    def _get_files_by_extension(self, extension):
        """
            Returns a list of files with the specified extension.
        """
        return [f for f in self.files if f.endswith(extension)]

    def get_xlsm_files(self):
        """
            Returns a list of .xlsm files.
        """
        return self._get_files_by_extension('.xlsm')

    def get_aqt_files(self):
        """
            Returns a list of .aqt files.
        """
        return self._get_files_by_extension('.aqt')

    def get_dat_files(self):
        """Returns a list of .dat files."""
        return self._get_files_by_extension('.dat')

    def get_xlsm_filter(self, path=None, sfilter="*_ge_OriginalSaveFile.xlsm"):
        """
            Filter .xlsm files based on a pattern.
            :param path: Directory to search in.
            :param sfilter: Pattern to filter files.
            :return: Sorted list of filtered .xlsm files.
        """
        if path:
            self.set_directory(path)
        xl_files = self.get_xlsm_files()
        return natsorted(fnmatch.filter(xl_files, sfilter))

    @staticmethod
    def has_path(file_name):
        """
            Check if the file name includes a path.
            :param file_name: The file name to check.
            :return: True if the file name includes a path, False otherwise.
        """
        head, tail = os.path.split(file_name)
        print(f"head: '{head}'  tail: '{tail}'  includes a path. Performing action...")
        return bool(head)

    @staticmethod
    def separate_path(file_path):
        """
            Separate the directory path and the base name from a file path.
            :param file_path: The file path to separate.
            :return: A tuple containing the directory path and the base name.
        """
        return os.path.dirname(file_path), os.path.basename(file_path)

    def get_dirname(self, file_path):
        """
            Return the directory name of the given file path.
        """
        if self.check_path == PathChecker.RET_NOTHING:
            print('get_dirname arg is not path ... ', file_path)
            return None

        return os.path.dirname(file_path) + "\\"

    def get_basename(self, file_path):
        """
            Return the base name of the given file path.
        """
        if self.check_path == PathChecker.RET_NOTHING:
            print('get_dirname arg is not path ... ', file_path)
            return None

        return os.path.basename(file_path)

    def is_exist(self, file_path):
        """
            Check if the file exists.
            os.path.exist return value : True or False
        """
        if self.check_path == PathChecker.RET_NOTHING:
            print('get_dirname arg is not path ... ', file_path)
            return False

        return os.path.exists(file_path)

    def is_valid(self, file_path):
        """
            Check if the file exists.
            os.path.exist return value : True or False
        """
        if self.check_path == PathChecker.RET_NOTHING:
            print('get_dirname arg is not path ... ', file_path)
            return False

        return os.path.exists(file_path)

    @staticmethod
    def copy_file(source, destination):
        """
        Copy a file from source to destination.
        source and destination are must be full path

        :param source: Source file path.
        :param destination: Destination file path.
        :return: True if the file was copied successfully, False otherwise.
        """
        try:
            shutil.copy(source, destination)
            print(f"File copied successfully from '{source}' to '{destination}'")
            return True
        except Exception as e:
            print(f"Error copying file: {e}")
            return False

    @staticmethod
    def move_file(source, destination):
        """
        Move a file from source to destination.
        source and destination are must be full path

        :param source: Source file path.
        :param destination: Destination file path.
        :return: True if the file was moved successfully, False otherwise.
        """
        try:
            shutil.move(source, destination)
            print(f"File moved successfully from '{source}' to '{destination}'")
            return True
        except Exception as e:
            print(f"Error moving file: {e}")
            return False

    def delete_files(self, folder_path, files):
        """
        Delete files from a specified folder.
        :param folder_path: The folder path where the files are located.
        :param files: List of file names to delete.
        :return: True if all files were deleted successfully, False otherwise.
        """

        if self.check_path(folder_path) == PathChecker.RET_FILE:
            folder_path = self.get_dirname(folder_path)

        try:
            for file_name in files:
                file_path = os.path.join(folder_path, file_name)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        print(f"{file_name} has been removed successfully from {folder_path}.")
                    except Exception as e:
                        print(f"Error deleting {file_name}: {e}")
                        return False
                else:
                    print(f"The file {file_name} does not exist in the folder {folder_path}.")
            return True
        except Exception as e:
            print(f"An error occurred while deleting files: {e}")
            return False

    def select_folder(self, initial_dir=''):
        root = tk.Tk()
        root.withdraw()  # 메인 윈도우를 숨깁니다.

        if not initial_dir:
            initial_dir = self.directory

        folder_path = filedialog.askdirectory(initialdir=initial_dir)  # 초기 디렉토리를 설정하여 폴더 선택 대화 상자를 엽니다.

        if folder_path:
            print("선택한 폴더:", folder_path)
        else:
            print("폴더를 선택하지 않았습니다.")

        return folder_path

    def unfold_path(self, folder_path):
        """
            폴더패스를 분리해서, 리스트로 반환
            ['D:', '09_hardRain', '09_ihanseol - 2024', '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청']
        """
        if not self.check_path(folder_path):
            folder_path = self.directory

        parts = folder_path.replace('/', '\\').split('\\')
        for part in parts:
            print(part)
        return parts

    @staticmethod
    def join_path_reverse(folder_list, n=0):
        """
        :param folder_list:
           this is a list of folders of disect
            ['D:', '09_hardRain', '09_ihanseol - 2024', '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청']

        :param n:
            끝에서 부터 몇자리까지 할것인가
            0 : 전체패스
            1 : 끝에서 부터 한자리 전까지 합침

            n 이 양수 이면 -를 부치고
            n 이 음수이면 그냥 쓰고
        :return:
        """

        if type(folder_list) != list:
            return None

        if n == 0:
            return "\\".join(folder_list[:])
        elif n > 0:
            return "\\".join(folder_list[:-n])
        else:
            return "\\".join(folder_list[:n])

    @staticmethod
    def join_path_forward(folder_list, n=0):
        """
        :param folder_list:
           this is a list of folders of disect
            ['D:', '09_hardRain', '09_ihanseol - 2024', '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청']

        :param n:
            앞에서 부터 몇자리까지 할것인가
            0 : 전체패스
            1 : 끝에서 부터 한자리 전까지 합침

            n 이 양수 이면 -를 부치고
            n 이 음수이면 그냥 쓰고
        :return:
        """

        depth = len(folder_list)
        if depth == 0:
            return None

        n = abs(n)
        if depth <= n:
            return "\\".join(folder_list[:n])


class PrepareYangsoofile(FileBase):
    def __init__(self, directory=r'D:\05_Send\\'):
        print('init FileProcessing', directory)

        if directory is None:
            print('in FileProcessing , directory is None')
            super().__init__(r"d:\05_Send\\")

        if self.check_path(directory) == PathChecker.RET_DIR:
            super().__init__(directory)
        else:
            super().__init__(r"d:\05_Send\\")

    def initial_set_yangsoo(self):
        """Copy the initial Yangsoo Excel file to the SEND directory."""
        self.copy_file(self.TC_DIR + self.YANGSOO_EXCEL, self.SEND + self.YANGSOO_EXCEL)

    def aqt_send(self, well_no=1, mod='include'):
        """
        Copy AQT files to the SEND directory for a specific well number.
        :param well_no: Well number to include in the file names.
        :param mod: Mode to determine which files to copy.
        """
        if mod == 'include':
            self.copy_file(self.TC_DIR + self.STEP_FILE, self.SEND + f"w{well_no}" + self.STEP_FILE)
        self.copy_file(self.TC_DIR + self.LONG_FILE, self.SEND + f"w{well_no}" + self.LONG_FILE)
        self.copy_file(self.TC_DIR + self.RECOVER_FILE, self.SEND + f"w{well_no}" + self.RECOVER_FILE)

    def duplicate_yangsoo(self, cnt):
        """
        Duplicate the initial Yangsoo Excel file for multiple wells.
        :param cnt: Number of wells to create duplicates for.
        """
        self.initial_set_yangsoo()
        for i in range(2, cnt + 1):
            destination_path = os.path.join(self.SEND, f"A{i}" + self.YANGSOO_REST)
            shutil.copy(self.SEND + self.YANGSOO_EXCEL, destination_path)


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


class TransferYangSooData(FileBase):
    def __init__(self):
        super().__init__()
        self.BASEDIR = ""
        self.YANGSOO_TEST = ""
        self.YANGSOO_BASE = "\\04_양수시험"
        self.PRN_BASE = "\\04_양수시험\\01_Prn Save File\\"
        self.AQT_BASE = "\\04_양수시험\\02_AQTEver3.4(170414)\\"
        self.YANGSOOILBO_BASE = "\\04_양수시험\\03_양수일보\\"

        self.DIR_YANGSOO_TEST = ''
        self.DIR_PRN = ''
        self.DIR_AQT = ''
        self.DIR_YANGSOOILBO = ''

    def isit_yangsoo_folder(self, folder_name):
        """
            ['D:', '09_hardRain', '09_ihanseol - 2024', '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청']
        """
        current_year = datetime.now().year
        dirlist = self.unfold_path(folder_name)

        if dirlist[1] == "09_hardRain" and dirlist[2].endswith(str(current_year)):
            return self.join_path_forward(dirlist, 4)
        else:
            return "FALSE"

    def dir_yangsoo_test(self):
        if self.DIR_YANGSOO_TEST == '':
            self.YANGSOO_TEST = self.BASEDIR + self.YANGSOO_BASE
        return self.YANGSOO_TEST

    def dir_prn(self):
        if self.DIR_PRN == '':
            self.DIR_PRN = self.BASEDIR + self.YANGSOO_BASE + self.PRN_BASE
        return self.DIR_PRN

    def dir_aqt(self):
        if self.DIR_AQT == '':
            self.DIR_AQT = self.BASEDIR + self.YANGSOO_BASE + self.AQT_BASE
        return self.DIR_AQT

    def dir_yangsoo_ilbo(self):
        if self.DIR_YANGSOOILBO == '':
            self.DIR_YANGSOOILBO = self.BASEDIR + self.YANGSOO_BASE + self.YANGSOOILBO_BASE
        return self.DIR_YANGSOOILBO

    def setBASEDIR(self):
        """
        ['D:', '09_hardRain', '09_ihanseol - 2024', '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청']
        :return:
        """
        sel_folder = self.select_folder('')
        self.BASEDIR = self.isit_yangsoo_folder(sel_folder)
        if self.BASEDIR == 'FALSE':
            self.print_debug("it\'s not yangsoo folder")
            return False

        self.print_debug(self.BASEDIR)
        self.print_debug(self.dir_yangsoo_test())
        self.print_debug(self.dir_prn())
        self.print_debug(self.dir_aqt())
        self.print_debug(self.dir_yangsoo_ilbo())

        return True


if __name__ == "__main__":
    # fp = PrepareYangsoofile()
    # fp.aqt_send(well_no=1)
    # fp.duplicate_yangsoo(3)

    tyd = TransferYangSooData()
    tyd.setBASEDIR()
