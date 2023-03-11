import os
import fnmatch

files = os.listdir()
w1_files = fnmatch.filter(files, "w1*.aqt")
print(f'len w1 files : {len(w1_files)}')



