#Requires AutoHotkey v2
#SingleInstance force

result := "Command line arguments:`n`n"
for index, arg in A_Args {
result .= "Argument " . index . ": " . arg . "`n"
}

MsgBox(result)