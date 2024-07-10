#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
;SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

;FormatTime, CurrentDateTime,, MMMM d, yyyy HH:mm:ss
FormatTime, CurrentDateTime,, yyyy MMMM d, HH:mm:ss

; Input Korean date and time
KoreanDateTime := CurrentDateTime
RegExMatch(KoreanDateTime, "(\d+) (\d+)¿ù (\d+), (\d+):(\d+):(\d+)", Match)

; Convert month number to English name
MonthNames := ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
Month := MonthNames[Match2]

SendInput %CurrentDateTime%, %Month%

return

