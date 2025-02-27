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


class AQTBASE:
    def __init__(self):
        self.AQTESOLV_PATH = 'C:\\WHPA\\AQTEver3.4(170414)\\AQTW32.EXE'
        self.DOCUMENTS = os.path.expanduser("~\\Documents")
        self.SEND = 'D:\\05_Send\\'
        self.SEND2 = 'D:\\06_Send2\\'

        self.YANGSOO_EXCEL = "A1_ge_OriginalSaveFile.xlsm"
        self.YANGSOO_REST = "_ge_OriginalSaveFile.xlsm"
        self.YANSOO_SPEC = "d:\\05_Send\\YanSoo_Spec.xlsx"
        self.TC_DIR = 'C:\\Program Files\\totalcmd\\AqtSolv\\'

        self.STEP_FILE = "_01_step.aqt"
        self.LONG_FILE = "_02_long.aqt"
        self.RECOVER_FILE = "_03_recover.aqt"

        self.ISAQTOPEN = False
        self.DEBUG_YES = True
        self.DELAY = 0.2
        self.IS_BLOCK = False
        """
        self.IS_BLOCK = False :
         because while running the program causes block or wait for user input
         then can't do anything
         so it must be False, user input allowed ...
        """

    @staticmethod
    def block_user_input():
        user32 = ctypes.windll.user32
        user32.BlockInput(True)

    @staticmethod
    def unblock_user_input():
        user32 = ctypes.windll.user32
        user32.BlockInput(False)

    def print_debug(self, message):
        if self.DEBUG_YES:
            if "*-@#$%&" in message:
                print(message * 180)
            else:
                print(message)


