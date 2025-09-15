import os
import sys


def print_debug(msg='', chr='*', len=180):
    print(chr * len)
    print(msg)
    print(chr * len)


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
        print_debug('-')
        for _ in directories: print(_)
        print_debug('-')

    return directories


def toggle_source_target(path=r"z:/06_Send2/", is_display=False):
    drive = get_drive_letter(path)
    if is_display:
        print_debug('-')
        print(drive, path)

    # if drive == "d:" or drive == "D:":
    #     target_folder = change_drive_letter(path, "Z:")
    #     print(path, target_folder)
    # else:
    #     target_folder = change_drive_letter(path, "D:")
    #     print(path, target_folder)

    target_drive = "Z:" if drive.lower() == "d:" else "D:"
    target_folder = change_drive_letter(path, target_drive)
    print(path, target_folder)

    print_debug('-')
    return target_folder


def folder_name_sync(path_source, path_target='empty'):
    """
    Synchronizes folder names between the source and target directories.

    Args:
        path_source (str): The source directory path.
        path_target (str): The target directory path (default is 'empty').

    Returns:
        bool: True if the folder names are synchronized successfully, False otherwise.
    """

    source_dir = path_source
    target_dir = path_target

    print(f"folder_name_sync, source: {source_dir}")
    print(f"folder_name_sync, target: {target_dir}")

    if target_dir == 'empty':
        print_debug('into toggle_source_target')
        target_dir = toggle_source_target(path=source_dir)

    os.chdir(target_dir)
    s_directories = list_directories_in_current_path(source_dir)
    t_directories = list_directories_in_current_path(target_dir)

    print(len(s_directories), len(t_directories))

    if len(s_directories) != len(t_directories):
        print("Folder lengths do not match!")
        return False

    print_debug('')
    print("Folder Name Sync")
    print(os.getcwd())

    for src_dir, tgt_dir in zip(t_directories, s_directories):
        print(f"src_dir = {src_dir}, tgt_dir = {tgt_dir}")
        rename_folder(current_name=src_dir, new_name=tgt_dir)

    print_debug('')
    return True




# 폴더이름을 양쪽 일치 시키기 위해서 작업을 하던중에 문제
# 토털커맨더에서 인자를 어떻게 설정해야 되는지를  몰라서, 여러가지를 시험하던 도중에 하나
# 시간이 지난뒤에 보게 되어, 잘은 모르지만 ...

# 나중에 , 그리고 후에 알게된 사실
# 토털커맨더 인자

#  "%P\" "%T\"



if __name__ == "__main__":

    # Print the number of arguments (including the script name)
    print(f"Number of arguments: {len(sys.argv)}")

    # Print the script name
    print(f"Script name: {sys.argv[0]}")

    # Print all arguments one by one
    for i, arg in enumerate(sys.argv[1:], start=1):
        arg_temp = arg.replace('"', '\\')
        print(f"Argument {i}: {arg_temp}")

    print_debug('this is parsing argument ', '-')
    source_dir = sys.argv[1].replace('"', '\\')
    target_dir = sys.argv[2].replace('"', '\\')

    print(f"1, source : {source_dir}")
    print(f"1, target : {target_dir}")

    _ = input("Enter")

    print_debug('sync folder name  ', '-')
    if source_dir and os.path.isdir(source_dir):
        folder_name_sync(source_dir, target_dir)

    if target_dir:
        _ = input(f"Folder Name Sync Complete source : {source_dir}  --> target {target_dir}")
    else:
        _ = input(f"Folder Name Sync Complete source : {source_dir}  --> target {toggle_source_target(source_dir)}")
