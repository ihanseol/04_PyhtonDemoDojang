import os
import time
import glob
import fnmatch
import copy
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


def delete_exisiting_pdffile():
	dir_path = os.path.expanduser("~\\Documents\\")

	for filename in os.listdir(dir_path):
		if filename.endswith(".pdf"):
			os.remove(dir_path + filename)

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

def change_filename(): 
	directory = "d:\\05_Send\\"
	for filename in os.listdir(): 
		if filename.endswith(".aqt"):
			name, ext = os.path.splitext(filename)
			if "- 복사본" in name:
				new_name = name.replace(" - 복사본", "_01") + ext
				os.rename(directory + filename, directory + new_name)

	# for file_name in glob.glob('*.aqt'):
	# 	print(file_name)

def remove_extension(file_name):
	return os.path.splitext(file_name)[0]


def mainjob(well, i, filename):
	# file_path = os.path.abspath(filename)
	os.startfile(program_path)
	time.sleep(0.5)
	pyautogui.hotkey('ctrl', 'o')
	pyautogui.typewrite(filename)
	pyautogui.press('enter') 
	time.sleep(0.6)

	printpdf(f'a{well}-{i}')
	setview_report()
	printpdf(f'p{well}-{i}')
	exit_program()
	


def get_wellnum(mode, f):
	# 1 -- return 'w1'
	# else -- return 1
	if mode == 1:
		return f.split("_")[0]
	else:
		well = f.split("_")[0]
		return int(well[1:])



def main_process():
	change_filename()
	delete_exisiting_pdffile()

	files = os.listdir()
	for i in range(1,13):
		j = 0
		wfiles = fnmatch.filter(files, f"w{i}*.aqt")
		if not wfiles: exit()
		for file in wfiles:
			j += 1
			print(f'{get_wellnum(2,file)}-{j}  - {file}')
			mainjob(i, j, file)


if __name__ == "__main__":
	main_process()




