class PathChecker:
    RET_FILE = 1
    RET_DIR = 2
    RET_NOTHING = 0

    @staticmethod
    def check_path(path=""):
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

    def resolve_path(self, path=""):
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
    def __init__(self, directory='D:\\05_Send\\'):
        AQTBASE.__init__(self)

        if directory is None:
            print('in File Base , directory is None')
            self.SEND = self.SEND

        self.files = None
        self._directory = directory

        if self.check_path(directory) is False:
            self._set_directory(directory)
        else:
            self._set_directory("d:\\05_Send\\")

    def _set_directory(self, directory):
        """
            Set the working directory and refresh the file list.
        """
        self._directory = directory
        os.chdir(self._directory)
        self.files = os.listdir(directory)

    # def refresh_files(self):
    #     if self.check_path(self.SEND):
    #         self.files = os.listdir(self.SEND)
    #     else:
    #         self._set_directory(r"d:\05_Send\\")

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
        """ Reset the directory and refresh the file list. """
        self._set_directory(directory)

    def _get_files_by_extension(self, extension):
        """ Returns a list of files with the specified extension. """
        self.files = os.listdir(self._directory)
        return [f for f in self.files if f.endswith(extension)]

    def get_xlsm_files(self):
        """ Returns a list of .xlsm files. """
        return self._get_files_by_extension('.xlsm')

    def get_xlsx_files(self):
        """ Returns a list of .xlsm files. """
        return self._get_files_by_extension('.xlsx')

    def get_aqt_files(self):
        """
            Returns a list of .aqt files.
            중간에, 디렉토리가 리프레시 되지 않는경우가 있어서
            일단은, aqtfiles만 해결하기 위해서, refresh_files를 추가 해줌
        """
        # self.refresh_files()
        return self._get_files_by_extension('.aqt')

    def get_dat_files(self):
        """Returns a list of .dat files."""
        return self._get_files_by_extension('.dat')

    def get_prn_files(self):
        """Returns a list of .dat files."""
        return self._get_files_by_extension('.dat')

    def get_pdf_files(self):
        """Returns a list of .dat files."""
        return self._get_files_by_extension('.pdf')

    def get_jpg_files(self):
        """Returns a list of .dat files."""
        return self._get_files_by_extension('.jpg')

    def get_image_files(self):
        """Returns a list of image files."""
        return self.get_list_files(['.jpg', '.jpeg', '.png'])

    def get_list_files(self, file_list):
        """
         return all list from files in file_list
        :param file_list:
           ['.dat','jpg','.xlsm']
        :return:
        """
        rlist = []
        for fl in file_list:
            rlist = rlist + self._get_files_by_extension(fl)
        return rlist

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

    def get_xlsmlist_filter(self, path=None, sfilter="*.xlsm"):
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

    def get_jpg_filter(self, path=None, sfilter="*page1.jpg"):
        """
            Filter .jpg files based on a pattern.
            :param path: Directory to search in.
            :param sfilter: Pattern to filter files.
            :return: Sorted list of filtered .jpg files.
        """
        if path:
            self.set_directory(path)
        _files = self.get_jpg_files()
        return natsorted(fnmatch.filter(_files, sfilter))

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
    def seperate_filename(filename):
        name, ext = os.path.splitext(filename)
        return name, ext

    @staticmethod
    def separate_path(file_path):
        """
            Separate the directory path and the base name from a file path.
            :param file_path: The file path to separate.
            :return: A tuple containing the directory path and the base name.
        """
        return os.path.dirname(file_path), os.path.basename(file_path)

    @staticmethod
    def is_hidden(filepath):
        """
            is filepath are hidden, True is hidden, False otherwise
        """
        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(filepath))
            assert attrs != -1
            return bool(attrs & 2)  # FILE_ATTRIBUTE_HIDDEN
        except (AssertionError, AttributeError):
            return False

    @staticmethod
    def list_directory_contents(path):
        """
         list all file and folder include hidden files:
        """
        try:
            dir_contents = os.listdir(path)
            return dir_contents
        except FileNotFoundError:
            return f"The directory '{path}' does not exist."
        except PermissionError:
            return f"Permission denied to access the directory '{path}'."
        except Exception as e:
            return f"An error occurred: {e}"

    def list_directories_only(self, path):
        """
            list directory only but exclude hidden directory:
        """
        dir_non_hidden = self.list_non_hidden_directories(path)
        dir_hidden = self.list_hidden_directories(path)

        if isinstance(dir_non_hidden, str) or isinstance(dir_hidden, str):
            return "An error occurred while fetching directories."

        return [_d for _d in dir_non_hidden if dir not in dir_hidden]
        # return list(set(dir_non_hidden) - set(dir_hidden))
        # using set, difference

    @staticmethod
    def list_non_hidden_directories(path):
        """
            list directory include hidden directory:
        """
        try:
            # Get the list of all entries in the given path
            entries = os.listdir(path)
            # Filter the list to include only non-hidden directories
            directories = [
                entry for entry in entries
                if os.path.isdir(os.path.join(path, entry)) and not entry.startswith('.')
            ]
            return directories
        except FileNotFoundError:
            return f"The directory '{path}' does not exist."
        except PermissionError:
            return f"Permission denied to access the directory '{path}'."
        except Exception as e:
            return f"An error occurred: {e}"

    @staticmethod
    def last_one(path):
        """
            c:\PythonProject\01_this folder\02_that folder\04_last_folder
            in this case
            return 04_last_folder
            return last one
        """
        seperation = path.split('\\')
        return seperation[len(seperation) - 1]

    def list_hidden_directories(self, path):
        """
            return hidden directories only
        """
        try:
            # Get the list of all entries in the given path
            entries = os.listdir(path)
            # Filter the list to include only hidden directories
            hidden_directories = [
                os.path.join(path, entry) for entry in entries
                if os.path.isdir(os.path.join(path, entry)) and self.is_hidden(os.path.join(path, entry))
            ]
            return [self.last_one(f) for f in hidden_directories]
        except FileNotFoundError:
            return f"The directory '{path}' does not exist."
        except PermissionError:
            return f"Permission denied to access the directory '{path}'."
        except Exception as e:
            return f"An error occurred: {e}"

    def get_dirname(self, file_path):
        """
            Return the directory name of the given file path.
        """
        if self.check_path() == PathChecker.RET_NOTHING:
            print('get_dirname arg is not path ... ', file_path)
            return None

        return os.path.dirname(file_path) + "\\"

    def get_basename(self, file_path):
        """
            Return the base name of the given file path.
        """
        if self.check_path() == PathChecker.RET_NOTHING:
            print('get_dirname arg is not path ... ', file_path)
            return None

        return os.path.basename(file_path)

    def is_exist(self, file_path):
        """
            Check if the file exists.
            os.path.exist return value : True or False
        """
        if self.check_path(file_path) == PathChecker.RET_NOTHING:
            print('get_dirname arg is not path ... ', file_path)
            return False

        return os.path.exists(file_path)

    def is_valid(self, file_path):
        """
            Check if the file exists.
            os.path.exist return value : True or False
        """
        if self.check_path(file_path) == PathChecker.RET_NOTHING:
            print('get_dirname arg is not path ... ', file_path)
            return False

        return os.path.exists(file_path)

    @staticmethod
    def set_pathstring_to_slash(file_path):
        """
          path has \\ and / mix ...
          so it refine the path by one '/'
          파일패스에 \\ 와 / 이 동시에 섞이게 되어 이것을 정리해줄 필요가 있다.
        :return:
        """
        source = file_path
        source = source.replace("\\", "/")
        return source

    def join_path_from_list(self, file_path_list):
        """
         패스의 리스트를 받아서
         그 패스의 리스트를 합쳐준다.
         그리고 합쳐진 패스리스트를 반환한다.

        :param file_path_list:
            file_path_list = ['d:\send\, 'path1', 'path2']
        :return:
            "d:\send\path1\path2'
        """

        base_path = file_path_list[0]
        extra_path = file_path_list[1:]
        for f in extra_path:
            f = self.set_pathstring_to_slash(f)
            base_path = base_path + f

        base_path = self.set_pathstring_to_slash(base_path)
        print('join_path_from_list : ', base_path)
        return base_path

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
            if os.path.exists(destination):
                os.remove(destination)
                print(f'Removed existing file: {destination}')

            shutil.move(source, destination)
            print(f"File moved successfully from '{source}' to '{destination}'")
            return True
        except Exception as e:
            print(f"Error moving file: {e}")
            return False

    def delete_file(self, file_path):
        """
        Delete files from a specified folder.
        :param file_path:
            The folder path where the files are located = directory + filename.
        :return: True if all files were deleted successfully, False otherwise.
        """

        if self.check_path(file_path) == PathChecker.RET_FILE:
            try:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        print(
                            f"{self.get_basename(file_path)} removed successfully from {self.get_dirname(file_path)}.")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
                        return False
                else:
                    print(f"The file {file_path} does not exist ...")
                return True
            except Exception as e:
                print(f"An error occurred while deleting files: {e}")

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
                file_path = str(os.path.join(folder_path, file_name))

                if self.check_path(file_path) == PathChecker.RET_FILE:
                    try:
                        os.remove(file_path)
                        print(f"{file_name} removed successfully from {folder_path}")
                    except Exception as e:
                        print(f"Error deleting {file_name}: {e}")
                        return False
                else:
                    print(f"The file {file_name} does not exist in the folder {folder_path} or its a directory")
            return True
        except Exception as e:
            print(f"An error occurred while deleting files: {e}")
            return False

    def delete_files_in_directory(self, folder_path):
        """
            delte all files in a directory
        :param folder_path:
        :return:
        """
        if self.check_path(folder_path) == PathChecker.RET_DIR:
            files = os.listdir(folder_path)
            print(f"delete_files_in_directory - {files}")
            self.delete_files(folder_path, files)
            return True
        else:
            print(f"delete_files_in_directory: {folder_path} its not a directory")
            return False

    @staticmethod
    def erase_all_yangsoo_test_files(directory):
        # if self.ask_yes_no_question(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                # Check if it's a file (and not a directory)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove the file
                # If it's a directory, use shutil.rmtree to remove it
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    @staticmethod
    def ask_yes_no_question(directory=''):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        try:
            response = messagebox.askyesno("Confirm", f"Do you want to proceed? {directory}")
            if response:
                print("User chose Yes")
                return True
            else:
                print("User chose No")
                return False
        finally:
            root.destroy()

    def select_folder(self, initial_dir=''):
        """
            using tkinter to select the folder where you want to
        :param initial_dir:
        :return:
        """
        root = tk.Tk()
        root.withdraw()  # 메인 윈도우를 숨깁니다.

        if not initial_dir:
            initial_dir = self.SEND

        folder_path = filedialog.askdirectory(initialdir=initial_dir)  # 초기 디렉토리를 설정하여 폴더 선택 대화 상자를 엽니다.

        if folder_path:
            print("선택한 폴더:", folder_path)
        else:
            print("폴더를 선택하지 않았습니다.")

        return folder_path

    def join_path_tofilename(self, folder_path, file_name):
        """
            input folder path and file name return to file_name with path
        :param folder_path:
        :param file_name:
        :return:
        """
        source = folder_path

        if self.check_path(folder_path) == PathChecker.RET_DIR:
            source = os.path.join(folder_path, file_name)
            source = source.replace("/", "\\")

        print('join_path: ', source)
        return source

    def unfold_path(self, folder_path):
        """
            폴더패스를 분리해서, 리스트로 반환
            ['D:', '09_hardRain', '09_ihanseol - 2024', '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청']
        """
        if not self.check_path(folder_path):
            folder_path = self.SEND

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

        if not isinstance(folder_list, list):
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


