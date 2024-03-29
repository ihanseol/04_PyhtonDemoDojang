import win32com.client


def write_to_excel():
    try:
        # Get running instance of Excel
        excel = win32com.client.GetActiveObject("Excel.Application")
    except:
        print("Excel is not running.")
        return

    # Access the active workbook
    wb = excel.ActiveWorkbook

    # Access the active sheet
    ws = wb.ActiveSheet

    # Write "Hello World" to cell A10
    ws.Range("A20").Value = "Hello World 33"

    # Save changes (if needed)
    wb.Save()

    # Close workbook and Excel application (optional)
    # wb.Close()
    # excel.Quit()


write_to_excel()
