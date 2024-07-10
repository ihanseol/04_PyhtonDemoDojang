; Replace F1 with your preferred hotkey
F1::
{ ; V1toV2: Added bracket
    CurrentDateTime := FormatTime(, "yyyy-MM-dd HH:mm:ss")
    SendInput(CurrentDateTime)
return
} ; V1toV2: Added bracket in the end
