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


"""
class AQTBASE:
class PathChecker:
class FileBase(AQTBASE, PathChecker):

"""

class AQTBASE:
    def __init__(self):
        self.AQTESOLV_PATH = 'C:\\WHPA\\AQTEver3.4(170414)\\AQTW32.EXE'
        self.DOCUMENTS = os.path.expanduser("~\\Documents")
        self.SEND = 'D:\\05_Send\\'
        self.SEND2 = 'D:\\06_Send2\\'

        self.YANGSOO_EXCEL = "A1_ge_OriginalSaveFile.xlsm"
        self.YANGSOO_REST = "_ge_OriginalSaveFile.xlsm"
        self.YANSOO_SPEC = "d:\\05_Send\\YanSoo_Spec.xlsx"

        #2025-9-28, Add Github folder path
        self.YANGSOO_GITHUB = "d:\\12_dev\\02_Excel3\\01_Acquifer Pumping Test\\01_양수시험"
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

    def get_file_filter(self, path=None, sfilter="*.hwp"):
        """
            Filter .jpg files based on a pattern.
            :param path: Directory to search in.
            :param sfilter: Pattern to filter files.
            :return: Sorted list of filtered .jpg files.
        """
        if path:
            self.set_directory(path)
        self.files = os.listdir(self._directory)
        return natsorted(fnmatch.filter(self.files, sfilter))

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
