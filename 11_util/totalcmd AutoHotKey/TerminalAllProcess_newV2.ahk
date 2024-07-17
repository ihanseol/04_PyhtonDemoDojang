
#Requires AutoHotkey v2.0
#SingleInstance

; Define the process name pattern to match
process_name_pattern := "autohotkey"

; Iterate over all running processes
for process, pid in ComObjGet("winmgmts:").ExecQuery("SELECT Name, ProcessId FROM Win32_Process")
{
    ; Check if the process name starts with the defined pattern and ends with ".exe"
    if (InStr(process.Name, process_name_pattern, CaseSensitive := 0) && InStr(process.Name, ".exe", CaseSensitive := 0))
    {
        ; Terminate the process
        ProcessClose(process.ProcessId)
        ProcessWaitClose(process.ProcessId)
        ;~ MsgBox, 0, Terminated Process, % "Terminated: " process.Name " (PID: " process.ProcessId ")"
    }
}

MsgBox("All processes matching the pattern have been terminated.", "Processes Terminated", 0)
