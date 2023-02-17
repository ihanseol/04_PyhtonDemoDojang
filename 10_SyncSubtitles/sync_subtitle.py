
#!/usr/bin/env python3


import os

def remove_extension(file_name):
    """Removes the extension from the given file name"""
    return os.path.splitext(file_name)[0]


# cwd = os.getcwd()
# dir_path = "/path/to/directory"  # Replace with the path to the directory you want to search in

files = os.listdir()
movie_files = []

for file in files:
    if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        movie_files.append(file)

movie_files.sort()

if len(movie_files) == 0:
    print('folder has no movie files ...')
    quit()


# mp4_files = [f for f in os.listdir(cwd) if f.endswith(".mp4")]
# mp4_files.sort()

smi_files = [f for f in os.listdir() if f.endswith(('.smi','.srt','.sub','.sami'))]
smi_files.sort()


file_names = []

for f in movie_files:
    base_name = remove_extension(f)
    file_names.append(base_name)
   

print('----------------------------------------------------')

print(f'movie files : {len(movie_files)}')
print(f'smi files : {len(smi_files)}')
print(f'filename : {len(file_names)}')


if len(movie_files) != len(smi_files):
    print('something wrong with movie and subtitle file ....')
    quit()

print('----------------------------------------------------')
i = int('0')
for f in smi_files:
    old_file_name = f
    new_file_name = file_names[i] + ".smi"
    print(new_file_name)

    os.rename(old_file_name, new_file_name)
    i+=1
print('----------------------------------------------------')






