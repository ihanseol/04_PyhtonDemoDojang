import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import fnmatch
import os
import shutil
from pathlib import Path
from natsort import natsorted
import ctypes
from datetime import datetime
import time
import re
import pyperclip
import pyautogui
import pandas as pd

"""
    2025/04/06
    file_path convert str to Path object
"""


class AQTBASE:
    def __init__(self):
        self.aqtesolv_path = Path('c:/WHPA/AQTEver3.4(170414)/AQTW32.EXE')
        self.documents = Path.home() / "Documents"
        self.send = Path('d:/05_send')
        self.send2 = Path('d:/06_send2')

        self.yangsoo_excel = "A1_ge_OriginalSaveFile.xlsm"
        self.yangsoo_rest = "_ge_OriginalSaveFile.xlsm"
        self.yangsoo_spec = "d:/05_send/YanSoo_Spec.xlsx"
        self.tc_dir = Path('c:/Program Files/totalcmd/AqtSolv')

        self.step_file = "_01_step.aqt"
        self.long_file = "_02_long.aqt"
        self.recover_file = "_03_recover.aqt"

        self.isaqtopen = False
        self.debug_yes = True
        self.delay = 0.2
        self.is_block = False
        """
        self.is_block = False :
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
        if self.debug_yes:
            if "*-@#$%&" in message:
                print(message * 180)
            else:
                print(message)


class PathChecker:
    RET_FILE = 1
    RET_DIR = 2
    RET_NOTHING = 0

    def line_print(self, msg):
        print('-' * 80)
        print(msg)
        print('-' * 80)

    def check_path(self, file_path):
        if isinstance(file_path, Path):
            if file_path.is_file():
                # print("  - It is a file.")
                return PathChecker.RET_FILE
            elif file_path.is_dir():
                # print("  - It is a directory.")
                return PathChecker.RET_DIR
            else:
                return PathChecker.RET_NOTHING
        else:
            self.line_print(f"The file path '{file_path}' is not a Path object.")
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
    def __init__(self, directory=Path('d:/05_send')):
        AQTBASE.__init__(self)

        if directory is None:
            print('in File Base , directory is None')

        self.files = None
        self._directory = directory

        if self.check_path(directory) is PathChecker.RET_DIR:
            self._set_directory(directory)
        else:
            self._set_directory(self.send)

    def _set_directory(self, target_dir):
        """
            Set the working directory and refresh the file list.
        """

        try:
            # Change the current working directory
            self._directory = target_dir
            os.chdir(target_dir)
            self.files = os.listdir(target_dir)
            if self.debug_yes: print(f" _set_directory(),  Successfully changed directory to: {Path.cwd()}")

        except FileNotFoundError:
            print(f"Error: Directory not found: {target_dir}")
        except NotADirectoryError:
            print(f"Error: Not a directory: {target_dir}")
        except OSError as e:
            print(f"Error changing directory to {target_dir}: {e}")

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

    @staticmethod
    def line_print(msg, **kwargs):
        print('-' * 80)
        print(msg)
        print('-' * 80)

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
    def is_hidden(filepath: Path) -> bool:
        """Checks if a file or directory is considered hidden."""
        name = filepath.name
        if name.startswith('.'):
            return True  # Unix-like hidden files

        if os.name == 'nt':
            import ctypes
            try:
                attrs = ctypes.windll.kernel32.GetFileAttributesW(str(filepath))
                if attrs != -1:
                    return (attrs & 0x2) != 0  # Check for the FILE_ATTRIBUTE_HIDDEN flag
            except Exception as e:
                return False  # Unable to get attributes, assume not hidden
        return False

    def get_filelist_indir(self, target_dir: Path = None):
        try:
            if not isinstance(target_dir, Path):
                target_dir = self.send

            if target_dir.is_dir():
                file_list = [
                    item for item in target_dir.iterdir()
                    if item.is_file() and not self.is_hidden(item)
                ]

                if file_list:
                    return file_list
                else:
                    print(f"No non-hidden files found in '{target_dir}'.")
            else:
                print(f"Error: '{target_dir}' is not a valid directory.")

        except OSError as e:
            print(f"An error occurred: {e}")

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

    def list_directories_only(self, folder_path) -> object:
        """
            folder_path:
                Path object

            list directory only but exclude hidden directory:
        """
        non_hidden_directory: object = self.list_non_hidden_directories(folder_path)
        dir_hidden: object = self.list_hidden_directories(folder_path)

        if isinstance(non_hidden_directory, str) or isinstance(dir_hidden, str):
            return "An error occurred while fetching directories."

        return [_d for _d in non_hidden_directory if _d not in dir_hidden]


    def list_hidden_directories(self, folder_path):
        """
            return hidden directories only
        """
        try:
            # Get the list of all entries in the given path
            entries = os.listdir(folder_path)
            # Filter the list to include only hidden directories
            hidden_directories = [
                Path(entry) for entry in entries if
                (os.path.isdir(entry) and self.is_hidden(Path(entry)))
            ]
            return hidden_directories
        except FileNotFoundError:
            return f"The directory '{folder_path}' does not exist."
        except PermissionError:
            return f"Permission denied to access the directory '{folder_path}'."
        except Exception as e:
            return f"An error occurred: {e}"

    def list_non_hidden_directories(self, folder_path) -> object:
        """
            list directory include hidden directory:
            folder_path -> Path object

            return:
                list of all non-hidden directories. in a folder_path
                :rtype: object
        """

        try:
            # Get the list of all entries in the given path
            entries = os.listdir(folder_path)
            # Filter the list to include only non-hidden directories
            directories = [
                Path(entry) for entry in entries
                if os.path.isdir(entry) and not entry.startswith('.') and not self.is_hidden(Path(entry))
            ]
            return directories
        except FileNotFoundError:
            return f"The directory '{folder_path}' does not exist."
        except PermissionError:
            return f"Permission denied to access the directory '{folder_path}'."
        except Exception as e:
            return f"An error occurred: {e}"

    @staticmethod
    def last_one(folder_path):
        """
            2025-4-6
            path -> Path object

            c:\PythonProject\01_this folder\02_that folder\04_last_folder
            in this case
            return 04_last_folder
            return last one directory
        """

        if not isinstance(folder_path, Path):
            seperation = folder_path.split('\\')
            return seperation[len(seperation) - 1]
        else:
            return folder_path.parent

    def get_dirname(self, file_path):
        """
            Return the directory name of the given file path.
        """
        if not isinstance(file_path, Path):
            self.line_print(f"The file path '{file_path}' is not a Path object.")

        if self.debug_yes: print(f" debug : {self.get_dirname.__name__}() : {str(file_path)}")

        if self.check_path(file_path) == PathChecker.RET_NOTHING:
            print('get_dirname arg is not path ... ', file_path)
            return None

        return file_path.parent

    def get_basename(self, file_path):
        """
            Return the base name of the given file path.
            os.path.basename("/home/user/documents/report.pdf") returns "report.pdf"
        """
        if not isinstance(file_path, Path):
            self.line_print(f"The file path '{file_path}' is not a Path object.")

        if self.check_path(file_path) == PathChecker.RET_NOTHING:
            print(' get_dirname() argument is not path ... ', file_path)
            return None

        return file_path.name

    def is_exist(self, file_path):
        """
            Check if the file exists.
            file_path --> Path object

            os.path.exist return value : True or False
        """
        if self.check_path(file_path) == PathChecker.RET_NOTHING:
            print(' get_dirname() argument is not path ... ', file_path)
            return False

        return os.path.exists(str(file_path))

    def is_valid(self, file_path):
        """
            Check if the file exists.
            os.path.exist return value : True or False
        """
        return self.is_exist(file_path)

    @staticmethod
    def set_pathstring_to_slash(file_path):
        """
          path has \\ and / mix ...
          so it refine the path by one '/'
          파일패스에 \\ 와 / 이 동시에 섞이게 되어 이것을 정리해줄 필요가 있다.
        :return:
        """

        if not isinstance(file_path, Path):
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
        source and destination are must be Path object


        :param
            source: Source file path.
        :param
            destination: Destination file path.
        :return:
            True if the file was copied successfully, False otherwise.
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
        source and destination are must be Path Object

        :param
            source: Source file path.
        :param
            destination: Destination file path.
        :return:
            True if the file was moved successfully, False otherwise.
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
            file_path is the Path Object
        :return:
            True if all files were deleted successfully, False otherwise.
        """

        if file_name := self.get_basename(file_path):
            try:
                dir_name = self.get_dirname(file_path)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        print(
                            f"{file_name} removed successfully from {dir_name}.")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
                        return False
                else:
                    print(f"The file {file_path} does not exist ...")
                return True
            except Exception as e:
                print(f"An error occurred while deleting files: {e}")

            return False

    def delete_files(self, files):
        """
        Delete files from a specified folder.
        :param files: List of file names to delete.
        :return: True if all files were deleted successfully, False otherwise.
        """

        if files:
            try:
                for file in files:
                    if self.check_path(file) == PathChecker.RET_FILE:
                        try:

                            file_name = file.name
                            dir_name = file.parent

                            os.remove(file)
                            print(f"{file_name} removed successfully from {dir_name}")
                        except Exception as e:
                            print(f"Error deleting {file}: {e}")
                            return False
                    else:
                        print(f" The file {file} does not exist in the folder ")
                return True
            except Exception as e:
                print(f"An error occurred while deleting files: {e}")
                return False
        else:
            return False

    def delete_files_in_directory(self, folder_path):
        """
            delte all files in a directory
        :param folder_path: --> Path Object
        :return:
        """
        if self.check_path(folder_path) == PathChecker.RET_DIR:
            # files = os.listdir(folder_path)
            files = self.get_filelist_indir(folder_path)
            print(f"delete_files_in_directory - {files}")
            self.delete_files(files)
            return True
        else:
            print(f"delete_files_in_directory: {folder_path} its not a directory")
            return False

    def erase_all_yangsoo_test_files(self, directory):
        files = self.get_filelist_indir(directory)

        for filename in files:
            try:
                # Check if it's a file (and not a directory)
                if os.path.isfile(filename) or os.path.islink(filename):
                    os.unlink(filename)  # Remove the file
                # If it's a directory, use shutil.rmtree to remove it
                elif os.path.isdir(filename):
                    shutil.rmtree(filename)
            except Exception as e:
                print(f'Failed to delete {filename}. Reason: {e}')

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
            initial_dir = self.send

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

        if isinstance(folder_path, Path):
            posix_path = folder_path.as_posix()
            if posix_path == ".":
                folder_path = str(folder_path.cwd())

        source = Path(folder_path)

        if self.check_path(source) == PathChecker.RET_DIR:
            source = os.path.join(folder_path, file_name)

        print(' join_path: ', source)
        return source

    def unfold_path(self, folder_path):
        """
            폴더패스를 분리해서, 리스트로 반환
            ['D:', '09_hardRain', '09_ihanseol - 2024', '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청']
        """

        if not self.check_path(folder_path):
            folder_path = self.send

        if isinstance(folder_path, Path):
            posix_path = folder_path.as_posix()
            if posix_path == ".":
                folder_path = str(folder_path.cwd())

        parts = folder_path.split('\\')
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


