import os
import sys


def one_level_up_if_directory(path):
    if os.path.isdir(path):
        parent_directory = os.path.dirname(path)
        return parent_directory
    else:
        return "The given path is not a directory."


def get_drive_letter(path):
    drive, _ = os.path.splitdrive(path)
    return drive


def change_drive_letter(path, new_drive_letter):
    # Split the path into drive and the rest of the path
    drive, tail = os.path.splitdrive(path)

    # Concatenate the new drive letter with the rest of the path
    new_path = os.path.join(new_drive_letter + '\\', tail.lstrip('\\'))

    return new_path


def rename_folder(current_name, new_name):
    try:
        os.rename(current_name, new_name)
        print(f"Folder renamed from '{current_name}' to '{new_name}'")
    except FileNotFoundError:
        print(f"The folder '{current_name}' does not exist.")
    except PermissionError:
        print(f"Permission denied to rename the folder '{current_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def list_directories_in_current_path(path=r"z:/06_Send2/", is_display=False):
    if os.path.isdir(path): os.chdir(path)
    current_path = os.getcwd()
    directories = [d for d in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, d))]

    if is_display:
        print('-' * 80)
        for _ in directories: print(_)
        print('-' * 80)

    return directories


def toggle_source_target(path=r"z:/06_Send2/", is_display=False):
    drive = get_drive_letter(path)
    if is_display:
        print('-' * 60)
        print(drive, path)

    if drive == "d:" or drive == "D:":
        target_folder = change_drive_letter(path, "Z:")
        print(path, target_folder)
    else:
        target_folder = change_drive_letter(path, "D:")
        print(path, target_folder)

    print('-' * 60)
    return target_folder


def folder_name_sync(path_source, path_target=''):
    source_dir = path_source
    target_dir = path_target

    print(f"folder_name_sync, source:{source_dir}, target:{target_dir}")

    if target_dir == '':
        target_dir = toggle_source_target(path=source_dir)

    # result = one_level_up_if_directory(path)
    # print(f"The path '{path}' is: {result}")

    os.chdir(target_dir)
    s_directories = list_directories_in_current_path(source_dir)
    t_directories = list_directories_in_current_path(target_dir)

    print(len(s_directories), len(t_directories))

    if len(s_directories) != len(t_directories):
        print("folder length is not match !")
        return False

    print("*" * 80)
    print("Folder Name Sync")
    print(os.getcwd())

    for src_dir, tgt_dir in zip(t_directories, s_directories):
        print(f"src_dir = {src_dir}, tgt_dir = {tgt_dir}")
        rename_folder(current_name=src_dir, new_name=tgt_dir)

    print("*" * 80)


folder_name_sync("d:\\09_hardRain\\09_ihanseol - 2024\\","e:\\09_hardRain\\09_ihanseol - 2024\\")