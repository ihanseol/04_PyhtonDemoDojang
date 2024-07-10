;~ #Persistent
#Include exit_reload.ahk

^!p::MainJob()   ; Ctrl+Alt+p
^!i::Test()      ; Ctrl+Alt+p



MainJob()
{

    FindExcelPopUP()
    return

}


FindExcelPopUP() {
    ; Define the filename of the image to search for
    imageFilename := "C:\Users\minhwasoo\Downloads\excel.jpg"

    Loop, 50
        {
            CoordMode, Pixel, Window
            ImageSearch, FoundX, FoundY, 0, 0, 1920, 1200, imageFilename
            If ErrorLevel = 0
                SoundBeep
            Sleep, 7000
        }
        Until ErrorLevel = 0
        If (ErrorLevel = 0)
        {
        }
        
}


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