class AqtProjectInfoInjector(FileBase):
    def __init__(self, directory, _company):
        super().__init__()
        self.COMPANY = _company
        self.ADDRESS = ""
        self.DEBUG = True
        self.DIRECTORY = directory

    def set_address(self, value):
        self.ADDRESS = value

    def set_company(self, value):
        self.COMPANY = value

    def open_aqt(self, filename):
        if not self.ISAQTOPEN:
            print(f'open_aqt: {filename}')
            os.startfile(self.AQTESOLV_PATH)
            self.ISAQTOPEN = True
            time.sleep(self.DELAY)

        pyautogui.hotkey('ctrl', 'o')
        pyautogui.press('backspace')
        pyautogui.typewrite(self.SEND + filename)
        time.sleep(self.DELAY)
        pyautogui.press('enter')
        time.sleep(self.DELAY)

    def open_aqt_file(self, filename):
        if not self.ISAQTOPEN:
            print(f'open_aqt: {self.SEND + filename}')
            os.startfile(self.SEND + filename)
            self.ISAQTOPEN = True
            time.sleep(self.DELAY)

    def close_aqt(self):
        if self.ISAQTOPEN:
            pyautogui.hotkey('ctrl', 's')
            time.sleep(self.DELAY)
            pyautogui.hotkey('alt', 'f4')
            time.sleep(self.DELAY)

        self.ISAQTOPEN = False

    def main_job(self, well, address):
        if self.ISAQTOPEN:
            time.sleep(0.2)
            pyperclip.copy(self.COMPANY)
            # enter project info
            pyautogui.hotkey('alt', 'e')
            # time.sleep(0.2)
            pyautogui.press('r')
            # project info

            pyautogui.hotkey('ctrl', 'v')

            for _ in range(3):
                pyautogui.press('tab')
                # time.sleep(0.2)

            pyperclip.copy(address)
            pyautogui.hotkey('ctrl', 'v')

            pyautogui.press('tab')
            pyperclip.copy(well)
            pyautogui.hotkey('ctrl', 'v')

            pyautogui.press('tab')
            pyautogui.hotkey('ctrl', 'v')

            pyautogui.press('enter')
            pyautogui.hotkey('ctrl', 's')
            time.sleep(self.DELAY)

    def aqt_mainaction(self, well_no, address, wfiles):
        """
        :param well_no:
             공번,
        :param address:
              주소
        :param wfiles:
            프로젝트 인포 세팅할 , 파일리스트
        """
        for j, file in enumerate(wfiles):
            self.open_aqt_file(file)
            self.main_job(f"W-{well_no}", address)
            self.close_aqt()

    @staticmethod
    def process_address(input_str):
        """
        :param input_str:
            주어진 주소값을 입력받고, 그 주소가 길면
            그 주소를 정해진 규칙에 의해서 잘라서
            반환한다.
            aqtsolv project_info 의 주소길이에 맟추어서

            부여읍,신정리177,실지번,산37-1 <-- AqtSolver 에 들어가는 최대치
            글자의 갯수로 20자이다.

        :return:
        """
        if len(input_str) >= 18:
            result = input_str.replace('번지', '')
            parts = input_str.split()
            i = 0

            for part in parts:
                if part.endswith("읍") or part.endswith("면") or part.endswith("동") or part.endswith(
                        "구") or part.endswith("시"):
                    break
                i += 1

            result = ' '.join(parts[i:])
            address_list = result.split()
            filtered_list = [item for item in address_list if not (item.endswith('아파트') or item == ',')]
            address_string = ' '.join(filtered_list)

            return address_string
        else:
            return input_str

    @staticmethod
    def extract_number(s):
        """
        :param s:
            주어진 스트링 S값을 입력받아,
            숫자만 추려서, 정수로 반환한다.
        :return:
        """
        return int(re.findall(r'\d+', s)[0])

    def change_aqt_filename(self):
        """
        aqtfile 을 SEND 에서 불러와서
        파일이름중에, 복사본이 있으면, 이것을 바꾸어 준다.
        """
        aqtfiles = self.get_aqt_files()
        for filename in aqtfiles:
            name, ext = self.seperate_filename(filename)

            if ext == ".aqt" and "_01" not in name:
                suffixes = [" - 복사본", " - Copy"]
                for suffix in suffixes:
                    if suffix in name:
                        new_name = name.replace(suffix, "_01") + ext
                        os.rename(os.path.join(self.SEND, filename), os.path.join(self.SEND, new_name))
                        break

    def get_wellno_list_insend(self):
        """
            Send folder 에 있는 , aqtfiles 의 관정번호를
            Set으로 추려서 유닉하게 만든다.
        """

        aqtfiles = self.get_aqt_files()
        aqtfiles = natsorted(aqtfiles)

        wellnos = [self.extract_number(f.split('_')[0]) for f in aqtfiles]
        return list(set(wellnos))

    def Set_Projectinfo(self, company, address):
        print(f"Set_Projectinfo,1 - company: {company} / address: {address}")
        self.change_aqt_filename()

        processed_address = self.process_address(address)
        self.set_company(company)
        self.set_address(processed_address)

        print(f'len(address) - {len(processed_address)}')
        if len(processed_address) > 21:
            print(f"its over the size ...{processed_address}")
        else:
            print(f"its in the size ...{processed_address}")

        self.block_user_input()

        aqtfiles = self.get_aqt_files()
        print(f'Set_Projectinfo2, - aqtfiles: {aqtfiles}')

        if not self.ISAQTOPEN:
            if aqtfiles:
                w_list = self.get_wellno_list_insend()
                for i in w_list:
                    wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")
                    print(f'Set_Projectinfo3, - wfiles: {wfiles}')
                    if wfiles:
                        self.aqt_mainaction(i, processed_address, wfiles)
            else:
                print('aqt files does not found ...')
        else:
            self.ISAQTOPEN = False

        time.sleep(0.5)
        self.unblock_user_input()


