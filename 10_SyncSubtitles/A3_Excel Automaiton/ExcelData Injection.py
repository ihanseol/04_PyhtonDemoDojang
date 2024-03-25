import random
import win32com.client
import win32com.client as win32
import time

random_int = random.randint(1, 100)
print("Random Integer:", random_int)

file_name = r"d:\05_Send\A3_ge_OriginalSaveFile.xlsm"
cell_values = {"I48": 7.5, "I52": 33, "M44": 33, "M45": 250, "M48": 5.62, "M49": 13.67, "M51": 150}

macro_name_01 = "mod_W1StepTEST.set_CB1"
macro_name_02 = "mod_W1StepTEST.set_CB2"

button_name = "CommandButton6"


def inject_value_to_cells(book, cell_values):
    sheet = book.Worksheets("Input")

    for cell, value in cell_values.items():
        sheet.Range(cell).Value = value

    random_int = random.randint(1, 100)
    formatted_random_int = "{:03d}".format(random_int)

    book.SaveAs("out" + str(formatted_random_int) + ".xlsm")
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


#
# def inject_value_to_sheet(file_name):
#     try:
#         excel = win32com.client.Dispatch("Excel.Application")
#         excel.ScreenUpdating = False
#         excel.Visible = True
#
#         book = excel.Workbooks.Open(file_name)
#
#         # Input Sheet
#         ws_input = book.Worksheets("Input")
#
#         ws = book.Worksheets("Input")
#         ws.Activate()
#
#         for cell, value in cell_values.items():
#             ws_input.Range(cell).Value = value
#
#         click_excel_button(ws_input, "CommandButton2")
#         time.sleep(1)
#         click_excel_button(ws_input, "CommandButton3")
#         time.sleep(1)
#         click_excel_button(ws_input, "CommandButton6")
#         time.sleep(1)
#
#         # StepTest Sheet
#         ws_step_test = book.Worksheets("stepTest")
#         ws_step_test.Activate()
#
#         click_excel_button(ws_step_test, "CommandButton1")
#         time.sleep(2)
#         click_excel_button(ws_step_test, "CommandButton2")
#         time.sleep(1)
#
#         # LongTest Sheet
#         ws_long_test = book.Worksheets("LongTest")
#         ws_long_test.Activate()
#
#         click_excel_button(ws_long_test, "CommandButton5")
#         time.sleep(3)
#         click_excel_button(ws_long_test, "CommandButton4")
#         time.sleep(1)
#         click_excel_button(ws_long_test, "CommandButton7")
#
#         book.Close(SaveChanges=True)
#         excel.Quit()
#
#     except Exception as e:
#         print("An error occurred:", e)


def inject_value_to_sheet(file_name):
    try:
        # excel = win32com.client.Dispatch("Excel.Application")
        # excel = win32com.client.gencache.EnsureDispatch("Excel.Application")

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        # excel = win32.Dispatch('Excel.Application')

        excel.ScreenUpdating = False
        book = excel.Workbooks.Open(file_name)
        excel.Visible = True

        ws = book.Worksheets("Input")
        ws.Activate()

        inject_value_to_cells(book, cell_values)
        print('inject value to cell')
        ws.Activate()

        click_excel_button(ws, "CommandButton2")
        print('Input, Button2')
        time.sleep(1)
        click_excel_button(ws, "CommandButton3")
        print('Input, Button3')
        time.sleep(1)
        click_excel_button(ws, "CommandButton6")
        print('Input, Button6')
        time.sleep(1)

        # StepTest Fit
        ws = book.Worksheets("stepTest")
        ws.Activate()

        time.sleep(1)

        click_excel_button(ws, "CommandButton1")
        print('Step, Button1')
        time.sleep(2)
        click_excel_button(ws, "CommandButton2")
        print('Step, Button2')
        time.sleep(1)

        # LongTermTes
        ws = book.Worksheets("LongTest")
        ws.Activate()

        time.sleep(1)
        click_excel_button(ws, "CommandButton5")
        print('Long, Button5')
        time.sleep(3)
        click_excel_button(ws, "CommandButton4")
        print('Long, Button5')
        time.sleep(1)
        click_excel_button(ws, "CommandButton7")
        print('Long, Button7')

        excel.ScreenUpdating = True
        sheet = None
        book.Close(SaveChanges=True)
        excel.Quit()
        excel = None
    except Exception as e:
        print(f"An error occurred, {file_name} : ", e)


def main():
    inject_value_to_sheet(file_name)


if __name__ == "__main__":
    main()
