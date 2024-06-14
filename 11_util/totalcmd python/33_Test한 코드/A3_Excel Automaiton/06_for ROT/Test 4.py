# its Working OK
# get process name by Ctypes and

import ctypes
import pythoncom

def get_process_names():
    # Load necessary functions from kernel32.dll
    kernel32 = ctypes.windll.kernel32
    psapi = ctypes.windll.psapi

    # Define constants
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010
    MAX_PATH = 260

    # Set up buffers and variables
    process_ids = (ctypes.c_ulong * 1024)()
    cb_needed = ctypes.c_ulong()
    count = ctypes.c_ulong()
    process_names = []

    # Get process IDs
    if not psapi.EnumProcesses(ctypes.byref(process_ids), ctypes.sizeof(process_ids), ctypes.byref(cb_needed)):
        return None

    # Calculate number of processes
    count.value = cb_needed.value // ctypes.sizeof(ctypes.c_ulong())

    # Iterate over each process ID
    for i in range(count.value):
        # Open the process
        h_process = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, process_ids[i])
        if h_process:
            # Get process name
            module_name = ctypes.create_string_buffer(MAX_PATH)
            if psapi.GetModuleFileNameExA(h_process, 0, module_name, MAX_PATH):
                process_names.append(module_name.value.decode("utf-8", "ignore"))
            kernel32.CloseHandle(h_process)

    return process_names

if __name__ == "__main__":
    process_names = get_process_names()
    if process_names:
        for name in process_names:
            print(name)
    else:
        print("Failed to retrieve process names.")
