import os
import random
import re
import time

import pandas as pd
import pyautogui
import win32com.client as win32
from natsort import natsorted

# Constants and Configurations
DEBUG_MODE = True
DIRECTORY = "d:\\05_Send\\"
df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")

# Excel Macros
EXCEL_MACROS = {
    "Input": ["CommandButton2", "CommandButton3", "CommandButton6", "CommandButton1"],
    "stepTest": ["CommandButton1", "CommandButton2"],
    "LongTest": ["ComboBox1", "CommandButton5", "CommandButton4", "CommandButton7"]
}


def get_excel_row(df, row_index):
    return df.iloc[row_index, :].tolist()


def extract_number(s):
    return int(re.findall(r'\d+', s)[0])


def inject_value_to_cells(book):
    # cell_values = {"I48": hp, "I52": casing, "M44": well_rad, "M45": simdo, "M48": natural, "M49": stable, "M51": q}

    def make_cell_values(row_index):
        row_data = get_excel_row(df, row_index)

        hp = row_data[1]
        casing = row_data[2]
        well_rad = row_data[3]

        simdo = row_data[4]
        q = row_data[5]
        natural = row_data[6]
        stable = row_data[7]

        gong = extract_number(row_data[0])
        str_gong = f"공  번 : W - {gong}"

        return {"J48": str_gong, "I52": casing, "I48": hp, "M44": well_rad, " M45": simdo, "M48": natural,
                "M49": stable, "M51": q}

    sheet = book.Worksheets("Input")

    filename = os.path.basename(book.Name)
    row_index = extract_number(filename) - 1

    if DEBUG_MODE: print(f'inject value to cell , processing make_cell_values ...')
    cell_values = make_cell_values(row_index)

    for cell, value in cell_values.items():
        sheet.Range(cell).Value = value

    if DEBUG_MODE: print(f'inject value to cell , finished ...')
    return None


def run_excel_macro(excel, wb, macro_name):
    excel.Application.Run("'" + wb.Name + "'!" + macro_name)


def click_excel_button(ws, button_name):
    button = None
    for obj in ws.OLEObjects():
        if obj.Name == button_name:
            button = obj
            break

    # If button is found, click it
    if button:
        button.Object.Value = True


def inject_values_to_sheet(file_name):
    try:
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.ScreenUpdating = False

        wb = excel.Workbooks.Open(file_name)
        excel.Visible = True
        excel.WindowState = -4137  # xlMaximizedWindow

        for sheet_name, buttons in EXCEL_MACROS.items():
            ws = wb.Worksheets(sheet_name)
            ws.Activate()
            time.sleep(1)

            if sheet_name == "Input":
                row_index = extract_number(os.path.basename(file_name)) - 1
                row_data = get_excel_row(df, row_index)
                inject_value_to_cells(ws, row_data)

            for button in buttons:
                click_excel_button(ws, button)
                time.sleep(1)
                if DEBUG_MODE:
                    print(f'{sheet_name}, {button} clicked')

        excel.ScreenUpdating = True
        wb.Close(SaveChanges=True)
        excel.Quit()
        time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")


def initial_delete_output_files():
    folder_path = r"c:/Users/minhwasoo/Documents/"
    xlsmfiles = [f for f in os.listdir(folder_path) if f.endswith('.xlsm')]

    for file in xlsmfiles:
        file_path = os.path.join(folder_path, file)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file} has been removed successfully.")
        else:
            print(f"The file {file} does not exist in the folder {folder_path}.")


def main():
    initial_delete_output_files()
    os.chdir(DIRECTORY)
    xlsmfiles = natsorted([f for f in os.listdir() if f.endswith('.xlsm')])

    for file in xlsmfiles:
        print('Processing file:', file)
        inject_values_to_sheet(os.path.join(DIRECTORY, file))


if __name__ == "__main__":
    main()
