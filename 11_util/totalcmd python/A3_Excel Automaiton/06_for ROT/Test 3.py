import pythoncom
import win32process


def get_process_names():
    process_names = []
    pids = win32process.EnumProcesses()
    for pid in pids:
        try:
            hProcess = win32process.OpenProcess(win32process.PROCESS_QUERY_INFORMATION | win32process.PROCESS_VM_READ,
                                                False, pid)
            process_name = win32process.GetModuleFileNameEx(hProcess, 0)
            process_names.append(process_name)
            win32process.CloseHandle(hProcess)
        except Exception as e:
            pass  # Ignore exceptions if process cannot be accessed
    return process_names


if __name__ == "__main__":
    process_names = get_process_names()
    for name in process_names:
        print(name)
