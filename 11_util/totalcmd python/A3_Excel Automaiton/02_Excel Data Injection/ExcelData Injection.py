import win32com.client
import win32com.client as win32
import time
import pandas as pd
import re
import os
from natsort import natsorted

DIRECTORY = "d:\\05_Send\\"
df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
DEBUG_YES = False


def get_excel_row(df, row_index):
    result = []
    result = df.iloc[row_index, :].tolist()
    return result


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
    cell_values = make_cell_values(row_index)

    for cell, value in cell_values.items():
        sheet.Range(cell).Value = value

    book.SaveAs("out_" + filename)
    return None


def run_excel_macro(excel, wb, macro_name):
    excel.Application.Run("'" + wb.Name + "'!" + macro_name)
    return None


def click_excel_button(ws, button_name):
    button = None
    for obj in ws.OLEObjects():
        if obj.Name == button_name:
            button = obj
            break

    # If button is found, click it
    if button:
        button.Object.Value = True


def inject_value_to_sheet(file_name):
    try:
        # excel = win32com.client.Dispatch("Excel.Application")
        # excel = win32com.client.gencache.EnsureDispatch("Excel.Application")

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        # excel = win32.Dispatch('Excel.Application')

        excel.ScreenUpdating = False
        wb = excel.Workbooks.Open(file_name)
        excel.Visible = True

        ws = wb.Worksheets("Input")
        ws.Activate()

        inject_value_to_cells(wb)
        if DEBUG_YES: print('inject value to cell')

        click_excel_button(ws, "CommandButton2")
        if DEBUG_YES: print('Input, Button2')
        time.sleep(1)
        click_excel_button(ws, "CommandButton3")
        if DEBUG_YES: print('Input, Button3')
        time.sleep(1)
        click_excel_button(ws, "CommandButton6")
        if DEBUG_YES: print('Input, Button6')
        time.sleep(1)

        # StepTest Fit
        ws = wb.Worksheets("stepTest")
        ws.Activate()

        time.sleep(1)

        click_excel_button(ws, "CommandButton1")
        if DEBUG_YES: print('Step, Button1')
        time.sleep(2)
        click_excel_button(ws, "CommandButton2")
        if DEBUG_YES: print('Step, Button2')
        time.sleep(1)

        # LongTermTes
        ws = wb.Worksheets("LongTest")
        ws.Activate()

        time.sleep(1)
        click_excel_button(ws, "CommandButton5")
        if DEBUG_YES: print('Long, Button5')
        time.sleep(2)
        click_excel_button(ws, "CommandButton4")
        if DEBUG_YES: print('Long, Button5')
        time.sleep(1)
        click_excel_button(ws, "CommandButton7")
        if DEBUG_YES: print('Long, Button7')

        excel.ScreenUpdating = True
        sheet = None
        wb.Close(SaveChanges=True)
        excel.Quit()
        excel = None
    except Exception as e:
        print(f"An error occurred, {file_name} : ", e)


def initial_delete_ouputfile():
    folder_path = r"c:/Users/minhwasoo/Documents/"
    files = os.listdir(folder_path)
    xlsmfiles = [f for f in files if f.endswith('.xlsm')]

    if xlsmfiles:
        for file in xlsmfiles:
            print(file)

            if os.path.exists(folder_path + file):
                os.remove(folder_path + file)
                print(f"{file} has been removed successfully.")
            else:
                print(f"The file {file} does not exist in the folder {folder_path}.")


def main():
    initial_delete_ouputfile()
    os.chdir(DIRECTORY)
    files = os.listdir()

    xlsmfiles = [f for f in files if f.endswith('.xlsm')]
    xlsmfiles = natsorted(xlsmfiles)

    for file in xlsmfiles:
        print('Processing file: ', file)
        inject_value_to_sheet(DIRECTORY + file)


if __name__ == "__main__":
    main()