class AqtExcelProjectInfoInjector(AqtProjectInfoInjector):
    def __init__(self, directory, company):
        super().__init__(directory, company)
        # self.df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
        self.df = pd.DataFrame()
        self.fb = FileBase()

    def set_dataframe(self, df):
        self.df = df

    def get_gong_n_address(self, row_index):
        """
            줄번호, row_index 를 받아서
            그 해당하는 인덱스의 공번, 주소를 리턴
        """

        if self.df.empty and self.is_exist(r"d:\05_Send\YanSoo_Spec.xlsx"):
            df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
            self.set_dataframe(df)

        try:
            row_data = self.df.iloc[row_index - 1, :].tolist()
            str_gong = row_data[0]
            address = row_data[1]
            time.sleep(1)
        except Exception as e:
            print(f"get_gong_n_address: {e}")
            return None, "None"

        print(str_gong, address)
        return str_gong, address

    def get_last_gong(self):
        """
          엑셀파일의 마지막 공번을 리턴
        :return:
        """

        if self.df.empty and self.is_exist(r"d:\05_Send\YanSoo_Spec.xlsx"):
            df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
            self.set_dataframe(df)

        try:
            str_gong = self.df.iloc[-1, 0]
            gong = self.df.extract_number(str_gong)
            time.sleep(1)
            return gong
        except Exception as e:
            print(f"get_last_gong: {e}")
            return None

    def get_gong_list(self):
        """
        :return:
            Excel 파일을 df 로 불러들여
            이곳에서 공번만을 주려서
            그것을  정수로, 돌려준다.
        """
        if self.df.empty and self.is_exist(r"d:\05_Send\YanSoo_Spec.xlsx"):
            df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
            self.set_dataframe(df)

        g_list = []
        gong_column = self.df['gong'].tolist()
        for f in gong_column:
            n = self.extract_number(f)
            g_list.append(n)
        print(f'g_list: {g_list}')
        return g_list

    def delete_difference(self, file_list):
        """
        :param file_list:
            [3, 4, 5]
            파일리스트에, 지워야할 관정파일들의 리스트를 받고
            그것을 SEND폴더에서 찾아서, 엑셀에 없는 공번들을 가진 aqt 파일을 지운다.
        :return:
        """
        aqtfiles = natsorted(self.get_aqt_files())

        for f in file_list:
            ffiles = fnmatch.filter(aqtfiles, f"w{f}_*.aqt")
            for _ in ffiles:
                os.remove(_)

    def process_projectinfo_byexcel(self, company, address):

        if self.df.empty and self.is_exist(r"d:\05_Send\YanSoo_Spec.xlsx"):
            df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
            self.set_dataframe(df)

        self.set_company(company)
        self.set_address(address)
        self.change_aqt_filename()

        send_list = self.get_wellno_list_insend()
        xlsx_list = self.get_gong_list()

        difference_set = list(set(send_list) - set(xlsx_list))
        self.delete_difference(difference_set)

        aqtfiles = natsorted([f for f in os.listdir() if f.endswith('.aqt')])
        aqtfiles = self.get_aqt_files()
        print(f'aqtfiles: {aqtfiles}')
        # self.block_user_input()

        for i in xlsx_list:
            gong, excel_address = self.get_gong_n_address(i)

            if gong is None:
                self.close_aqt()
                return None

            processed_address = self.process_address(excel_address)
            print(f'gong: {gong}, address: {processed_address}')
            wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")
            print(f"wfiles: {wfiles}")

            if wfiles:
                if self.DEBUG:
                    print('Processing file: ', wfiles)
                self.aqt_mainaction(self.extract_number(gong), processed_address, wfiles)

        if self.DEBUG:
            print('All files processed.')

        self.unblock_user_input()

    def process_projectinfo_likesejong(self, company):

        if self.df.empty and self.is_exist(r"d:\05_Send\YanSoo_Spec.xlsx"):
            df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
            self.set_dataframe(df)

        self.set_company(company)
        # self.set_address(address)
        self.change_aqt_filename()

        send_list = self.get_wellno_list_insend()
        xlsx_list = self.get_gong_list()

        difference_set = list(set(send_list) - set(xlsx_list))
        self.delete_difference(difference_set)

        aqtfiles = natsorted([f for f in os.listdir() if f.endswith('.aqt')])
        aqtfiles = self.get_aqt_files()
        if not aqtfiles:
            print('Error No AQT')
            return None

        print(f'aqtfiles: {aqtfiles}')
        # self.block_user_input()

        for i in xlsx_list:
            gong, excel_address = self.get_gong_n_address(i)

            if gong is None:
                self.close_aqt()
                return None

            processed_address = self.process_address(excel_address)
            self.set_address(processed_address)

            print(f'gong: {gong}, address: {processed_address}')
            wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")
            print(f"wfiles: {wfiles}")

            if wfiles:
                if self.DEBUG:
                    print('Processing file: ', wfiles)
                self.aqt_mainaction(self.extract_number(gong), processed_address, wfiles)

        if self.DEBUG:
            print('All files processed.')

        self.unblock_user_input()


if __name__ == "__main__":
    # fp = PrepareYangsoofile()
    # fp.aqtfile_to_send(well_no=1)
    # fp.duplicate_yangsoo(3)

    # tyd = TransferYangSooFile()
    # tyd.setBASEDIR()
    # tyd.move_origin_to_ihanseol(tyd.SEND2)

    # tyd.move_origin_to_ihanseol()
    # tyd.move_send2_to_ihanseol()

    #
    # tyd.move_documents_to_ihanseol()
    # tyd.Test()

    # main
    # spi = AqtProjectInfoInjector("d:\\05_Send", "aa")
    # print(spi.process_address("충청남도 당진시 송악읍 신평로 1469"))

    # test, initial_set_yangsoo_excel
    py = PrepareYangsoofile()
    py.initial_set_yangsoo_excel()
