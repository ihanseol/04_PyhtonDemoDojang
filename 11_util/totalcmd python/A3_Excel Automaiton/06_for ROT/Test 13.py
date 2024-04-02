import win32com.client


def get_excel_instances():
    # Create a COM object for Excel application
    excel = win32com.client.Dispatch("Excel.Application")

    # Iterate through running Excel instances
    for wb in excel.Workbooks:
        print("Excel file:", wb.FullName)


# Call the function to get Excel instances
get_excel_instances()
