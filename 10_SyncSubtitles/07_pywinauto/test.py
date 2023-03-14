import pywinauto, time
from pywinauto.application import Application
from pywinauto.controls.win32_controls import ButtonWrapper


app=Application().start(cmd_line=r"c:\WHPA\AQTEver3.4(170414)\AQTW32.EXE")
time.sleep(1)
app.aqtesolveforwindows.menu_item("File->Open").click()
filename = "w1_02_long.aqt"
app.열기["파일 이름(N):Edit"].type_keys(filename)
time.sleep(1)
# edit_ctrl = app.UntitledNotepad.child_window(control_type=UIAWrapper.EditControlTypeId)
app.열기.type_keys('%o')
time.sleep(1)
#app[f'{filename}'].type_keys("^p")

fapp = app['AQTESOLV for Windows - w1_02_long.aqt']
fapp.type_keys("^p")

# whandle=pywinauto.findwindows.find_windows(title="인쇄")[0]
# fapp.인쇄.확인.click()


#control = fapp.window(class_name='Button10')
#control_wrapper = ButtonWrapper(control)
#control_wrapper.click()

# fapp["인쇄"].type_keys("{ENTER}")

w = app.windows(class_name='#32770')
window_list[0].click()

time.sleep(1)