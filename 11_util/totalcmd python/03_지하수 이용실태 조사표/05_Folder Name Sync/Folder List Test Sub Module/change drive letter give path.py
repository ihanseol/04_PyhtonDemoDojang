import os


def change_drive_letter(path, new_drive_letter):
    if get_path_separator(path) == '/':
        convert_path_separator(path)

    # Split the path into drive and the rest of the path
    drive, tail = os.path.splitdrive(path)

    # Concatenate the new drive letter with the rest of the path
    new_path = os.path.join(new_drive_letter + '\\', tail.lstrip('\\'))

    return new_path


def convert_path_separator(path):
    # Replace '/' with '\\'
    return path.replace('/', '\\')


def get_path_separator(path):
    if '/' in path:
        return '/'
    elif '\\' in path:
        return '\\'
    else:
        return None


def get_drive_letter(path):
    drive, _ = os.path.splitdrive(path)
    return drive


def toggle_source_target(path=r"z:/06_Send2/"):
    drive = get_drive_letter(path)
    print(drive, path)

    if drive == "d:" or drive == "D:":
        target_folder = change_drive_letter(path, "Z:")
        print(path, target_folder)
    else:
        target_folder = change_drive_letter(path, "D:")
        print(path, target_folder)

    return target_folder
#
# # Example usage:
# path = r'C:\Users\Example\Documents\file.txt'
# new_path = change_drive_letter(path, 'D')
# print(f"New path: {new_path}")


target_folder = toggle_source_target()


