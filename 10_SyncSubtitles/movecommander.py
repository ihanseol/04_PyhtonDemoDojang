import os
import sys
import time
import subprocess
import shutil
import platform

arch = platform.architecture()[0]

if arch == "64bit":
    print("System is x64")
    commander_name =  "TOTALCMD64.EXE"
else:
    print("System is x86")
    commander_name =  "TOTALCMD.EXE"

subprocess.run(["taskkill", "/f", "/im", commander_name])


if len(sys.argv) != 2:
    print("Usage: python script.py <rar_file_name>")
    sys.exit(1)


desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
print("Desktop path:", desktop_path)


source_rar = sys.argv[1]
target_dir = desktop_path


print(f"source file : {source_rar}")
print(f"target directory : {target_dir}")


print(f"Extract {source_rar} ....")
subprocess.run(["C:\\Program Files\\WinRAR\\winrar.exe", "x", "-y", source_rar, "-op", target_dir], check=True)


print("delete tatalcmd directory ...")

folder_path = r"c:\Program Files\totalcmd"

if os.path.exists(folder_path):       
    subprocess.run(["rmdir", "/s", "/q", folder_path], shell=True)


# input("!!! finder program files ...")

print(f"os.listdir(target_dir)[0] : {os.listdir(target_dir)[0]}")
# time.sleep(2)
print("Done waiting.")

#src_folder = r"c:\Users\minhwasoo\Desktop\totalcmd"

src_folder = desktop_path + "\\totalcmd"
dst_folder = r"c:\Program Files"


print(f"Source Folder : {src_folder}")
print(f"Destination Folder : {dst_folder}")

# input("press enter key ...")

shutil.move(src_folder, dst_folder)









 




