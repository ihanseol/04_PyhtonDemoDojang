import os
import time
import fnmatch
import pyautogui

program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'

def setview_default():
	pyautogui.hotkey('alt', 'v')
	time.sleep(0.1)
	pyautogui.press('r')

def setview_report():
	pyautogui.hotkey('alt', 'v')
	time.sleep(0.1)
	pyautogui.press('r')


# def delete_exisiting_pdffile():
# 	dir_path = os.path.expanduser("~\\Documents\\")

# 	for filename in os.listdir(dir_path):
# 		if filename.endswith(".pdf"):
# 			os.remove(dir_path + filename)

# def delete_existing_pdf_files():
#     documents_path = os.path.expanduser("~\\Documents\\")
#     pdf_files = [file for file in os.listdir(documents_path) if file.endswith(".pdf")]
#     for file in pdf_files:
#         os.remove(os.path.join(documents_path, file))



def delete_existing_pdf_files(folder_path):
    pdf_files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]
    for file in pdf_files:
        os.remove(os.path.join(folder_path, file))

# The function now takes a parameter `folder_path` which specifies the folder where the PDF files are located. 
# This makes the function more reusable as it can now be used to delete PDF files from any folder, not just the Documents folder.



def printpdf(fname):
	pyautogui.hotkey('ctrl', 'p')
	pyautogui.press('enter')
	time.sleep(0.3)
	pyautogui.typewrite(fname)	
	pyautogui.press('enter') 	
	time.sleep(0.3)

def exit_program():
	pyautogui.hotkey('alt', 'f4')
	time.sleep(0.1)
	pyautogui.press('n') 	

# Version 1
# def change_filename(): 
# 	directory = "d:\\05_Send\\"
# 	for filename in os.listdir(): 
# 		if filename.endswith(".aqt"):
# 			name, ext = os.path.splitext(filename)
# 			if "- 복사본" in name:
# 				new_name = name.replace(" - 복사본", "_01") + ext
# 				os.rename(directory + filename, directory + new_name)

# Version 2
# def change_filename(directory):
#     for filename in os.listdir(directory):
#         if filename.endswith(".aqt") and "- 복사본" in filename:
#             name, ext = os.path.splitext(filename)
#             new_name = name.replace(" - 복사본", "_01") + ext
#             os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))


# Version 3
def change_filename(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".aqt") and "- 복사본" in filename:
            new_name = filename.replace(" - 복사본", "_01")
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
	    



def remove_extension(file_name):
	return os.path.splitext(file_name)[0]


def mainjob(well, i, filename):
	# file_path = os.path.abspath(filename)
	os.startfile(program_path)
	time.sleep(0.5)
	pyautogui.hotkey('ctrl', 'o')
	pyautogui.typewrite(filename)
	pyautogui.press('enter') 
	time.sleep(0.5)

	printpdf(f'a{well}-{i}')
	setview_report()
	printpdf(f'p{well}-{i}')
	exit_program()
	


# def get_wellnum(mode, f):
# 	# 1 -- return 'w1'
# 	# else -- return 1
# 	if mode == 1:
# 		return f.split("_")[0]
# 	else:
# 		well = f.split("_")[0]
# 		return int(well[1:])

# version 1
#
def get_wellnum(mode, f):
    well = f.split("_")[0]
    if mode == 1:
        return 'w' + well[1:]
    else:
        return int(well[1:])


# Original Version
#
# def main_process():
# 	change_filename()
# 	delete_exisiting_pdffile()

# 	files = os.listdir()
# 	for i in range(1,13):
# 		j = 0
# 		wfiles = fnmatch.filter(files, f"w{i}*.aqt")
# 		if not wfiles: exit()
# 		for file in wfiles:
# 			j += 1
# 			print(f'{get_wellnum(2,file)}-{j}  - {file}')
# 			mainjob(i, j, file)


# Version 1 

def main_process():
    change_filename()
    delete_existing_pdffile()

    files = os.listdir()
    for i in range(1, 13):
        j = 0
        wfiles = fnmatch.filter(files, f"w{i}*.aqt")
        if not wfiles:
            exit()
        for file in wfiles:
            j += 1
            well_num = get_wellnum(2, file)
            print(f'{well_num}-{j}  - {file}')
            mainjob(i, j, file)


if __name__ == "__main__":
	main_process()




















