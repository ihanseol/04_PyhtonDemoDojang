CoordMode, Pixel, Window  ; Sets coordinate mode to use screen coordinates

Loop
{
    ; Searches for the image "Excel01.jpg" within the combined screen coordinates of both monitors
    ImageSearch, FoundX, FoundY, 0, 0, A_ScreenWidth, A_ScreenHeight, c:\Program Files\totalcmd\AqtSolv\Excel01.jpg

    ; Checks if the ImageSearch command was successful (ErrorLevel = 0 means success)
    If ErrorLevel = 0
    {
        ; Simulates pressing the Enter key
        Send, {Enter}
        SoundBeep
        MsgBox, %FoundX%, %FoundY%
        Sleep, 1000  ; Optional: Add a delay to wait before searching again (in milliseconds)
    }

    ; Optional: Add a longer sleep to reduce CPU usage if needed
    Sleep, 500  ; Adjust the sleep time based on how frequently you want to check for the image
}
