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

from .FileManager import FileBase
from .AqtProjectInfoInjector import AqtProjectInfoInjector


class AqtExcelProjectInfoInjector(AqtProjectInfoInjector):
    def __init__(self, directory, company):
        super().__init__(directory, company)
        # self.df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
        self.df = pd.DataFrame()
        self.fb = FileBase()
        self.project_name = ''
        self.is_jiyeol = False  # 지열공이면, 단계파일을 포함해서 해야해서 ...

    def set_dataframe(self, df):
        self.df = df
        self.project_name = self.df.loc[0, 'Project Name']
        self.is_jiyeol = True if ('지열' in self.project_name) else False

    def get_gong_n_address(self, row_index):
        """
            줄번호, row_index 를 받아서
            그 해당하는 인덱스의 공번, 주소를 리턴
        """

        if self.df.empty and self.is_exist(r"d:\05_Send\YanSoo_Spec.xlsx"):
            df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
            self.set_dataframe(df)

        try:
            row_data = self.df.loc[row_index - 1]
            str_gong = row_data['gong']
            address = row_data['address']
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

    """
        2025/4/9 6:58 오후
        Excel File, 'Yansoo_Spec.xlsx' 로 처리할때는, 회사명과 주소를 엑셀파일에서 찾는것으로 수정
        def process_projectinfo_byexcel(self, company, address):
    """

    def process_projectinfo_byexcel(self, addOne=False):

        # if self.df.empty and self.is_exist(r"d:\05_Send\YanSoo_Spec.xlsx"):
        if self.is_exist(r"d:\05_Send\YanSoo_Spec.xlsx"):
            df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
            self.set_dataframe(df)

        company = self.df.loc[0, 'Company']
        address = self.df.loc[0, 'address']

        self.set_company(company)
        self.set_address(address)
        self.change_aqt_filename()

        send_list = self.get_wellno_list_insend()
        xlsx_list = self.get_gong_list()

        difference_set = list(set(send_list) - set(xlsx_list))
        if difference_set:
            self.delete_difference(difference_set)

        # aqtfiles = natsorted([f for f in os.listdir() if f.endswith('.aqt')])
        aqtfiles = self.get_aqt_files()
        print(f'aqtfiles: {aqtfiles}')
        # self.block_user_input()

        for i in xlsx_list:
            if addOne:
                gong, excel_address = self.get_gong_n_address(1)
            else:
                gong, excel_address = self.get_gong_n_address(i)

            """
               여기에서, 공번과, 주소를 가져오는데
               더힐CC 처럼 , 마지막에 공번 4를 하나 추가하려면
               가져오질 못한다. 없으니까 ....
            """

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
