;~ #Persistent
#Include exit_reload.ahk

^!p::MainJob()   ; Ctrl+Alt+p
^!i::Test()      ; Ctrl+Alt+p



MainJob()
{

    ;~ ExcelToFrontAndCloseWarning()
    FindExcelPopUP()
    ;~ GetExcelClass()
    return

}

; ~ FindExcelPopUP() {
;     ~ ; Define the filename of the image to search for
;     ~ imageFilename := "excel.jpg"

;     ~ ; Capture a screenshot of the secondary screen
;     ~ CoordMode, Pixel, Screen
;     ~ WinGetPos, X, Y, Width, Height, ahk_class XLMAIN ; Replace XLMAIN with the class of your Excel window
;     ~ ImageSearch, FoundX, FoundY, X, Y, Width, Height, *25 %imageFilename% ; Adjust the tolerance as needed

;     ~ ; Check if the image was found
;     ~ if ErrorLevel = 0 {
;         ~ MsgBox, Image found at coordinates (%FoundX%, %FoundY%)
;     ~ } else {
;         ~ MsgBox, Image not found.
;     ~ }

;     ~ return
; ~ }


;~ GetExcelClass(){

    ;~ WinGetClass, ExcelClass, ahk_exe EXCEL.EXE
    MsgBox, The class of the Excel window is %ExcelClass%.

    ;~ return ExcelClass

;~ }

;~ FindExcelPopUP() {
    ;~ ; Define the filename of the image to search for
    ;~ imageFilename := "excel.jpg"

    ;~ ; Capture a screenshot of the secondary screen


    ;~ ExcelClass := GetExcelClass()
    ;~ MsgBox, %ExcelClass%

    ;~ CoordMode, Pixel, Screen

    ;~ WinGetPos, X, Y, Width, Height, ahk_class XLMAIN ; Replace XLMAIN with the class of your Excel window

    ;~ WinGetPos, X, Y, Width, Height, %ExcelClass%
    ;~ ImageSearch, FoundX, FoundY, X, Y, Width, Height, *25 %imageFilename% ; Adjust the tolerance as needed

    ;~ ; Check if the image was found
    ;~ if (ErrorLevel = 0) {
        ;~ MsgBox, Image found at coordinates (%FoundX%, %FoundY%)
    ;~ } else {
        ;~ MsgBox, Image not found.
    ;~ }
;~ }


; ---------------------------------------------------------------------------------------------------------

;~ GetExcelClass() {
    ;~ if !WinExist("ahk_exe EXCEL.EXE") {
        ;~ MsgBox, Error: Excel window not found.
        ;~ return ""  ; Return an empty string if Excel window is not found
    ;~ }

    ;~ WinGetClass, ExcelClass, ahk_exe EXCEL.EXE
    ;~ return ExcelClass
;~ }

;~ FindExcelPopUP() {
    ;~ ; Define the filename of the image to search for
    ;~ imageFilename := "excel.jpg"

    ;~ ; Get the class of the Excel window
    ;~ ExcelClass := GetExcelClass()
    ;~ if (ExcelClass = "") {
        ;~ MsgBox, Error: Excel class not retrieved.
        ;~ return
    ;~ }

    ;~ ; Capture a screenshot of the secondary screen
    ;~ CoordMode, Pixel, Screen
    ;~ WinGetPos, X, Y, Width, Height, %ExcelClass%
    ;~ if (ErrorLevel != 0) {
        ;~ MsgBox, Error: Failed to get position of Excel window.
        ;~ return
    ;~ }

    ;~ ; Search for the image within the Excel window area
    ;~ ImageSearch, FoundX, FoundY, X, Y, Width, Height, *25 %imageFilename%

    ;~ ; Check if the image was found
    ;~ if (ErrorLevel = 0) {
        ;~ MsgBox, Image found at coordinates (%FoundX%, %FoundY%)
    ;~ } else {
        ;~ MsgBox, Image not found.
    ;~ }
;~ }





; ---------------------------------------------------------------------------------------------------------

FindExcelPopUP() {
    ; Define the filename of the image to search for
    imageFilename := "excel.jpg"

    ; Get the class of the Excel window
    ExcelClass := GetExcelClass()
    if (ExcelClass = "") {
        MsgBox, Error: Excel class not retrieved.
        return
    }

    ; Capture a screenshot of the secondary screen
    CoordMode, Pixel, Screen
    WinGetPos, X, Y, Width, Height, %ExcelClass%
    if (ErrorLevel != 0) {
        MsgBox, Error: Failed to get position of Excel window.
        return
    }

    ; Search for the image within the Excel window area
    ImageSearch, FoundX, FoundY, X, Y, Width, Height, *25 %imageFilename%

    ; Check if the image was found
    if (ErrorLevel = 0) {
        MsgBox, Image found at coordinates (%FoundX%, %FoundY%)
    } else {
        MsgBox, Image not found.
    }
}

