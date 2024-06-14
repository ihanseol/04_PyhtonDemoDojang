import win32com.client as win32

def get_excel_object_by_pathname(pathname):
    try:
        excel = win32.GetObject(Pathname=pathname)
        return excel
    except Exception as e:
        print("Error:", e)
        return None

excel_by_pathname = get_excel_object_by_pathname(r"d:\05_Send\pythonProject\06_for ROT\Set ROT.xlsm")

if excel_by_pathname:
    print("Connected to Excel file using Pathname.")
    print(excel_by_pathname)

# Get the active workbook and active sheet
wb = excel_by_pathname.ActiveWorkbook
ws = wb.ActiveSheet

# Write "Hello World" into cell A30
ws.Range("A30").Value = "Hello World"