import os
import shutil
import fnmatch
from natsort import natsorted
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime


class AQTBASE:
    def __init__(self):
        self.AQTESOLV_PATH = 'C:\\WHPA\\AQTEver3.4(170414)\\AQTW32.EXE'
        self.DOCUMENTS = os.path.expanduser("~\\Documents")
        self.SEND = 'D:\\05_Send\\'
        self.SEND2 = 'D:\\06_Send2\\'

        self.YANGSOO_EXCEL = "A1_ge_OriginalSaveFile.xlsm"
        self.YANGSOO_REST = "_ge_OriginalSaveFile.xlsm"
        self.YANSOO_SPEC = "d:\\05_Send\\YanSoo_Spec.xlsx"
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
    def __init__(self, directory='D:\\05_Send\\'):
        AQTBASE.__init__(self)

        if directory is None:
            print('in File Base , directory is None')
            self.directory = self.SEND

        self.files = None

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
    #     if self.check_path(self.directory):
    #         self.files = os.listdir(self.directory)
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
        self.files = os.listdir(self.directory)
        return [f for f in self.files if f.endswith(extension)]

    def get_xlsm_files(self):
        """ Returns a list of .xlsm files. """
        return self._get_files_by_extension('.xlsm')

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
                            f"{self.get_basename(file_path)} has been removed successfully from {self.get_dirname(file_path)}.")
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
                file_path = os.path.join(folder_path, file_name)

                if self.check_path(file_path) == PathChecker.RET_FILE:
                    try:
                        os.remove(file_path)
                        print(f"{file_name} has been removed successfully from {folder_path}")
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
        if self.check_path(folder_path) == PathChecker.RET_DIR:
            files = os.listdir(folder_path)
            print(f"delete_files_in_directory - {files}")
            self.delete_files(folder_path, files)
            return True
        else:
            print(f"delete_files_in_directory: {folder_path} its not a directory")
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

    def initial_set_yangsoo_excel(self):
        """Copy the initial Yangsoo Excel file to the SEND directory."""
        self.copy_file(self.TC_DIR + self.YANGSOO_EXCEL, self.SEND + self.YANGSOO_EXCEL)

    def change_filename(self):
        """
          이것은, AQT 파일에 복사본이 포함되어있을경우
          이 복사본을 제거하고, 다른이름 _01 로 대체하는 함수이다.
        """
        aqtfiles = self.get_aqt_files()

        for filename in aqtfiles:
            name, ext = self.seperate_filename(filename)

            if ext == ".aqt" and "_01" not in name:
                if "- 복사본" in name:
                    new_name = name.replace(" - 복사본", "_01") + ext
                    os.rename(os.path.join(self.SEND, filename), os.path.join(self.SEND, new_name))

                if "- Copy" in name:
                    new_name = name.replace(" - Copy", "_01") + ext
                    os.rename(os.path.join(self.SEND, filename), os.path.join(self.SEND, new_name))

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

    def dir_yangsoo_test(self):
        if self.DIR_YANGSOO_TEST == '':
            self.DIR_YANGSOO_TEST = self.BASEDIR + self.YANGSOO_BASE
        return self.DIR_YANGSOO_TEST

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

    def setBASEDIR(self, directory=''):
        """
          ['D:', '09_hardRain', '09_ihanseol - 2024', '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청']
        :return:
        """

        print('***********')
        print(directory)
        print('***********')

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

    def move_documents_to_ihanseol(self):
        fb = FileBase()
        fb.set_directory(self.DOCUMENTS)

        print(self.DOCUMENTS)

        if self.isDIRSET:
            dat_files = fb.get_dat_files()
            xlsm_files = fb.get_xlsm_files()

            self.print_debug("-")
            print(self.DIR_PRN)
            print(self.DIR_YANGSOO_TEST)
            self.print_debug("-")

            for f in dat_files:
                source = self.join_path(self.DOCUMENTS, f)
                target = self.join_path(self.DIR_PRN, f)
                fb.move_file(source, target)

            for f in xlsm_files:
                source = self.join_path(self.DOCUMENTS, f)
                target = self.join_path(self.DIR_YANGSOO_TEST, f)
                fb.move_file(source, target)

    def move_send_to_ihanseol(self):
        """
            aqt file start with w
            pdf files start with a
            jpg files start with *page1
        """
        fb = FileBase()
        fb.set_directory(self.SEND)

        aqt_files = fb.get_aqt_files()
        pdf_files = fb.get_pdf_files()
        jpg_files = fb.get_jpg_files()

        w_aqtfiles = [f for f in aqt_files if f.startswith('w')]

        a_pdffiles = [f for f in pdf_files if f.startswith('a')]
        w_pdffiles = [f for f in pdf_files if f.startswith('w')]
        p_pdffiles = [f for f in pdf_files if f.startswith('p')]

        jpg_apagefiles = fb.get_jpg_filter(sfilter='a*page*')
        jpg_ppagefiles = fb.get_jpg_filter(sfilter='p*page*')
        jpg_wpagefiles = fb.get_jpg_filter(sfilter='w*page*')

        self.print_debug('-')
        print(w_aqtfiles)
        print(a_pdffiles)
        print(jpg_apagefiles)
        print(jpg_ppagefiles)
        self.print_debug('-')

        if len(a_pdffiles) > 0 and len(jpg_apagefiles) > 0:
            self.erase_all_yangsoo_test_files(self.DIR_AQT)

            print('its a goto \\02_AQTEver3.4(170414)')
            for f in a_pdffiles:
                source = self.join_path(self.SEND, f)
                target = self.join_path(self.DIR_AQT, f)
                fb.move_file(source, target)

            for f in p_pdffiles:
                source = self.join_path(self.SEND, f)
                target = self.join_path(self.DIR_AQT, f)
                fb.move_file(source, target)

            for f in jpg_apagefiles:
                source = self.join_path(self.SEND, f)
                target = self.join_path(self.DIR_AQT, f)
                fb.move_file(source, target)

            for f in jpg_ppagefiles:
                source = self.join_path(self.SEND, f)
                target = self.join_path(self.DIR_AQT, f)
                fb.move_file(source, target)

            for f in w_aqtfiles:
                source = self.join_path(self.SEND, f)
                target = self.join_path(self.DIR_AQT, f)
                fb.move_file(source, target)

        if len(jpg_wpagefiles) > 0 and len(w_pdffiles) > 0:
            self.erase_all_yangsoo_test_files(self.DIR_YANGSOOILBO)
            print('this is goto yangsoo ilbo ')
            for f in jpg_wpagefiles:
                source = self.join_path(self.SEND, f)
                target = self.join_path(self.DIR_YANGSOOILBO, f)
                fb.move_file(source, target)

            for f in w_pdffiles:
                source = self.join_path(self.SEND, f)
                target = self.join_path(self.DIR_YANGSOOILBO, f)
                fb.move_file(source, target)

    def move_send2_to_ihanseol(self):
        """
            aqt file start with w
            pdf files start with a
            jpg files start with *page1
        """
        fb = FileBase()
        fb.set_directory(self.SEND2)

        prn_files = fb.get_prn_files()
        xlsm_files = fb.get_xlsm_files()

        print(prn_files)
        print(xlsm_files)

        if prn_files:
            self.erase_all_yangsoo_test_files(self.DIR_PRN)

        if self.isDIRSET:
            self.print_debug("-")
            print(self.DIR_PRN)
            print(self.DIR_YANGSOO_TEST)
            self.print_debug("-")

            for f in prn_files:
                source = self.join_path(self.SEND2, f)
                target = self.join_path(self.DIR_PRN, f)
                fb.move_file(source, target)

            for f in xlsm_files:
                source = self.join_path(self.SEND2, f)
                target = self.join_path(self.DIR_YANGSOO_TEST, f)
                fb.move_file(source, target)
        else:
            print('self.DIRSET is Empty')

    def erase_all_yangsoo_test_files(self, directory):
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

    def Test(self):
        fb = FileBase()
        fb.set_directory(self.DOCUMENTS)
        print(fb.get_list_files(['.dat', '.xlsm']))


if __name__ == "__main__":
    # fp = PrepareYangsoofile()
    # fp.aqtfile_to_send(well_no=1)
    # fp.duplicate_yangsoo(3)

    tyd = TransferYangSooFile()
    tyd.setBASEDIR()

    # tyd.move_send_to_ihanseol()
    tyd.move_send2_to_ihanseol()

    #
    # tyd.move_documents_to_ihanseol()
    # tyd.Test()
