import os   
import time
import pyautogui
import shutil

from os import listdir
from os.path import isfile, join



def convert_photo(count, delay):
    
    if count == 0 :
        time.sleep(3)

    pyautogui.keyDown('alt')
    time.sleep(delay)
    pyautogui.press('o')
    time.sleep(delay)
    pyautogui.keyUp('alt')
    time.sleep(delay)

    if count==0 :
        pyautogui.moveTo(1071, 259)
        time.sleep(delay)
        pyautogui.click()
        pyautogui.typewrite('D:\\05_Send')
        time.sleep(delay)
        pyautogui.press('enter')  
        time.sleep(delay)


    pyautogui.moveTo(699, 363)
    time.sleep(delay)
    pyautogui.click()
    time.sleep(delay)
    pyautogui.press('enter')  
    time.sleep(delay*2)


    #save
    pyautogui.moveTo(53, 145)
    time.sleep(delay)
    pyautogui.click()
    time.sleep(delay*2)
    pyautogui.moveTo(699, 363)
    time.sleep(delay)
    pyautogui.click()
    time.sleep(delay)
    pyautogui.press('enter')  
    time.sleep(delay)
    pyautogui.press('y')
    time.sleep(delay*2)


def listMyFile():
    mypath = "D:\\05_Send"
    count = 0

    os.chdir(mypath)
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    print(" ready 5 second ....")
    time.sleep(5)

    for i in onlyfiles:
        convert_photo(count, 0.5)
        count = count + 1
        print("file : ",i," moving ...")
        filemove(i)
        time.sleep(1)


def filemove(filename):        
    src = 'd:\\05_Send\\'
    dir = 'c:\\Users\\minhwasoo\\Downloads\\'
    shutil.move(src + filename, dir + filename)



def main():
    listMyFile()

if __name__ == "__main__":
    main()
    #convert_photo()



