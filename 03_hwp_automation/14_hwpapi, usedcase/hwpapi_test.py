from hwpapi.core import App

app = App()

app.open(r'd:\05_Send\iyong(field).hwp')
hwp = app.get_hwnd()

app.api.Run('SelectAll')
app.api.Run('Copy')
app.api.MovePos(3)

app.api.Run('Paste')
app.api.MovePos(3)



# action = app.actions.InsertText()
# p = action.pset
# p.Text = "Hello\r\nWorld!"
# action.run()


