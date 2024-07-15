wnd := Gui()
wnd.SetFont("cWhite s12", "Segoe UI")
; w90 = width 90
; h40 = height 40
; Background7D00AB = BackgroundColor 7D00AB
; 0x201 = Combination of styles SS_CENTER (0x1) and SS_CENTERIMAGE (0x200)
; +Border = Add a border around the control
Txt := wnd.Add("Text", "w90 h40 Background7D00AB 0x201 +Border", "Click this")
Txt.OnEvent("Click", TextClicked)
wnd.Show()

TextClicked(*) {
    MsgBox "Clicked"
}