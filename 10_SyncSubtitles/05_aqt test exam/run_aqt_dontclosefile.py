import os, time, glob
import fnmatch
import copy, argparse
import pyautogui

program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
isAqtOpen = False

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
	global isAqtOpen
	if not isAqtOpen:
		os.startfile(program_path)
		isAqtOpen = True
		
	time.sleep(0.3)
	pyautogui.hotkey('ctrl', 'o')
	pyautogui.typewrite(filename)
	pyautogui.press('enter') 
	time.sleep(0.3)

	printpdf(f'a{well}-{i}')
	setview_report()
	printpdf(f'p{well}-{i}')
	# exit_program()
	


def get_wellnum(mode, f):
	# 1 -- return 'w1'
	# else -- return 1
	if mode == 1:
		return f.split("_")[0]
	else:
		well = f.split("_")[0]
		return int(well[1:])


def shutdown_apps(n):
	print('Enter Shutdown Process ...')
	pyautogui.hotkey('alt', 'f4')	
	for i in range(1, n+1):		
		pyautogui.press('n') 	
		print(f'closing window {i} ... ')	


def main_process():
	change_filename()
	delete_exisiting_pdffile()

	files = os.listdir()
	aqtfiles = [f for f in os.listdir() if f.endswith('.aqt')]
	print(f'aqtfiles : {len(aqtfiles)}')

	for i in range(1,13):
		j = 0
		wfiles = fnmatch.filter(files, f"w{i}*.aqt")
		if not wfiles: return len(aqtfiles)			
		for file in wfiles:
			j += 1
			print(f'{get_wellnum(2,file)}-{j}  - {file}')
			mainjob(i, j, file)

if __name__ == "__main__":
	n = main_process()
	print('\n'*1)
	print(f'Process end .... return value from main_process is {n}')
	print('Shutdown AQTW32  Application ...')
	print('\n'*1)
	shutdown_apps(n)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['sub', 'mov'], help="Select 'sub' or 'mov' mode.")
    args = parser.parse_args()

    main_job(args.mode)

if __name__ == "__main__":
    main()
