GetExcelClass() {
    if !WinExist("ahk_exe EXCEL.EXE") {
        MsgBox, Error: Excel window not found.
        return ""  ; Return an empty string if Excel window is not found
    }

    WinGetClass, ExcelClass, ahk_exe EXCEL.EXE
    return ExcelClass
}

; Call the main function
FindExcelPopUP()





; ---------------------------------------------------------------------------------------------------------



; Function to bring Excel window to the foreground and close the warning window
ExcelToFrontAndCloseWarning() {
    ; Specify the title of the Excel window
    ; You can customize this title to match your Excel window title

    ;~ ExcelTitle := "ahk_class XLMAIN"
    ExcelTitle := "Microsoft Excel"

    ;~ Msgbox, %ExcelTitle%

    ; Activate the Excel window and bring it to the front
    WinActivate, %ExcelTitle%
    WinWaitActive, %ExcelTitle%

    ; Wait for the warning window to appear
    ; Replace "Warning Window Title" with the title of the warning window
    ;~ WinWait, "Excel"

    ; Close the warning window by sending an Enter key press

    Send {Enter}
    SendInput {Enter}
    return

}





; Function to bring Excel window to the foreground
ExcelBringToFront() {
    ; Specify the title of the Excel window
    ; You can customize this title to match your Excel window title
    ExcelTitle :=  "Microsoft Excel"

    ; Activate the Excel window
    WinActivate, %ExcelTitle%
}




MaximizeScreen()
{
    SetTitleMatchMode, 2 ; Allows partial matching of window titles

    if WinExist("ahk_class XLMAIN") ; Checks if an Excel window exists
    {

        WinActivate, ahk_class XLMAIN ; Activates the main window of Excel
        WinWaitActive, ahk_class XLMAIN ; Waits until Excel is active
        WinMaximize ; Maximizes the active window, which will be Excel if it was successfully activated
    }
    else
    {
        MsgBox, Excel is not found ; Displays a message box if Excel is not found
    }

    return
}

; Function to find and activate an Excel window
ActivateExcelWindow() {
    ; Attempt to find an Excel window by its class
    If WinExist("ahk_class XLMAIN") {
        ; If found, activate and bring it to the foreground
        WinActivate
        return True
    } else {
        ; If not found, optionally display a message or take some other action
        MsgBox, Excel window not found.
        return False
    }
}

MoveExcelToPrimaryScreen()
{
    if WinExist("ahk_class XLMAIN")  ; Checks if an Excel window exists
    {
        WinGet, activeWindowID, ID, A  ; Gets the window ID of the active window

        WinRestore, ahk_id %activeWindowID% ; Restore the window if it is minimized or maximized

        ; Get primary monitor's dimensions
        SysGet, MonitorWorkArea, MonitorWorkArea, 1 ; 1 is typically the primary monitor

        ; Move the Excel window to the primary monitor
        WinMove, ahk_id %activeWindowID%, , MonitorWorkAreaLeft, MonitorWorkAreaTop
    }
    else
    {
        MsgBox, Excel is not found  ; Displays a message box if Excel is not found
    }
}


SecondScreenClick()
{

    #NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
    SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.

    ; Set the coordinates for the secondary screen
    ; Replace these coordinates with the actual coordinates of your secondary screen
    SecondaryScreenX := 3974  ; Example: X-coordinate of the secondary screen
    SecondaryScreenY := 773     ; Example: Y-coordinate of the secondary screen

    ; Move the mouse cursor to the secondary screen
    MouseMove, %SecondaryScreenX%, %SecondaryScreenY%

    ; Click to focus on the secondary screen
    Click
    Sleep 500
    Send, {Enter}{Enter}


    return

}


Test() {
    ; Example usage
    if IsExcelOnPrimaryScreen() {
        MsgBox, Excel is on the primary screen.
    } else {
        MsgBox, Excel is on the secondary screen.
    }

    return

}

; Function to determine if Excel window is on primary or secondary screen
IsExcelOnPrimaryScreen() {
    ; Get the position and size of the Excel window
    WinGetPos, X, Y, Width, Height, ahk_class XLMAIN

    ; Get the position and size of the primary screen
    SysGet, PrimaryMonitor, MonitorWorkArea

    ; Check if the Excel window overlaps with the primary screen
    if (X >= PrimaryMonitorLeft && X < PrimaryMonitorRight && Y >= PrimaryMonitorTop && Y < PrimaryMonitorBottom) {
        ; Excel window is on the primary screen
        return true
    } else {
        ; Excel window is not on the primary screen (assuming it's on the secondary screen)
        return false
    }
}





