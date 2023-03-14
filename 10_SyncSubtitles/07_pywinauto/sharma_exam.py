from pywinauto import application

app = application.Application()
app.start("Notepad.exe")
app.Notepad.menu_select("File -> Open")
app.Open.Edit.set_edit_text('test.txt')
app.Open.Open.click(double=True)

print (app.Notepad.Edit.window_text())

