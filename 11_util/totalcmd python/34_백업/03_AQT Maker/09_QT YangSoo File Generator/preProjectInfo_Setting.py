import fnmatch
import time
import os
import pyperclip
from pick import pick
import re
from natsort import natsorted
import pyautogui
from FileProcessing_V4_001 import FileBase
import ctypes


class AqtSolveProjectInfoInjector:
    def __init__(self, directory, company):
        self.directory = directory
        self.company = company
        self.debug = True
        self.program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
        self.delay = 0.5
        self.is_aqt_open = False
        self.is_block = True
        self.df = ""
        self.fb = FileBase()

    def open_aqt(self, filename):
        if not self.is_aqt_open:
            os.startfile(self.program_path)
            self.is_aqt_open = True
            time.sleep(self.delay)

        pyautogui.hotkey('ctrl', 'o')
        pyautogui.press('backspace')
        pyautogui.typewrite(self.directory + filename)
        time.sleep(self.delay)
        pyautogui.press('enter')
        time.sleep(self.delay)

    def close_aqt(self):
        if self.is_aqt_open:
            pyautogui.hotkey('ctrl', 's')
            time.sleep(self.delay)
            pyautogui.hotkey('alt', 'f4')
            time.sleep(self.delay)

        self.is_aqt_open = False

    def main_job(self, well, address):
        def enter_project_info():
            pyautogui.hotkey('alt', 'e')
            time.sleep(0.2)
            pyautogui.press('r')

        if self.is_aqt_open:
            time.sleep(0.2)
            pyperclip.copy(self.company)
            enter_project_info()
            pyautogui.hotkey('ctrl', 'v')

            for _ in range(3):
                pyautogui.press('tab')
                time.sleep(0.2)

            pyperclip.copy(address)
            pyautogui.hotkey('ctrl', 'v')

            pyautogui.press('tab')
            pyperclip.copy(well)
            pyautogui.hotkey('ctrl', 'v')

            pyautogui.press('tab')
            pyautogui.hotkey('ctrl', 'v')

            pyautogui.press('enter')
            pyautogui.hotkey('ctrl', 's')
            time.sleep(self.delay)

    @staticmethod
    def process_address(input_str):
        parts = input_str.split()
        i = 0

        for part in parts:
            if part.endswith("읍") or part.endswith("면") or part.endswith("동") or part.endswith("구"):
                break
            i += 1

        result = ' '.join(parts[i:])

        if len(result) > 21:
            result = result.replace('번지', '')

        address_list = result.split()
        filtered_list = [item for item in address_list if not (item.endswith('아파트') or item == ',')]
        address_string = ' '.join(filtered_list)

        return address_string

    @staticmethod
    def extract_number(s):
        return int(re.findall(r'\d+', s)[0])

    def change_aqt_filename(self):
        """
         aqtfile 을 SEND 에서 불러와서
         파일이름중에, 복사본이 있으면, 이것을 바꾸어 준다.
        """

        aqtfiles = self.fb.get_aqt_files()
        for filename in aqtfiles:
            name, ext = self.fb.seperate_filename(filename)

            if ext == ".aqt" and "_01" not in name:
                if "- 복사본" in name:
                    new_name = name.replace(" - 복사본", "_01") + ext
                    os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, new_name))

                if "- Copy" in name:
                    new_name = name.replace(" - Copy", "_01") + ext
                    os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, new_name))

    def get_wellno_list_insend(self):
        """
         Send folder 에 있는 , aqtfiles 의 관정번호를
         set추려서 유닉하게 만든다.
        """
        os.chdir(self.directory)
        aqtfiles = natsorted([f for f in os.listdir() if f.endswith('.aqt')])

        fn_list = []
        for f in aqtfiles:
            num = self.extract_number(f.split('_')[0])
            fn_list.append(num)

        fn_list = list(set(fn_list))
        return fn_list


def main_call(address, company):
    fb = FileBase()
    injector = AqtSolveProjectInfoInjector('d:\\05_Send\\', company)

    print(f'preProjectInfo, address: {address}, company: {company}')
    injector.change_aqt_filename()

    aqtfiles = fb.get_aqt_files()
    print(f'preProjectInfo, aqtfiles: {aqtfiles}')

    if not injector.is_aqt_open:
        if aqtfiles:
            w_list = injector.get_wellno_list_insend()
            print(f'preProjectInfo, w_list: {w_list}')

            for i in w_list:  # maximum well number is 18
                wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")
                if wfiles:
                    for j, file in enumerate(wfiles):
                        print(injector.directory + file)
                        injector.open_aqt(file)
                        injector.main_job(f"W-{i}", address)

                    injector.close_aqt()
                    # 이 오픈과 클로즈의 문제로 인해서, 여러번 실행해야 할경우에, 문제가 발생함
                    # 오픈했던, 그 안에 넣어서 해결함
        else:
            print('preProjectInfo, aqt files does not found ...')
    else:
        injector.is_aqt_open = False

    del injector
    del fb
    time.sleep(0.5)


def main():
    fb = FileBase()

    title = 'Please choose your Company: '
    options = ['SanSu', 'DaeWoong', 'WooKyung', 'HanIL', 'DongHae', 'HyunYoon', 'JunIL', 'BuYeo', 'TaeYang', 'SamWon',
               'MainGeo']

    MyCompany = ["산수개발(주)", "대웅엔지니어링 주식회사", "(주) 우경엔지니어링", "주식회사 한일지하수", "(주)동해엔지니어링",
                 "(주)현윤이앤씨", "(주) 전일", "부여지하수개발 주식회사", "(주)태양이엔지", "삼원개발(주)", "마인지오 주식회사"]

    option, index = pick(options, title, indicator='==>', default_index=1)
    print(option, index, MyCompany[index])

    address = input('Enter the Company Address :')

    if not address:
        G_ADDRESS = "Empty Address"
    else:
        G_ADDRESS = address

    injector = AqtSolveProjectInfoInjector('d:\\05_Send\\', MyCompany[index])

    user32 = ctypes.windll.user32
    if injector.is_block:
        user32.BlockInput(True)

    files = os.listdir(injector.directory)
    aqtfiles = [f for f in files if f.endswith('.aqt')]

    if aqtfiles:
        w_list = injector.get_wellno_list_insend()
        for i in w_list:  # maximum well number is 18
            wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")
            if wfiles:
                for j, file in enumerate(wfiles):
                    injector.open_aqt(file)
                    injector.main_job(f"W-{i}", G_ADDRESS)

        injector.close_aqt()
    else:
        print('aqt files does not found ...')

    time.sleep(0.5)

    if injector.is_block:
        user32.BlockInput(False)


if __name__ == "__main__":
    # main()
    # main_call("address", "company")
    main_call("장대동 278-13", "풍년가구")
