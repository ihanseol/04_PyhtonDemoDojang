"""
    # *************************************************************************
    # 그리고 리팩토
    # *************************************************************************
"""

import win32com.client as win32
import time
import pandas as pd
import re
import os
import random
from natsort import natsorted
import pyautogui
import pygetwindow as gw
import pytz
from datetime import datetime, timedelta
from typing import Any
import tkinter as tk
from tkinter import scrolledtext
from move_window_to_second_monitor import SimpleWindowMover




# Create a dictionary based on the table
table_data = {
    60: 17,
    75: 18,
    90: 19,
    105: 20,
    120: 21,
    140: 22,
    160: 23,
    180: 24,
    240: 25,
    300: 26,
    360: 27,
    420: 28,
    480: 29,
    540: 30,
    600: 31,
    660: 32,
    720: 33,
    780: 34,
    840: 35,
    900: 36,
    960: 37,
    1020: 38,
    1080: 39,
    1140: 40,
    1200: 41,
    1260: 42,
    1320: 43,
    1380: 44,
    1440: 45,
    1500: 46,
}


def get_mytime_from_table(stabletime):
    # Return the corresponding MY_TIME for the given STABLETIME
    return table_data.get(stabletime, "STABLETIME not found")


class YangSooInjector:
    INPUT_COLUMNS = [
        'gong', 'address', 'hp', 'pump_simdo', 'pumping_capacity', 'casing', 'well_diameter', 'simdo', 'q', 'natural',
        'stable', 'Project Name', 'Jigu Name', 'Company', 'stable_time', 'longterm_test_time', 'bedrock', 'ph'
    ]

    def __init__(self, directory, text_widget):
        self.directory = directory
        # self.spec_file = spec_file
        self.text_widget = text_widget

        try:
            self.df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
        except Exception as e:
            self.printinfo(f" YanSoo.xlsx Not Found - {e}")

        # self.df = pd.read_excel(spec_file)
        self.isOLD = True
        self.debug_yes = True
        self.STABLE_TIME = 0
        self.LONG_TERM_TEST_TIME = pd.Timestamp('2024-06-29 15:45:09')
        '''
                    여기서, 안정수위 도달시간 stable_time = 0 이면
                    이것은, 자동으로 처리한다는 의미이다.        
        '''

        self.yangsoo_files = []
        """
            yangsoo_files = ge_Original_SaveFiles
        """

    def printinfo(self, *args, **kwargs):
        """Print function that outputs to the text widget instead of console."""
        message = ' '.join(map(str, args))
        if kwargs:
            message += ' ' + ' '.join(f'{k}={v}' for k, v in kwargs.items())
        self.text_widget.insert(tk.END, message + '\n')
        self.text_widget.see(tk.END)
        self.text_widget.update()

    def countdown(self, n):
        self.printinfo(' Please Move the Command Window to Side ! ')
        while n > 0:
            self.printinfo(n)
            time.sleep(1)
            n -= 1
        self.printinfo("Time's up!")

    @staticmethod
    def extract_number(s):
        return int(re.findall(r'\d+', s)[0])

    def click_excel_button(self, ws, button_name):

        """
            def click_button():
                for i in range(1, ws.OLEObjects().Count + 1):
                    obj = ws.OLEObjects().Item(i)
                    if obj.Name == button_name:
                        obj.Object.Value = True
                        return True
                return False
        """

        def click_button():
            for obj in ws.OLEObjects():
                if obj.Name == button_name:
                    obj.Object.Value = True
                    return True
            return False

        while True:
            try:
                if not click_button(): return False
                break  # Exit the loop if no exception is raised
            except Exception as e:
                self.printinfo(f" {ws} - {button_name} : Error in Button Click Function {e}")
                time.sleep(1)  # Optional: Wait a bit before retrying
            finally:
                self.change_window('EXCEL')
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)

        return True

    def click_excel_buttons(self, ws, button_names):
        check = False
        for button_name in button_names:
            check = self.click_excel_button(ws, button_name)
            if not check:
                self.printinfo(f" {button_name} Not Found ...")
            else:
                self.printinfo(f" Button Click Function {button_name}")
        return check

    @staticmethod
    def isit_oldversion(ws, button_name):
        """
        :param ws:
        :param button_name:
        :return:
            button_name found is ws then this is True

        """
        for obj in ws.OLEObjects():
            if obj.Name == button_name:
                return False
        return True

    def get_excel_row(self, row_index):
        try:
            r_value = self.df.loc[row_index]
        except IndexError:
            return None

        return r_value

    def parse_and_adjust_timestamp(self, timestamp_str):
        """ Parse, localize to Seoul timezone, and add seconds to a timestamp string. """
        try:
            # Convert the string to a pandas Timestamp
            timestamp = pd.Timestamp(timestamp_str)

            # Localize to Seoul timezone if it is naive
            if timestamp.tzinfo is None:
                # seoul_tz = pytz.timezone('Asia/Seoul')
                # timestamp = timestamp.tz_localize(seoul_tz)
                timestamp = timestamp.tz_localize('UTC')

            # Add 10 seconds to the timestamp
            timestamp += timedelta(seconds=10)

            return timestamp
        except Exception as e:
            self.printinfo(f" Error parsing, localizing, and adjusting timestamp: {e}")
            return None  # Handle this appropriately in your code

    def make_cell_values(self, row_index):
        if len(self.yangsoo_files) == 1:
            row_data = self.get_excel_row(0)
            """
                yangsoo_files가 한개밖에 없으면
                더힐CC처럼 , 공 하나가 추가되어
                이것만 처리해야 할경우
            """
        else:
            row_data = self.get_excel_row(row_index)

        len_row_data = len(row_data)
        self.printinfo(f' len(row_data): {len_row_data}')

        # address, hp, casing, well_rad, simdo, q, natural, stable = row_data[1:9]

        address = row_data['address']
        hp = row_data['hp']
        casing = row_data['casing']
        well_rad = row_data['well_diameter']
        simdo = row_data['simdo']
        q = row_data['q']
        natural = row_data['natural']
        stable = row_data['stable']

        project_name = jigu_name = company_name = ''
        ph = 7.0

        self.STABLE_TIME = row_data['stable_time']

        self.printinfo(f' time stamp of longtest_time : {row_data["longterm_test_time"]}')
        # self.LONG_TERM_TEST_TIME = self.parse_and_adjust_timestamp(row_data[13])

        # Fixed: Check if timestamp exists and handle timezone properly
        longterm_time = row_data['longterm_test_time']

        try:
            if pd.isna(longterm_time):
                # If no timestamp provided, use a default
                self.LONG_TERM_TEST_TIME = pd.Timestamp('2024-06-29 15:45:09')
            else:
                # Convert to Timestamp if it's not already
                if not isinstance(longterm_time, pd.Timestamp):
                    longterm_time = pd.Timestamp(longterm_time)

                # Remove timezone info if it exists to avoid localization issues
                if longterm_time.tzinfo is not None:
                    self.LONG_TERM_TEST_TIME = longterm_time.tz_localize(None)
                else:
                    self.LONG_TERM_TEST_TIME = longterm_time
        except Exception as e:
            print(f"Error processing longterm_test_time: {e}")
            # Fallback to default timestamp
            self.LONG_TERM_TEST_TIME = pd.Timestamp('2024-06-29 15:45:09')


        project_name = row_data['Project Name']
        jigu_name = row_data['Jigu Name']
        company_name = row_data['Company']
        pump_simdo = row_data['pump_simdo']
        tochul = row_data['tochul']
        ph = row_data['ph']
        pumping_capacity = row_data['pumping_capacity']
        yangsoo_time = row_data['yangsoo_time']

        # Swap natural and stable if stable is less than natural to prevent errors
        if stable < natural:
            natural, stable = stable, natural

        gong = self.extract_number(row_data['gong'])
        str_gong = f"공  번 : W - {gong}"

        time.sleep(1)

        cell_values = {
            "J48": str_gong,
            "I46": address,
            "I52": casing,
            "I48": hp,
            "M44": well_rad,
            "M45": simdo,
            "M48": natural,
            "M49": stable,
            "M51": q,
            "I50": pump_simdo,
            "K50": tochul,
            "I51": pumping_capacity
        }

        if len_row_data > 9:
            cell_values.update({
                "I44": project_name,
                "I45": jigu_name,
                "I47": company_name,
                "c9": ph,
                "z999": yangsoo_time
            })

        return cell_values

    def inject_value_to_cells(self, book, excel):
        cell_values_string = {
            "J48": "str_gong",
            "I46": "address",
            "I52": "casing",
            "I48": "hp",
            "M44": "well_rad",
            "M45": "simdo",
            "M48": "natural",
            "M49": "stable",
            "M51": "q",
            "I50": "pump_simdo",
            "K50": "tochul",
            "I51": "pumping_capacity",
            "I44": "project_name",
            "I45": "jigu_name",
            "I47": "company_name",
            "c9": "ph",
            "z999": "yangsoo_time"
        }

        sheet = book.Worksheets("Input")
        sheet_w1 = book.Worksheets("w1")

        filename = os.path.basename(book.Name)
        row_index = self.extract_number(filename) - 1
        if self.debug_yes: self.printinfo(' inject value to cell, processing make_cell_values...')

        cell_values = self.make_cell_values(row_index)
        sheet.Range("M49").Value = 300  # 안정수위를 일단 300으로 , 에러를 차단하기 위해서 ...

        if cell_values.get("z999") == 2880:
            excel.Application.Run("mod_INPUT.SetTimeTo2880")
        else:
            excel.Application.Run("mod_INPUT.SetTimeTo1440")

        for cell, value in cell_values.items():
            self.printinfo(f'inject_value_to_cells : {cell} : {cell_values_string.get(cell)}, - {value}')
            if cell != "c9":
                sheet.Range(cell).Value = value
            else:
                sheet_w1.Range(cell).Value = value

            time.sleep(1)

        if self.debug_yes: self.printinfo(' inject value to cell, finished...')

    def inject_values(self, wb, excel):
        if self.debug_yes:
            self.printinfo('='*100)
            self.printinfo(' inject value to cell, _inject_input is started ...')
            self.printinfo('=' * 100)

        self._inject_input(wb, excel)
        self.printinfo('')

        if self.debug_yes:
            self.printinfo('=' * 100)
            self.printinfo(' inject step test ...')
            self.printinfo('=' * 100)
        self._inject_step_test(wb)
        self.printinfo('')

        if self.debug_yes:
            self.printinfo('=' * 100)
            self.printinfo(' inject long term test ...')
            self.printinfo('=' * 100)
        self._inject_long_term_test(wb, excel)
        self.printinfo('')

        if self.debug_yes:
            self.printinfo('=' * 100)
            self.printinfo(' water quality check  ...')
            self.printinfo('=' * 100)
        self._inject_w1_test(wb)

    # 간이양수시험
    # 2025-3-29
    def _inject_w1_test(self, wb):
        ws = wb.Worksheets("w1")
        ws.Activate()
        self.printinfo(" YangSoo Type - New Version")

        temp_ref = [14.8, 14.9, 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7]
        ec_ref = [200, 201, 202, 219, 203, 204, 218, 205, 206, 213, 207, 208, 209, 210, 211, 215, 217]

        temp = random.choice(temp_ref)
        ec = random.choice(ec_ref)

        if self.debug_yes: self.printinfo(f' inject basic Temp : {temp} ...')
        ws.Range("C7").Value = temp
        if self.debug_yes: self.printinfo(f' inject basic EC : {ec} ...')
        ws.Range("C8").Value = ec

        self.printinfo(' Make adjust Value Pressed ... ')
        self.click_excel_button(ws, "CommandButton2")
        time.sleep(1)

    def _inject_input(self, wb, excel):
        ws = wb.Worksheets("Input")
        ws.Activate()
        time.sleep(1)
        self.inject_value_to_cells(wb, excel)

        time.sleep(1)

        self.change_window('EXCEL')
        excel.Application.SendKeys("{PGUP}")
        # excel.ActiveWindow.LargeScroll(Down=-1)

        button_mapping = {
            "old": ["CommandButton2", "CommandButton3", "CommandButton6", "CommandButton1"],
            "new": ["CommandButton_CB1", "CommandButton_CB2", "CommandButton_Chart"]
        }

        if self.isit_oldversion(ws, button_mapping["new"][0]):
            self.isOLD = True
            self.printinfo(" YangSoo Type - Old Version")
            button_set = button_mapping["old"]
            labels = ['SetCB1', 'SetCB2', 'Chart', 'PumpingTest']
        else:
            self.isOLD = False
            self.printinfo(" YangSoo Type - New Version")
            button_set = button_mapping["new"]
            labels = ['SetCB1', 'SetCB2', 'SetChart']

        for button, label in zip(button_set, labels):
            self.click_excel_button(ws, button)
            self.printinfo(f' _inject_input -- {label}')
            time.sleep(1)

    def _inject_step_test(self, wb):
        ws = wb.Worksheets("stepTest")
        ws.Activate()
        time.sleep(1)

        self.printinfo(' _inject_step_test -- FindAnswer Button ')
        self.click_excel_button(ws, "CommandButton1")
        time.sleep(2)

        self.printinfo(' _inject_step_test -- Check Button ')
        self.click_excel_button(ws, "CommandButton2")

    def _inject_long_term_test(self, wb, excel):
        ws = wb.Worksheets("LongTest")
        wskin = wb.Worksheets("SkinFactor")

        ws.Activate()
        values = [540, 600, 660, 720, 780, 840]

        # Clear GoalSeekTarget
        ws.Range("GoalSeekTarget").Value = 0

        selected_value = random.choice(values) if self.STABLE_TIME == 0 else self.STABLE_TIME
        wskin.Range("G16").Value = selected_value

        if self.debug_yes:
            self.printinfo(f' stable time selection ... : {selected_value}')

        actions = [
            {"button": "CommandButton5", "label": "Reset 0.1", "delay": 1},
            {"combo_box": "ComboBox1", "value": selected_value, "delay": 1},
            {"module": ["mod_W1LongtermTEST", "mod_W1_LongtermTEST"], "delay": 1},
            {"button": "CommandButton5", "label": "Reset 0.1", "delay": 1},
            {"button": "CommandButton4", "label": "FindAnswer", "delay": 2},
            {"button": "CommandButton7", "label": "Check", "delay": 0}
        ]

        try:
            if self.LONG_TERM_TEST_TIME is None:
                raise ValueError("LONG_TERM_TEST_TIME is None. Ensure it is properly initialized.")

            ws.Range("C10").Value = self.LONG_TERM_TEST_TIME
        except Exception as e:
            self.printinfo(f" Error assigning timestamp to Excel cell: {e}")

        for action in actions:
            if "button" in action:
                self.printinfo(f' _inject_long_term_test -- {action["label"]}')
                self.click_excel_button(ws, action["button"])
            elif "combo_box" in action:
                ws.OLEObjects(action["combo_box"]).Object.Value = action["value"]
                self.printinfo(f' _inject_long_term_test -- Set ComboBox value to {action["value"]}')
            elif "module" in action:
                self.printinfo(' _inject_long_term_test -- excel.Application.Run("mod_W1LongtermTEST.TimeSetting")')
                self.ExcelApplicationModule(excel, action["module"])
            time.sleep(action["delay"])

    def ExcelApplicationModule(self, excel, module_names):
        if self.isOLD:
            module_name = module_names[0]
        else:
            module_name = module_names[1]

        excel.Application.Run(f"{module_name}.SetMY_TIME")
        excel.Application.Run(f"{module_name}.TimeSetting")

        time.sleep(1)
        self.printinfo(f" Application.Run, {module_name} is running successfully")

    def data_validation(self):
        def collect_ge_original_save_files():
            files = natsorted([f for f in os.listdir() if f.endswith('.xlsm')])
            filtered_files = [f for f in files if "ge_OriginalSaveFile" in f]

            self.yangsoo_files = filtered_files
            return filtered_files

        os.chdir(self.directory)
        yangsoo_files = collect_ge_original_save_files()

        if not yangsoo_files:
            self.printinfo(" No YangSoo .xlsm files found.")
            return None

        last_file = yangsoo_files[-1]
        row_index = self.extract_number(last_file) - 1

        if len(yangsoo_files) == 1:
            check = self.get_excel_row(0)
        else:
            check = self.get_excel_row(row_index)

        return yangsoo_files if check is not None else None

    def process_files(self):
        self.countdown(3)
        # self.window_to_secondscreen("YanSoo Injector")

        files = self.data_validation()
        if files is None:
            self.printinfo(" Index Does not have YangSoo file ...")
            return None

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.ScreenUpdating = False

        excel.Visible = True
        excel.WindowState = -4137  # xlMaximizedWindow
        self.change_window('EXCEL')

        for file in files:
            if self.debug_yes: self.printinfo(f' Processing file:  {file}')
            wb = excel.Workbooks.Open(self.directory + file)

            self.printinfo('\n\n')
            self.printinfo('=' * 100)
            self.printinfo(f'  Processing file: {file}')
            self.printinfo('=' * 100)

            self.inject_values(wb, excel)
            wb.Close(SaveChanges=True)

        excel.ScreenUpdating = True
        excel.Quit()
        if self.debug_yes: self.printinfo('All files processed.')

    def change_window(self, name_title) -> None:
        gwindows = gw.getWindowsWithTitle(name_title)

        if gwindows:
            window = gwindows[0]
            window.activate()
            if not window.isMaximized:
                window.maximize()
        else:
            self.printinfo(f"  No  {name_title} found.")

    def window_to_secondscreen(self, name_title) -> None:
        gwindows = gw.getWindowsWithTitle(name_title)

        if gwindows:
            window = gwindows[0]
            window.activate()
            pyautogui.hotkey('win', 'shift', 'right')
        else:
            self.printinfo(f" No {name_title} found.")

    def initial_delete_output_file(self, folder_path):
        files = os.listdir(folder_path)
        xlsm_files = [f for f in files if f.endswith('.xlsm')]

        for file in xlsm_files:
            file_path = os.path.join(folder_path, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                self.printinfo(f" {file} has been removed successfully.")
            else:
                self.printinfo(f" The file {file} does not exist in the folder {folder_path}.")



def run_main():
    root = tk.Tk()
    root.title("YanSoo Injector")
    root.geometry("1200x700")  # Initial size, but will expand

    # Create a scrolled text widget that fills the entire window
    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=40, font=('Consolas', 11))
    text_widget.pack(fill=tk.BOTH, expand=True)

    # Initialize injector with text widget
    injector = YangSooInjector("d:\\05_Send\\", text_widget)
    injector.initial_delete_output_file(r"c:/Users/minhwasoo/Documents/")
    injector.process_files()

    # Keep the window open
    root.mainloop()





if __name__ == "__main__":
    # main()
    run_main()