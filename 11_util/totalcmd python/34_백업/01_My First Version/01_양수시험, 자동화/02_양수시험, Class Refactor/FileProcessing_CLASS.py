import time
import re
import os
import shutil
import fnmatch
import ctypes
from natsort import natsorted


class AQTBASE:
    def __init__(self):
        self.AQTESOLV_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
        self.DOCUMENTS = "c:\\Users\\minhwasoo\\Documents\\"
        self.SOURCE = "d:\\05_Send\\"
        self.SEND = "d:\\05_Send\\"
        self.DESTINATION = "d:\\06_Send2\\"
        self.SEND2 = "d:\\06_Send2\\"
        self.ISAQTOPEN = False
        self.DEBUG_YES = False
        self.DELAY = 0.5
        self.IS_BLOCK = False


class FileProcessing(AQTBASE):
    def __init__(self, directory="d:\\05_Send\\"):
        super().__init__()
        self._directory = directory
        os.chdir(self._directory)
        self.files = os.listdir(directory)

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value) -> None:
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
        :param path: the directory where the filter will run
        :paramsfilter: string to filter
        :return:
                list of filtered xlsm files

        """

        self.set_directory(path)
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
        """
        head, tail = os.path.split(file_name)
        if head:
            # print(f"The filename '{tail}' includes a path. Performing action...")
            return True
        else:
            # print(f"The filename '{tail}' does not include a path.")
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

    def delete_files(self, folder_path, files) -> None:
        try:
            if files:
                for file in files:
                    print(file)
                    if self.is_exist(folder_path + file):
                        os.remove(folder_path + file)
                        print(f"{file} has been removed successfully.")
                    else:
                        print(f"The file {file} does not exist in the folder {folder_path}.")
        except Exception as e:
            print(f"Error : {e}")

    def duplicate_aqtfile_long(self, well):
        shutil.copyfile(self.SEND + f"w{well}_02_long.aqt", self.SEND + f"w{well}_02_long_01.aqt")

    def after_work(self):
        self.directory = self.DOCUMENTS
        xlsmfiles = self.get_xlsm_files()
        datfiles = self.get_dat_files()

        for file in xlsmfiles:
            self.move_file(self.DOCUMENTS + file, self.DESTINATION + file)

        for file in datfiles:
            self.move_file(self.DOCUMENTS + file, self.DESTINATION + file)


if __name__ == "__main__":
    file_processing = FileProcessing()
    xlsm_files = file_processing.get_xlsm_filter()
    print(xlsm_files)

