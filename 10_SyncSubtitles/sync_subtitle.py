import os

def remove_extension(file_name):
    """Removes the extension from the given file name"""
    return os.path.splitext(file_name)[0]


cwd = os.getcwd()
# dir_path = "/path/to/directory"  # Replace with the path to the directory you want to search in

mp4_files = [f for f in os.listdir(cwd) if f.endswith(".mp4")]
mp4_files.sort()

smi_files = [f for f in os.listdir(cwd) if f.endswith(".smi")]
smi_files.sort()


file_names = []

for f in mp4_files:
    base_name = remove_extension(f)
    file_names.append(base_name)
   

print('----------------------------------------------------')

print(f'mp4file : {len(mp4_files)}')
print(f'smifile : {len(smi_files)}')
print(f'filename : {len(file_names)}')


if len(mp4_files) != len(smi_files):
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