def main_test1():
    fb = FileBase()
    file_list = fb.get_file_filter(".", "*.hwp*")
    if file_list:
        print(file_list)
    else:
        exit()

    fb.line_print(' delete left over hwpx files ....')
    for _ in file_list:
        file = fb.send / _
        print(f" file list in main_test1 : {file}")
        fb.delete_file(file)


def main_test2():
    fb = FileBase()
    jpg_files = fb.get_jpg_filter(".", "a1*.jpg")
    n_count = len(jpg_files)
    print("length of jpg_files:", len(jpg_files))
    if n_count == 4:
        print("-- include dangye --")
    else:
        print("-- exclude dangye --")

    jpg_files = fb.get_jpg_filter(".", "a*.jpg")
    last = ''.join(jpg_files[-1:])
    well = int(last[1])

    print("last :", well)


def main_test3():
    fb = FileBase()
    # fb.delete_files_in_directory(Path.cwd())

    # print(fb.list_non_hidden_directories(Path('d:/')))
    # print(fb.list_non_hidden_directories(Path(".")))
    # print(fb.list_hidden_directories(Path('d:/05_Send')))
    # print(fb.list_directory_contents(Path(".")))

    # print(fb.list_directories_only(Path(".")))
    # print(fb.get_dirname(Path(r'd:\05_Send\05_수질성적서 왁구 - 30공까지.hwpx')))
    # print(fb.get_basename(Path(r'd:\05_Send\05_수질성적서 왁구 - 30공까지.hwpx')))
    # print(fb.is_exist(Path(r'd:\05_Send\05_수질성적서 왁구 - 30공까지.hwpx')))
    # print(fb.is_exist(r'd:\05_Send\05_수질성적서 왁구 - 30공까지.hwpx'))
    # fb.copy_file(Path(r'd:\05_Send\05_수질성적서 왁구 - 30공까지.hwpx'), Path('c:/Temp'))

    # print(fb.unfold_path(Path(".")))
    # print(fb.join_path_tofilename(Path("."), Path("05_수질성적서 왁구 - 30공까지.hwpx")))
    print(fb.get_xlsm_files())
    print(fb.last_one(Path(r'd:\05_Send\A2_ge_OriginalSaveFile.xlsm')))


if __name__ == "__main__":
    main_test3()
