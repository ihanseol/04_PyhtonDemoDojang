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


def extract_rar_to_desktop(rar_file_path):
    winrar_path = "C:\\Program Files\\WinRAR\\winrar.exe"
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

    print(f"Attempting to extract '{rar_file_path}' to '{desktop_path}' using winrar.exe...")

    try:
        if not os.path.exists(rar_file_path):
            print(f"Error: The file '{rar_file_path}' was not found.")
            return

        command = [winrar_path, 'x', rar_file_path, desktop_path]

        # Use subprocess.run to execute the command.
        # It captures the output and returns a CompletedProcess object.
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        print("Extraction successful!")
        # Print any output from WinRAR's standard output
        if result.stdout:
            print(f"WinRAR Output:\n{result.stdout}")

    except FileNotFoundError:
        # This error occurs if winrar.exe is not in the system's PATH
        print("Error: 'winrar.exe' was not found.")
        print(
            "Please ensure WinRAR is installed and its directory is added to your system's PATH environmental variable.")
    except subprocess.CalledProcessError as e:
        # This error occurs if winrar.exe returns a non-zero exit code (an error)
        print(f"Error: WinRAR extraction failed with exit code {e.returncode}.")
        print(f"WinRAR Error Output:\n{e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def kill_totalcommander():
    arch = platform.architecture()[0]

    dummy_process_name = ''

    if arch == "64bit":
        print("System is x64")
        dummy_process_name = "TOTALCMD64.EXE"
    else:
        print("System is x86")
        dummy_process_name = "TOTALCMD.EXE"

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


def extract_totalcmd_rar(source_rar):
    winrar_path = "C:\\Program Files\\WinRAR\\winrar.exe"

    if len(sys.argv) != 2:
        print("Usage: python script.py <rar_file_name>")
        sys.exit(1)

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    print("Desktop path:", desktop_path)

    target_dir = desktop_path

    print(f"source file : {source_rar}")
    print(f"target directory : {target_dir}")

    print(f"Extract {source_rar} ....")

    rar_filename = sys.argv[1]

    # script_directory = os.path.dirname(os.path.abspath(__file__))
    # file_to_extract = os.path.join(script_directory, rar_filename)

    extract_rar_to_desktop(source_rar)


def delete_and_move():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    print("Desktop path:", desktop_path)

    print("delete tatalcmd directory ...")

    folder_path = r"c:\Program Files\totalcmd"

    if os.path.exists(folder_path):
        subprocess.run(["rmdir", "/s", "/q", folder_path], shell=True)

    # input("!!! finder program files ...")

    print(f"os.listdir(target_dir)[0] : {os.listdir(desktop_path)[0]}")
    # time.sleep(2)
    print("Done waiting.")

    # src_folder = r"c:\Users\minhwasoo\Desktop\totalcmd"

    src_folder = desktop_path + "\\totalcmd"
    dst_folder = r"c:\Program Files"

    print(f"Source Folder : {src_folder}")
    print(f"Destination Folder : {dst_folder}")

    # input("press enter key ...")

    shutil.move(src_folder, dst_folder)


if __name__ == "__main__":
    source_rar = sys.argv[1]

    kill_totalcommander()
    extract_totalcmd_rar(source_rar)
    delete_and_move()
