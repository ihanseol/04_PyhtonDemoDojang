import psutil

def get_excel_file_path():
    for process in psutil.process_iter():
        if process.name() == "EXCEL.EXE":
            try:
                # Accessing the command line arguments of the process
                cmd_args = process.cmdline()
                for arg in cmd_args:
                    # Check if the argument contains ".xlsm", indicating an Excel file
                    if arg.lower().endswith(".xlsm") or arg.lower().endswith(".xlsx"):
                        return arg
            except (psutil.AccessDenied, psutil.ZombieProcess):
                continue
    return None

# Get the path of the active Excel file
file_path = get_excel_file_path()

if file_path:
    print("Active Excel file path:", file_path)
else:
    print("No active Excel instance found.")



