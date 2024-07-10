#include <WinAPI.au3>

Global Const $MAX_PATH = 260

Func PathCombine($dir, $file)
    Local $dest = DllStructCreate("char[261]")
    DllCall("Shlwapi.dll\PathCombineA", "ptr", DllStructGetPtr($dest), "str", $dir, "str", $file)
    Return DllStructGetData($dest, 1)
EndFunc

Func SortResults(ByRef $coords)
    Local $swapped
    Do
        $swapped = False
        For $i = 0 To UBound($coords) - 2
            If $coords[$i].x > $coords[$i + 1].x Then
                _ArraySwap($coords, $i, $i + 1)
                $swapped = True
            EndIf
        Next
    Until Not $swapped
EndFunc

Func ImageSearchAll($imageFile, $x1 = 0, $y1 = 0, $x2 = "Screen", $y2 = "Screen", $var = 0)
    Local $x2Coord = ($x2 = "Screen") ? @DesktopWidth : $x2
    Local $y2Coord = ($y2 = "Screen") ? @DesktopHeight : $y2
    Local $found = []
    Local $y = $y1
    Do
        Local $x = $x1
        Local $lastFoundY = 0
        Do
            $ErrorLevel = _ImageSearch($x, $y, $x2Coord, $y2Coord, $imageFile, $var)
            If $ErrorLevel = 2 Then Return -1
            If Not $ErrorLevel Then
                If $lastFoundY = 0 Or $lastFoundY = $foundY Then
                    $found[$found[0] + 1] = ObjCreate("Scripting.Dictionary")
                    $found[$found[0]].Add("x", $foundX)
                    $found[$found[0]].Add("y", $foundY)
                    $x = $foundX + 1
                    $lastFoundY = $foundY
                Else
                    ExitLoop
                EndIf
            EndIf
        Until $ErrorLevel
        $y = $lastFoundY + 1
    Until ($x = $x1) And $ErrorLevel
    Return $found
EndFunc

Func DoSearch()
    Local $WinTitle = "DaVinci Resolve by Blackmagic Design - 17.2.1"
    WinActivate($WinTitle)
    Local $Dots = ImageSearchAll("dot.png", 1450, 1550, 2400, 2050, 6)
    SortResults($Dots)
    For $i = 1 To $Dots[0]
        WinActivate($WinTitle)
        MouseMove($Dots[$i].x + 1, $Dots[$i].y + 8)
        MsgBox(0, "Result " & $i, "Cursor is pointing at dot #" & $i & ".`n`nClick 'OK' or press 'Enter' for next dot.")
    Next
EndFunc

HotKeySet("^!a", "MyFunc")

Func MyFunc()
    Local $xx = 1
    Local $yy = 2
    Local $x = $xx + 130
    Local $y = $yy + 13
    MsgBox(0, "", "x: " & $x & @CRLF & "y: " & $y)
EndFunc

HotKeySet("^d", "SearchAndClickImage")

Func SearchAndClickImage()
    Run("msedge.exe https://www.google.co.kr/")
    Sleep(1000)
    Local $FoundX, $FoundY
    Local $error = _ImageSearch(0, 0, @DesktopWidth, @DesktopHeight, "google_lens.png", $FoundX, $FoundY)
    If Not $error Then
        MouseClick("left", $FoundX, $FoundY)
        Sleep(1000)
    EndIf
    $error = _ImageSearch(0, 0, @DesktopWidth, @DesktopHeight, "pasteimage.png", $FoundX, $FoundY)
    If Not $error Then
        MouseClick("left", $FoundX, $FoundY)
        Sleep(1000)
    EndIf
    Send("^v")
    Sleep(1000)
    $error = _ImageSearch(0, 0, @DesktopWidth, @DesktopHeight, "*32 translate.png", $FoundX, $FoundY)
    If Not $error Then
        MsgBox(0, "", "Text found at X: " & $FoundX & ", Y: " & $FoundY)
    Else
        MsgBox(0, "", "Text not found.")
    EndIf
EndFunc

While True
    Sleep(100)
WEnd
