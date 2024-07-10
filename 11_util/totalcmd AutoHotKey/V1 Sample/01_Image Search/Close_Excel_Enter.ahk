CoordMode, Pixel, Window  ; Sets coordinate mode to use relative coordinates to the active window

Loop
{
    ; Searches for the image "close.png" within the specified screen coordinates
    ImageSearch, FoundX, FoundY, 0, 0, 1920, 1200, c:\Program Files\totalcmd\AqtSolv\excel.png

    ; Checks if the ImageSearch command was successful (ErrorLevel = 0 means success)
    If ErrorLevel = 0
    {
        ; Simulates pressing the Enter key
        Send, {Enter}
        Sleep, 1000  ; Optional: Add a delay to wait before searching again (in milliseconds)
    }

    ; Optional: Add a longer sleep to reduce CPU usage if needed
    Sleep, 500  ; Adjust the sleep time based on how frequently you want to check for the image
}
