CoordMode, Pixel, Window  ; Sets coordinate mode to use relative coordinates to the active window

Loop
{
    ; Searches for the image "close.png" within the specified screen coordinates
    ImageSearch, FoundX, FoundY, 0, 0, 1920, 1200, C:\Users\minhwasoo\Pictures\key.png

    ; Checks if the ImageSearch command was successful (ErrorLevel = 0 means success)
    If ErrorLevel = 0
    {
        ; Clicks at the coordinates where the image was found
        Click, %FoundX%, %FoundY%, Left, 1
	SoundBeep
        Sleep, 1000  ; Optional: Add a delay to wait before searching again (in milliseconds)
    }

    ; Optional: Add a longer sleep to reduce CPU usage if needed
    Sleep, 100  ; Adjust the sleep time based on how frequently you want to check for the image
}
