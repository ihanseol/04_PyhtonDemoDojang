from pywinauto import Application, findwindows
import time

# Function to insert data into Excel using window handle
def insert_data_into_excel(hwnd, data):
    app = Application().connect(handle=hwnd)
    window = app.window(handle=hwnd)

    # Activate the Excel window
    window.set_focus()

    # Assuming Excel sheet is active, you can directly send keys to insert data
    for row_index, row_data in enumerate(data, start=1):
        for col_index, cell_value in enumerate(row_data, start=1):
            window.send_keystrokes(f"{cell_value}{{TAB}}")
            time.sleep(0.1)  # Adjust sleep time if needed
        window.send_keystrokes("{ENTER}")

# Example usage
if __name__ == "__main__":
    # Obtain the handle of the Excel window (you may need to adapt this part)

    #hwnd = findwindows.find_window(title_re='.*Excel')
    #hwnd = findwindows.find_window(process=excel_pid)
    hwnd = findwindows.find_window(class_name="XLMAIN")

    if hwnd:
        # Sample data to insert into Excel
        data_to_insert = [
            ["Name", "Age", "City"],
            ["John", "30", "New York"],
            ["Alice", "25", "Los Angeles"],
            ["Bob", "35", "Chicago"]
        ]

        # Insert data into Excel
        insert_data_into_excel(hwnd, data_to_insert)
    else:
        print("Excel window not found.")
