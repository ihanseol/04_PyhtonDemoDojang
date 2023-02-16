import os
import sys
import shutil
import codecs

if len(sys.argv) != 2:
    print("Usage: python script.py <rar_file_name>")
    sys.exit(1)


desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
print("Desktop path:", desktop_path)

filename = sys.argv[1]
target_dir = desktop_path

# Open the file in Notepad
# filename = 'file.csv'


with codecs.open(filename, 'r', encoding='cp949') as f:
    file_contents = f.read()

# Save the file as UTF-8 with BOM
with codecs.open(filename, 'w', encoding='utf-8-sig') as f:
    f.write(file_contents)




