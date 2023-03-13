# !/usr/bin/env python3

# import os
# import sys

# def remove_extension(file_name):
#     """Removes the extension from the given file name"""
#     return os.path.splitext(file_name)[0]

# def get_extension(file_name):
#     return os.path.splitext(file_name)[1]

# def main_job(mode):
#     # cwd = os.getcwd()
#     # dir_path = "/path/to/directory"  # Replace with the path to the directory you want to search in

#     files = os.listdir()
#     movie_files = [f for f in os.listdir() if f.endswith(('.mp4', '.mkv', '.avi', '.mov', '.m4v'))]
#     movie_files.sort()

#     if not movie_files:
#         print('folder has no movie files ...')
#         exit()

#     smi_files = [f for f in os.listdir() if f.endswith(('.smi', '.ass', '.srt', '.sub', '.sami'))]
#     smi_files.sort()

#     file_names = []

#     if mode == 'mov':
#         for f in movie_files:
#             base_name = remove_extension(f)
#             file_names.append(base_name)
#     else:
#         for f in smi_files:
#             base_name = remove_extension(f)
#             file_names.append(base_name)

#     file_extensions = []

#     if mode == 'mov':
#         for f in smi_files:
#             file_extensions.append(get_extension(f))
#     else:
#         for f in movie_files:
#             file_extensions.append(get_extension(f))

#     print('----------------------------------------------------')
#     print(f'movie files : {len(movie_files)}')
#     print(f'smi files : {len(smi_files)}')
#     print(f'filename : {len(file_names)}')

#     if len(movie_files) != len(smi_files):
#         print('something wrong with movie and subtitle file ....')
#         quit()

#     # change filename by subtitle name
#     print('----------------------------------------------------')
#     i = int('0')
#     if mode == 'mov':
#         for f in smi_files:
#             old_file_name = f
#             new_file_name = file_names[i] + file_extensions[i]
#             print(new_file_name)
#             os.rename(old_file_name, new_file_name)
#             i += 1
#     else:
#         for f in movie_files:
#             old_file_name = f
#             new_file_name = file_names[i] + file_extensions[i]
#             print(new_file_name)
#             os.rename(old_file_name, new_file_name)
#             i += 1

#     print('----------------------------------------------------')


import os


def get_files_with_extension(extension):
    return [f for f in os.listdir() if f.endswith(extension)]


def get_base_name(file_name):
    return os.path.splitext(file_name)[0]


def get_extension(file_name):
    return os.path.splitext(file_name)[1]


def rename_files(old_file_names, new_file_names):
    for old_name, new_name in zip(old_file_names, new_file_names):
        os.rename(old_name, new_name)


def main_job(mode):
    movie_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.m4v')
    subtitle_extensions = ('.smi', '.ass', '.srt', '.sub', '.sami')

    movie_files = get_files_with_extension(movie_extensions)
    subtitle_files = get_files_with_extension(subtitle_extensions)

    if not movie_files or not subtitle_files:
        print('Folder has no movie or subtitle files ...')
        exit()

    movie_files.sort()
    subtitle_files.sort()

    if len(movie_files) != len(subtitle_files):
        print('Something wrong with movie and subtitle files ....')
        quit()

    file_names = [get_base_name(f) for f in movie_files] if mode == 'mov' else [get_base_name(f) for f in subtitle_files]
    file_extensions = [get_extension(f) for f in subtitle_files] if mode == 'mov' else [get_extension(f) for f in movie_files]

    print('----------------------------------------------------')
    print(f'Movie files: {len(movie_files)}')
    print(f'Subtitle files: {len(subtitle_files)}')
    print(f'Filename: {len(file_names)}')

    rename_files(subtitle_files if mode == 'mov' else movie_files, [file_names[i] + file_extensions[i] for i in range(len(file_names))])

    print('----------------------------------------------------')


# if __name__ == "__main__":
#     mode = sys.argv[1]
#     if mode == 'sub':
#         print("You selected 'sub' mode.")
#     elif mode == 'mov':
#         print("You selected 'mov' mode.")
#     else:
#         print("Invalid mode. Please select either 'sub' or 'mov'.")
#         exit()

#     main_job(mode)

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['sub', 'mov'], help="Select 'sub' or 'mov' mode.")
    args = parser.parse_args()

    main_job(args.mode)

if __name__ == "__main__":
    main()