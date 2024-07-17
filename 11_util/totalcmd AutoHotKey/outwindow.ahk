#Requires AutoHotkey v2

global myGui := ""
global ListBox := ""
global DebugArray := ["This is Debug Array"]
global sum := 0

if A_LineFile = A_ScriptFullPath
{
    if !A_IsCompiled
    {
        myGui := Constructor()
        myGui.Show("w973 h594")
    }
}

Constructor() {
    myGui := Gui()
    myGui.SetFont("s10", "Consolas")
    ListBox := myGui.Add("ListBox", "x8 y48 w945 h529", DebugArray)
    myGui.OnEvent('Close', (*) => ExitApp())
    myGui.Title := "Window"
    return myGui
}

^!a:: {
	global sum

    sum += 1
    DebugArray.Push("This is " . sum)

    if myGui
        ListBox := myGui.Add("ListBox", "x8 y48 w945 h529", DebugArray)
}