import os
import shutil
import fnmatch
from natsort import natsorted


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


class FileBase(AQTBASE):
    def __init__(self, directory=r'D:\05_Send\\'):
        super().__init__()
        self._directory = directory
        self._set_directory(directory)

    def _set_directory(self, directory):
        """Set the working directory and refresh the file list."""
        self._directory = directory
        os.chdir(self._directory)
        self.files = os.listdir(directory)

    @property
    def directory(self):
        """Getter for the directory."""
        return self._directory

    @directory.setter
    def directory(self, value):
        """Setter for the directory. Refreshes file list if the directory changes."""
        if self._directory != value:
            self._set_directory(value)

    def set_directory(self, directory):
        """Reset the directory and refresh the file list."""
        self._set_directory(directory)

    def _get_files_by_extension(self, extension):
        """Returns a list of files with the specified extension."""
        return [f for f in self.files if f.endswith(extension)]

    def get_xlsm_files(self):
        """Returns a list of .xlsm files."""
        return self._get_files_by_extension('.xlsm')

    def get_aqt_files(self):
        """Returns a list of .aqt files."""
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

    @staticmethod
    def get_dirname(file_path):
        """Return the directory name of the given file path."""
        return os.path.dirname(file_path) + "\\"

    @staticmethod
    def get_basename(file_path):
        """Return the base name of the given file path."""
        return os.path.basename(file_path)

    @staticmethod
    def is_exist(file_path):
        """Check if the file exists."""
        return os.path.exists(file_path)

    @staticmethod
    def copy_file(source, destination):
        """
        Copy a file from source to destination.
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


class FileProcessing(FileBase):
    def __init__(self, directory=r'D:\05_Send\\'):
        super().__init__(directory)

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


if __name__ == "__main__":
    fp = FileProcessing()
    fp.aqt_send(well_no=1)
    fp.duplicate_yangsoo(3)
