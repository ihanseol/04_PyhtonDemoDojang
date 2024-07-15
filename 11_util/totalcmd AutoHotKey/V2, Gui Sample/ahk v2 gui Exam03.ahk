wnd := Gui()
wnd.SetFont("cWhite s12", "Segoe UI")
wnd.Add("Text", "w90 h40 Background7D00AB 0x201 +Border", "Click this").OnEvent("Click", (*) => MsgBox("Clicked"))
wnd.Show()