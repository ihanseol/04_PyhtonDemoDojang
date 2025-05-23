import os
import pickle
import ctypes
import shutil
import fnmatch
from natsort import natsorted
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime


class SavedpathClass:
    def __init__(self):
        self.flocation = ''
        self.ls_directory = 'c:\\Program Files\\totalcmd\\AqtSolv\\'

    def SavePath(self, path_data):
        file_path = os.path.join(self.ls_directory, 'SaveFolder.sav')
        os.makedirs(self.ls_directory, exist_ok=True)  # Create the directory if it doesn't exist

        # Define the file path
        file_path = os.path.join(self.ls_directory, 'SaveFolder.sav')
        # Save the data to the file
        with open(file_path, 'wb') as file:
            pickle.dump(path_data, file)

        print(f'File saved to {file_path}')
        self.flocation = path_data

    def LoadPath(self):
        file_path = os.path.join(self.ls_directory, 'SaveFolder.sav')
        with open(file_path, 'rb') as file:
            loaded_data = pickle.load(file)

        print(f'File loaded from {file_path}')
        self.flocation = loaded_data


class AQTBASE:
    def __init__(self):
        self.AQTESOLV_PATH = 'C:\\WHPA\\AQTEver3.4(170414)\\AQTW32.EXE'
        self.DOCUMENTS = os.path.expanduser("~\\Documents")
        self.SEND = 'D:\\05_Send\\'
        self.SEND2 = 'D:\\06_Send2\\'

        self.YANGSOO_EXCEL = "A1_ge_OriginalSaveFile.xlsm"
        self.YANGSOO_REST = "_ge_OriginalSaveFile.xlsm"
        self.TC_DIR = 'C:\\Program Files\\totalcmd\AqtSolv\\'

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
            if message in "*-@#$%&":
                print(message * 180)
            else:
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
        """ Reset the directory and refresh the file list. """
        self._set_directory(directory)

    def _get_files_by_extension(self, extension):
        """ Returns a list of files with the specified extension. """
        return [f for f in self.files if f.endswith(extension)]

    def get_xlsm_files(self):
        """ Returns a list of .xlsm files. """
        return self._get_files_by_extension('.xlsm')

    def get_aqt_files(self):
        """ Returns a list of .aqt files. """
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

        return [dir for dir in dir_non_hidden if dir not in dir_hidden]
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

    def last_one(self, path):
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
            if os.path.exists(destination):
                os.remove(destination)
                print(f'Removed existing file: {destination}')

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


    def join_path(self, folder_path, file_name):
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
            # self.DIR_YANGSOO_TEST = self.BASEDIR + self.YANGSOO_BASE
            self.DIR_YANGSOO_TEST = self.BASEDIR + self.YANGSOO_BASE

        source = self.DIR_YANGSOO_TEST
        self.DIR_YANGSOO_TEST = source.replace("/", "\\")
        return self.DIR_YANGSOO_TEST

    def dir_prn(self):
        if self.DIR_PRN == '':
            self.DIR_PRN = self.BASEDIR + self.YANGSOO_BASE + self.PRN_BASE

        source = self.DIR_PRN
        self.DIR_PRN = source.replace("/", "\\")
        return self.DIR_PRN

    def dir_aqt(self):
        if self.DIR_AQT == '':
            self.DIR_AQT = self.BASEDIR + self.YANGSOO_BASE + self.AQT_BASE

        source = self.DIR_AQT
        self.DIR_AQT = source.replace("/", "\\")
        return self.DIR_AQT

    def dir_yangsoo_ilbo(self):
        if self.DIR_YANGSOOILBO == '':
            self.DIR_YANGSOOILBO = self.BASEDIR + self.YANGSOO_BASE + self.YANGSOOILBO_BASE

        source = self.DIR_YANGSOOILBO
        self.DIR_YANGSOOILBO = source.replace("/", "\\")
        return self.DIR_YANGSOOILBO

    def setBASEDIR(self, directory=''):
        """
          ['D:', '09_hardRain', '09_ihanseol - 2024', '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청']
        :return:
        """
        # spc = SavedpathClass()
        # spc.LoadPath()

        print('***********')
        print(directory)
        print('***********')

        current_year = datetime.now().year

        if directory != '' and self.check_path(directory) == PathChecker.RET_DIR:
            self.BASEDIR = directory
        else:
            sel_folder = self.select_folder(f'd:\\09_hardRain\\09_ihanseol - {current_year}\\')
            sel_folder = self.isit_yangsoo_folder(sel_folder)
            self.BASEDIR = sel_folder

        if self.isit_yangsoo_inside(self.BASEDIR):
            self.print_debug("it has yangsoo inside ... ")
            self.isDIRSET = True
        else:
            self.print_debug("its not contain yangsoo folder ...")
            self.isDIRSET = False
            return "FALSE"

        self.print_debug("*")
        self.print_debug(self.BASEDIR)
        self.print_debug(self.dir_yangsoo_test())
        self.print_debug(self.dir_prn())
        self.print_debug(self.dir_aqt())
        self.print_debug(self.dir_yangsoo_ilbo())
        self.print_debug("*")

        if not self.isDIRSET:
            self.isDIRSET = True

        return self.BASEDIR

    def transfer_files(self, files, source_folder, target_folder):
        for f in files:
            source = self.join_path(source_folder, f)
            target = self.join_path(target_folder, f)
            self.move_file(source, target)

    def move_documents_to_ihanseol(self):
        self.set_directory(self.DOCUMENTS)
        print(self.DOCUMENTS)

        if self.isDIRSET:
            dat_files = self.get_dat_files()
            xlsm_files = self.get_xlsm_files()

            self.print_debug("-")
            print(self.DIR_PRN)
            print(self.DIR_YANGSOO_TEST)
            self.print_debug("-")

            self.transfer_files(dat_files, self.DOCUMENTS, self.DIR_PRN)
            self.transfer_files(xlsm_files, self.DOCUMENTS, self.DIR_YANGSOO_TEST)

    def move_send_to_ihanseol(self):
        """
            aqt file start with w
            pdf files start with a
            jpg files start with *page1
        """
        self.set_directory(self.SEND)

        aqt_files = self.get_aqt_files()
        pdf_files = self.get_pdf_files()
        jpg_files = self.get_jpg_files()

        a_pdffiles = [f for f in pdf_files if f.startswith('a')]
        w_pdffiles = [f for f in pdf_files if f.startswith('w')]
        p_pdffiles = [f for f in pdf_files if f.startswith('p')]

        jpg_apagefiles = self.get_jpg_filter(sfilter='a*page*')
        jpg_ppagefiles = self.get_jpg_filter(sfilter='p*page*')
        jpg_wpagefiles = self.get_jpg_filter(sfilter='w*page*')

        self.print_debug('-')
        print('aqtfiles:', aqt_files)
        print('a_pdffiles:', a_pdffiles)
        print('jpg_apagefiles:', jpg_apagefiles)
        print('jpg_ppagefiles:', jpg_ppagefiles)
        self.print_debug('-')

        if len(a_pdffiles) > 0 and len(jpg_apagefiles) > 0:
            self.erase_all_yangsoo_test_files(self.DIR_AQT)
            print('its a goto \\02_AQTEver3.4(170414)')
            self.transfer_files(a_pdffiles, self.SEND, self.DIR_AQT)
            self.transfer_files(p_pdffiles, self.SEND, self.DIR_AQT)
            self.transfer_files(jpg_apagefiles, self.SEND, self.DIR_AQT)
            self.transfer_files(jpg_ppagefiles, self.SEND, self.DIR_AQT)
            self.transfer_files(aqt_files, self.SEND, self.DIR_AQT)

        if len(jpg_wpagefiles) > 0 and len(w_pdffiles) > 0:
            self.erase_all_yangsoo_test_files(self.DIR_YANGSOOILBO)
            print('this is goto yangsoo ilbo ')
            self.transfer_files(jpg_wpagefiles, self.SEND, self.DIR_YANGSOOILBO)
            self.transfer_files(w_pdffiles, self.SEND, self.DIR_YANGSOOILBO)

    def move_send2_to_ihanseol(self):
        """
            aqt file start with w
            pdf files start with a
            jpg files start with *page1
        """
        self.set_directory(self.SEND2)

        prn_files = self.get_prn_files()
        xlsm_files = self.get_xlsm_files()
        aqt_files = self.get_aqt_files()

        print('prn_files:', prn_files)
        print('xlsm_files:', xlsm_files)
        print('aqt_files:', aqt_files)

        if prn_files:
            self.erase_all_yangsoo_test_files(self.DIR_PRN)

        if self.isDIRSET:
            self.print_debug("-")
            print(self.DIR_PRN)
            print(self.DIR_YANGSOO_TEST)
            self.print_debug("-")

            self.transfer_files(prn_files, self.SEND2, self.DIR_PRN)
            self.transfer_files(xlsm_files, self.SEND2, self.DIR_YANGSOO_TEST)
            self.transfer_files(aqt_files, self.SEND2, self.DIR_AQT)
        else:
            print('self.DIRSET is Empty')

    @staticmethod
    def erase_all_yangsoo_test_files(directory):
        # if self.ask_yes_no_question(directory):

        directory = directory.replace("\\", "/")

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

    def Test(self):
        fb = FileBase()
        fb.set_directory(self.DOCUMENTS)
        ret = fb.list_non_hidden_directories(self.DOCUMENTS)
        print(ret)
        ret = fb.list_hidden_directories(self.DOCUMENTS)
        print(ret)
        print(fb.list_directories_only(self.DOCUMENTS))

        # print(fb.get_list_files(['.dat', '.xlsm']))


if __name__ == "__main__":
    # fp = PrepareYangsoofile()
    # fp.aqtfile_to_send(well_no=1)
    # fp.duplicate_yangsoo(3)

    tyd = TransferYangSooFile()
    ret = tyd.setBASEDIR()
    print(ret)

    # tyd.move_send_to_ihanseol()
    # tyd.move_send2_to_ihanseol()

    #
    # tyd.move_documents_to_ihanseol()
    # tyd.Test()
