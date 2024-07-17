#Requires AutoHotkey v1
#SingleInstance
#Persistent
;~ SetTimer, WatchExcelPopup, 100
;~ Return



loop
{

WatchExcelPopup:
    ; Check if Excel is active
    IfWinActive, ahk_class XLMAIN
    {
	SoundBeep 750, 500
        ; Check for any popup windows in Excel
        ;~ IfWinExist, ahk_class #32770 ; #32770 is the class for dialog boxes
	IfWinExist, Microsoft Excel
        {
            ; Activate the popup window
	    SoundBeep
            WinActivate
            ; Send the Enter key
            Send, {Enter}
        }
    }

}


^e::
{
    ExitApp
}





