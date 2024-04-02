import win32com.client

def write_to_excel():
    try:
        # Attempt to connect to an existing instance of Excel using the Running Object Table (ROT)
        excel = None
        excel_instances = []

        # Enumerate all running objects to find Excel instances
        rot = win32com.client.Dispatch("Rot13UI.RotEntry")
        for i in range(rot.Count):
            excel_instances.append(rot.Item(i).Application)

        # Choose the first Excel instance found
        if excel_instances:
            excel = excel_instances[0]

        if excel is None:
            print("No running instance of Excel found.")
            return

        # Ensure Excel is visible
        excel.Visible = True

        # Get the active workbook and active sheet
        wb = excel.ActiveWorkbook
        ws = wb.ActiveSheet

        # Write "Hello World" into cell A30
        ws.Range("A30").Value = "Hello World"

        print("Successfully wrote 'Hello World' into cell A30.")
    except Exception as e:
        print(f"Failed to write to Excel: {e}")

if __name__ == "__main__":
    write_to_excel()
