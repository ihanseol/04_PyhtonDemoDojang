
import time
import re
import os
import shutil
import fnmatch
import ctypes
from natsort import natsorted
import pyautogui
import pygetwindow as gw
import Get_TS_from_AQTESOLV_OCR_CLASS_VERSION as GetTS
import win32com.client as win32


class AQTBASE:
    def __init__(self):
        self.AQTESOLV_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
        self.DOCUMENTS = "c:\\Users\\minhwasoo\\Documents\\"
        self.SEND = "d:\\05_Send\\"
        self.SEND2 = "d:\\06_Send2\\"
        self.ISAQTOPEN = False
        self.DEBUG_YES = True
        self.DELAY = 0.5
        self.IS_BLOCK = False
        """
        self.IS_BLOCK = False :
         because while run the program cause block or wait for user input
         then cann't do anything
         so it must be False, userinput allowed ...
        """


class FileProcessing(AQTBASE):
    def __init__(self, directory="d:\\05_Send\\"):
        super().__init__()
        self._directory = directory
        os.chdir(self._directory)
        self.files = os.listdir(directory)

    @property
    def directory(self):
        """
        directory , getter ...
        :return:
        """
        return self._directory

    @directory.setter
    def directory(self, value) -> None:
        """
        directory , setter
        :param value: setting directory to
        :return: void
        """
        if self._directory != value:  # if _directory changed then refresh files
            self._directory = value
            self.files = os.listdir(value)

    def set_directory(self, directory) -> None:
        """
          Reset the value of the internal directory variable
          Accordingly, the value of the file list is also updated.

            directory and files value refresh

        :param directory:
        :return:
        """
        self._directory = directory
        self.files = os.listdir(directory)

    def get_files_by_extension(self, extension):
        """Returns a list of files with the specified extension."""
        return [f for f in self.files if f.endswith(extension)]

    def get_xlsm_files(self):
        """Returns a list of .xlsm files."""
        return self.get_files_by_extension('.xlsm')

    def get_aqt_files(self):
        """Returns a list of .aqt files."""
        return self.get_files_by_extension('.aqt')

    def get_dat_files(self):
        """Returns a list of .dat files."""
        return self.get_files_by_extension('.dat')

    def get_xlsm_filter(self, path="d:\\05_Send\\", sfilter="*_ge_OriginalSaveFile.xlsm") -> list:
        """
        :param sfilter:
        :param path: the directory where the filter will run
        :paramsfilter: string to filter
        :return:
                list of filtered xlsm files

        """

        self.set_directory(path)
        """ 
            set directory to work
            and refresh files : file list in the path
            so xlsm, aqt, dat files retrived ...         
        """
        xl_files = self.get_xlsm_files()

        xlsmfiles = fnmatch.filter(xl_files, sfilter)
        return natsorted(xlsmfiles)

    @staticmethod
    def has_path(file_name) -> bool:
        """
        file_name has path or not
        if file_name include path like c:\\user\\this ...

        :param file_name: filename
        :return:
            head --> file path
            tail --> file
        """
        head, tail = os.path.split(file_name)
        print(f"head :'{head}'  tail : {tail}  includes a path. Performing action...")

        if head:
            return True
        else:
            return False

    @staticmethod
    def separate_path(file_path):
        directory_path = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        return directory_path, base_name

    @staticmethod
    def get_basename_of_path(file_path) -> str:
        return os.path.dirname(file_path) + "\\"

    @staticmethod
    def get_basename_of_file(file_path) -> str:
        return os.path.basename(file_path)

    @staticmethod
    def is_exist(file_path) -> bool:
        """
        is file exisit ... give file_path ...

        :return:
        true --> file exist
        false --> file does not exist

        """
        return os.path.exists(file_path)

    @staticmethod
    def move_file(source, destination) -> None:
        """
        move file source to destination

        :param source:
        :param destination:

        """
        try:
            shutil.move(source, destination)
            print(f"File moved successfully from '{source}' to '{destination}'")
        except Exception as e:
            print(f"Error moving file: {e}")

    @staticmethod
    def delete_files(folder_path, files) -> None:
        try:
            for file_name in files:
                file_path = os.path.join(folder_path, file_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"{file_name} has been removed successfully from {folder_path}.")
                else:
                    print(f"The file {file_name} does not exist in the folder {folder_path}.")
        except Exception as e:
            print(f"An error occurred while deleting files: {e}")

    def duplicate_aqtfile_long(self, well):
        shutil.copyfile(self.SEND + f"w{well}_02_long.aqt", self.SEND + f"w{well}_02_long_01.aqt")

    def after_work(self):
        self.set_directory(self.DOCUMENTS)
        xlsmfiles = self.get_xlsm_files()
        datfiles = self.get_dat_files()

        for file in xlsmfiles:
            self.move_file(self.DOCUMENTS + file, self.SEND2 + file)

        for file in datfiles:
            self.move_file(self.DOCUMENTS + file, self.SEND2 + file)



if __name__ == "__main__":
    file_processing = FileProcessing()
    xlsm_files = file_processing.get_xlsm_filter()
    print(xlsm_files)

