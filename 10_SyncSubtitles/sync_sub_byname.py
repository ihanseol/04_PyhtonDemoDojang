# !/usr/bin/env python3

import os
import sys


def remove_extension(file_name):
    """Removes the extension from the given file name"""
    return os.path.splitext(file_name)[0]


def get_extension(file_name):
    return os.path.splitext(file_name)[1]


def main_job(mode):
    # cwd = os.getcwd()
    # dir_path = "/path/to/directory"  # Replace with the path to the directory you want to search in

    files = os.listdir()
    movie_files = [f for f in os.listdir() if f.endswith(('.mp4', '.mkv', '.avi', '.mov', '.m4v'))]
    movie_files.sort()

    if not movie_files:
        print('folder has no movie files ...')
        exit()

    smi_files = [f for f in os.listdir() if f.endswith(('.smi', '.ass', '.srt', '.sub', '.sami'))]
    smi_files.sort()

    file_names = []

    if mode == 'mov':
        for f in movie_files:
            base_name = remove_extension(f)
            file_names.append(base_name)
    else:
        for f in smi_files:
            base_name = remove_extension(f)
            file_names.append(base_name)

    file_extensions = []

    if mode == 'mov':
        for f in smi_files:
            file_extensions.append(get_extension(f))
    else:
        for f in movie_files:
            file_extensions.append(get_extension(f))

    print('----------------------------------------------------')
    print(f'movie files : {len(movie_files)}')
    print(f'smi files : {len(smi_files)}')
    print(f'filename : {len(file_names)}')

    if len(movie_files) != len(smi_files):
        print('something wrong with movie and subtitle file ....')
        quit()

    # change filename by subtitle name
    print('----------------------------------------------------')
    i = int('0')
    if mode == 'mov':
        for f in smi_files:
            old_file_name = f
            new_file_name = file_names[i] + file_extensions[i]
            print(new_file_name)
            os.rename(old_file_name, new_file_name)
            i += 1
    else:
        for f in movie_files:
            old_file_name = f
            new_file_name = file_names[i] + file_extensions[i]
            print(new_file_name)
            os.rename(old_file_name, new_file_name)
            i += 1

    print('----------------------------------------------------')


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == 'sub':
        print("You selected 'sub' mode.")
    elif mode == 'mov':
        print("You selected 'mov' mode.")
    else:
        print("Invalid mode. Please select either 'sub' or 'mov'.")
        exit()

    main_job(mode)
