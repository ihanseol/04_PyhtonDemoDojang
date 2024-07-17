/*

2024, 7월 17, 수요일 5:46 오후

이것은, 디버그 윈도우로 사용하기 위해서 만듬
콘솔 아웃풋이 적절한것을 못찾아서
그냥 리스트박스를 띠우고
거기에다가 메시지를 추가하는 형태로 구현하고자 함 ..


*/


#Requires AutoHotkey v2
#SingleInstance

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