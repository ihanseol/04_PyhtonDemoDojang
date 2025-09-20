import os
import sys
import time
import subprocess
import shutil
import psutil
import platform

def terminate_process_by_name(process_name):
    """
    Terminates a process by its name. This function is for educational purposes
    to demonstrate process management concepts.

    Args:
        process_name (str): The name of the process to terminate.
    """
    print(f"Attempting to terminate any processes named '{process_name}'...")

    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            try:
                # Terminate the process
                process.terminate()
                print(f"Process with PID {process.pid} and name '{process.info['name']}' terminated.")
            except psutil.AccessDenied:
                print(
                    f"Access denied. Cannot terminate process with PID {process.pid}. You may need to run this script as an administrator.")
            except psutil.NoSuchProcess:
                print(f"Process with PID {process.pid} was not found (it may have already been terminated).")
            except Exception as e:
                print(f"An error occurred while terminating process with PID {process.pid}: {e}")


if __name__ == '__main__':
    arch = platform.architecture()[0]
    dummy_process_name = ''

    if arch == "64bit":
        print("System is x64")
        dummy_process_name = "TOTALCMD64.EXE"
    else:
        print("System is x86")
        dummy_process_name = "TOTALCMD.EXE"


    # Check if a dummy process exists for demonstration purposes
    process_found = False
    for p in psutil.process_iter(['name']):
        if p.info['name'] == dummy_process_name:
            process_found = True
            break

    if process_found:
        print(f"Found '{dummy_process_name}'. Calling terminate_process_by_name().")
        terminate_process_by_name(dummy_process_name)
    else:
        print(f"'{dummy_process_name}' not found. Please create a dummy process to test.")
        print("For example, on Windows, you can open Notepad before running this script.")

