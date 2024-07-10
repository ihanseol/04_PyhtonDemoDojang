;~ #Persistent
#Include "exit_reload.ahk"


PathCombine(dir, file) {
    dest := Buffer(260, 1) ; MAX_PATH ; V1toV2: if 'dest' is a UTF-16 string, use 'VarSetStrCapacity(&dest, 260)'
    DllCall("Shlwapi.dll\PathCombineA", "UInt", dest, "UInt", dir, "UInt", file)
    Return dest
}



SortResults(coords) {
	Loop{
		swapped := 0
		Loop coords.MaxIndex() - 1
			if (coords[A_Index].x > coords[A_Index + 1].x) {
				coords.InsertAt(A_Index, coords[A_Index + 1])
				coords.RemoveAt(A_Index + 2)
				swapped := 1
			}
	} until !swapped
}



ImageSearchAll(imageFile, x1:=0, y1:=0, x2:="Screen", y2:="Screen", var:=0) {
	x2 := x2 = "Screen" ? A_ScreenWidth : x2
	y2 := y2 = "Screen" ? A_ScreenHeight : y2
	found := []
	y := y1
	Loop{
		x := x1
	    lastFoundY := 0
		Loop{
			ErrorLevel := !ImageSearch(&foundX, &foundY, x, y, x2, y2, "*" var " " imageFile)
			if (ErrorLevel = 2)
				return -1
			if !ErrorLevel {
				if (lastFoundY = 0 || lastFoundY = foundY) {
					found.Push({x: foundX, y: foundY})
					x := foundX + 1
					lastFoundY := foundY
				} else
					break
			}
		} until ErrorLevel
		y := lastFoundY + 1
	} until (x = x1) && ErrorLevel
	return found
}


; == Functions ==
DoSearch(){

    WinTitle := "DaVinci Resolve by Blackmagic Design - 17.2.1"

    WinActivate(WinTitle)

    Dots := ImageSearchAll("dot.png", 1450, 1550, 2400, 2050, 6)

    SortResults(Dots)

    for Each, Dot in Dots {
        WinActivate(WinTitle)
        MouseMove(Dot.x + 1, Dot.y + 8)
        MsgBox("Cursor is pointing at dot #" A_Index ".`n`nClick 'OK' or press 'Enter' for next dot.", "Result " A_Index, "")
    }
}



^!A::
{
    xx := 1
    yy := 2

    x := xx + 130
    y := yy + 13

    MsgBox("x: " . x . "`ny: " . y)

    ; Alternatively, you can use the following MsgBox command:
    ; MsgBox, % "x: " x "`ny: " y

    return
}


^d:: ; Define a hotkey (Ctrl + D) to search and click the image
{
    ; Step 1: Capture the screenshot of the current window

    Run("msedge.exe https://www.google.co.kr/")
    Sleep(1000)

    CoordMode("Pixel", "Screen")
    CoordMode("Mouse", "Screen")
    ;~ WinGetPos, , , Width, Height, A

    Try {

        ErrorLevel := !ImageSearch(&FoundX, &FoundY, 0, 0, A_ScreenWidth, A_ScreenHeight, "google_lens.png")
        MouseClick("left", FoundX, FoundY)
        Sleep(1000)

    } Catch e
        Throw e


    Try {

        ErrorLevel := !ImageSearch(&FoundX, &FoundY, 0, 0, A_ScreenWidth, A_ScreenHeight, "pasteimage.png")
        MouseClick("left", FoundX, FoundY)
        Sleep(1000)

    } Catch e
        Throw e

    Send("^v")
    Sleep(1000)


CoordMode("Pixel", "Screen")

Try {
    ; Take a screenshot of the area where the text is expected to appear
    ; Adjust the coordinates to match the area on your screen
    CoordMode("Pixel", "Screen")
    ErrorLevel := !ImageSearch(&FoundX, &FoundY, 0, 0, A_ScreenWidth, A_ScreenHeight, "*32 translate.png")

    ; Check if text was found
    if (ErrorLevel = 0) {
        MsgBox("Text found at X: " FoundX ", Y: " FoundY)
    } else {
        MsgBox("Text not found.")
    }

    Sleep(1000)
} Catch e {
    MsgBox("Error: " . e.Message)
    Throw
}

    Return
}
