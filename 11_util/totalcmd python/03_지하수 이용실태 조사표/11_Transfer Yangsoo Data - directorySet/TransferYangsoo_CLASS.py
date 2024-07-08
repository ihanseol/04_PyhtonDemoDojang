
from datetime import datetime
import os

from FileProcessing_V4_20240708 import FileBase
from FileProcessing_V4_20240708 import PathChecker


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

                self.DIR_PRN = self.join_path_from_list([self.BASEDIR, '\\', arg_01])
                self.DIR_AQT = self.join_path_from_list([self.BASEDIR, '\\', arg_02])
                self.DIR_YANGSOOILBO = self.join_path_from_list([self.BASEDIR, '\\', arg_03])
            else:
                os.chdir(self.DIR_YANGSOO_TEST)
                self.print_debug(self.dir_prn())
                self.print_debug(self.dir_aqt())
                self.print_debug(self.dir_yangsoo_ilbo())

    def setBASEDIR(self, directory=''):
        """
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

    def move_documents_to_ihanseol(self):
        fb = FileBase()
        fb.set_directory(self.DOCUMENTS)

        print(self.DOCUMENTS)

        if self.isDIRSET:
            file_mappings = {
                "dat": (fb.get_dat_files(), self.DIR_PRN),
                "xlsm": (fb.get_xlsm_files(), self.DIR_YANGSOO_TEST),
            }

            self.print_debug("-")
            print(self.DIR_PRN)
            print(self.DIR_YANGSOO_TEST)
            self.print_debug("-")

            for file_type, (files, target_directory) in file_mappings.items():
                for f in files:
                    source = self.join_path_tofilename(self.DOCUMENTS, f)
                    target = self.join_path_tofilename(target_directory, f)
                    fb.move_file(source, target)

    def move_send_to_ihanseol(self):
        """
        Move files based on specific start patterns.
        - aqt files start with 'w'
        - pdf files start with 'a', 'w', or 'p'
        - jpg files start with '*page1'
        """
        fb = FileBase()
        fb.set_directory(self.SEND)

        # Get the initial lists of files
        file_mappings = {
            'aqt': fb.get_aqt_files(),
            'pdf': fb.get_pdf_files(),
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
            'jpg_w': file_mappings['jpg_w']
        }

        self.print_debug('-')
        for key, files in filtered_files.items():
            print(f"{key}: {files}")
        self.print_debug('-')

        # Move files to the respective directories
        if filtered_files['a_pdf'] and filtered_files['jpg_a']:
            self._move_files_to_dir(filtered_files, ['a_pdf', 'p_pdf', 'jpg_a', 'jpg_p', 'w_aqt'], self.DIR_AQT,
                                    "02_AQTEver3.4(170414)")

        if filtered_files['jpg_w'] and filtered_files['w_pdf']:
            self._move_files_to_dir(filtered_files, ['jpg_w', 'w_pdf'], self.DIR_YANGSOOILBO, "yangsoo ilbo")

    def _move_files_to_dir(self, filtered_files, keys, target_directory, debug_message):
        fb = FileBase()
        self.erase_all_yangsoo_test_files(target_directory)
        print(f'this is goto {debug_message}')
        for key in keys:
            for f in filtered_files[key]:
                source = self.join_path_tofilename(self.SEND, f)
                target = self.join_path_tofilename(target_directory, f)
                fb.move_file(source, target)

    def move_send2_to_ihanseol(self):
        """
        Handles the movement of files based on their extensions and starting characters:
        - .aqt files start with 'w'
        - .pdf files start with 'a'
        - .jpg files start with '*page1'
        """
        fb = FileBase()
        fb.set_directory(self.SEND2)

        # Retrieve different types of files
        file_types = {
            "prn_files": fb.get_prn_files(),
            "xlsm_files": fb.get_xlsm_files(),
            "aqt_files": fb.get_aqt_files(),
            "xlsx_files": fb.get_xlsx_files()
        }

        print(file_types["prn_files"])
        print(file_types["xlsm_files"])

        if file_types["prn_files"]:
            self.erase_all_yangsoo_test_files(self.DIR_PRN)

        if self.isDIRSET:
            self.print_debug("-")
            print(self.DIR_PRN)
            print(self.DIR_YANGSOO_TEST)
            self.print_debug("-")

            # Define target directories for different file types
            target_directories = {
                "prn_files": self.DIR_PRN,
                "xlsm_files": self.DIR_YANGSOO_TEST,
                "xlsx_files": self.DIR_YANGSOO_TEST,
                "aqt_files": self.DIR_AQT
            }

            for file_type, files in file_types.items():
                target_dir = target_directories[file_type]
                for f in files:
                    source = self.join_path_tofilename(self.SEND2, f)
                    target = self.join_path_tofilename(target_dir, f)
                    fb.move_file(source, target)
        else:
            print('self.DIRSET is Empty')

    def Test(self):
        fb = FileBase()
        fb.set_directory(self.DOCUMENTS)
        print(fb.get_list_files(['.dat', '.xlsm']))
