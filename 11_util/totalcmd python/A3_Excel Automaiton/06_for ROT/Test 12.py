import pythoncom
import re

def get_excel_instances():
    # Initialize COM context and get running object table
    context = pythoncom.CreateBindCtx(0)
    running_coms = pythoncom.GetRunningObjectTable()
    monikers = running_coms.EnumRunning()

    # Regular expression pattern to match Excel file names
    excel_pattern = re.compile(r'^Excel\.Application\.')

    # Iterate through running objects
    for moniker in monikers:
        name = moniker.GetDisplayName(context, moniker)
        obj = running_coms.GetObject(moniker)

        # Debug print statements
        print("Display Name:", name)
        print("Object:", obj)
        print()

        # Check if the object corresponds to Excel instance
        if excel_pattern.match(name):
            print("Excel file:", name)

# Call the function to get Excel instances
get_excel_instances()
