import os
import shutil
import fnmatch
from natsort import natsorted


class AQTBASE:
    def __init__(self):
        self.AQTESOLV_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
        self.DOCUMENTS = "c:/Users/minhwasoo/Documents/"
        self.SEND = "d:/05_Send/"
        self.SEND2 = "d:/06_Send2/"

        self.YANGSOO_EXCEL = r"A1_ge_OriginalSaveFile.xlsm"
        self.YANGSOO_REST = "_ge_OriginalSaveFile.xlsm"
        self.TC_DIR = "c:/Program Files/totalcmd/AqtSolv/"

        self.STEP_FILE = "_01_step.aqt"
        self.LONG_FILE = "_02_long.aqt"
        self.RECOVER_FILE = "_03_recover.aqt"

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


class FileBase(AQTBASE):
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
        os.chdir(directory)

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
    def get_dirname(file_path) -> str:
        return os.path.dirname(file_path) + "\\"

    @staticmethod
    def get_basename(file_path) -> str:
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

    def copy_file(self, source, destination):
        """
        copy file from source to destination

        :param source:
            source path, including file and dir
        :param destination:
            destination path, including file and dir

        :return:
        """
        try:
            shutil.copy(source, destination)
            print(f"File moved successfully from '{source}' to '{destination}'")
            return True
        except Exception as e:
            print(f"Error copying file: {e}")
            return False

    def move_file(self, source, destination):
        """
        move file source to destination

        :param source:

        :param destination:

        """
        try:
            shutil.move(source, destination)
            print(f"File moved successfully from '{source}' to '{destination}'")
            return True
        except Exception as e:
            print(f"Error moving file: {e}")
            return False

    def delete_files(self, folder_path, files):
        try:
            for file_name in files:
                file_path = os.path.join(folder_path, file_name)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        print(f"{file_name} has been removed successfully from {folder_path}.")
                        return True
                    except Exception as e:
                        print(f"Error {e}")
                        return False
                else:
                    print(f"The file {file_name} does not exist in the folder {folder_path}.")
                    return False
        except Exception as e:
            print(f"An error occurred while deleting files: {e}")
            return False


class FileProcessing(FileBase):
    def __init__(self, directory="d:\\05_Send\\"):
        super().__init__(directory)


    def initial_set_yangsoo(self):
        self.copy_file(self.TC_DIR + self.YANGSOO_EXCEL, self.SEND + self.YANGSOO_EXCEL)

    def aqt_send(self, well_no=1, mod='include'):
        if mod == 'include':
            self.copy_file(self.TC_DIR + self.STEP_FILE, self.SEND + f"w{well_no}" + self.STEP_FILE)
        self.copy_file(self.TC_DIR + self.LONG_FILE, self.SEND + f"w{well_no}" + self.LONG_FILE)
        self.copy_file(self.TC_DIR + self.RECOVER_FILE, self.SEND + f"w{well_no}" + self.RECOVER_FILE)

    def duplicate_yangsoo(self, cnt):
        def duplicate_func(well_no):
            destination_path = os.path.join(self.SEND, f"A{well_no}" + self.YANGSOO_REST)
            shutil.copy(self.SEND+self.YANGSOO_EXCEL, destination_path)
            return destination_path

        self.initial_set_yangsoo()
        for i in range(2, cnt+1):
            duplicate_func(i)


if __name__ == "__main__":
    fp = FileProcessing()
    fp.aqt_send(well_no=1)
    fp.duplicate_yangsoo(3)


