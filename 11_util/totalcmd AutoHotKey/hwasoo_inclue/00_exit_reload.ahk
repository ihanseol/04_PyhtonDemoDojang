

^!R::      ; CTRL + ALT + R
Reload, "c:\Users\minhwasoo\Downloads\search image.ahk"
Return

^e::exitapp


^P::  ; CTRL + p
clipboard =
send, ^c
;~ Send, % "%" . Clipboard . "%"
send,%  WrapWithPercent(Clipboard)
OutputDebug A_Now ': Because the window "' TargetWindowTitle '" did not exist, the process was aborted.'
MsgBox,%  Clipboard

Return

WrapWithPercent(text) {

    if InStr(text, "%")
    {
        ;~ StringReplace, text, text, `%, , All
        text := StrReplace(text, "%", "")
        return text
    }
    else
    {
        return "%" . text . "%"
    }
}

DebugMessage(str)
{
 global h_stdout
 DebugConsoleInitialize()  ; start %console% window if not yet started
 str .= "`n" ; add line feed
 DllCall("WriteFile", "uint", h_Stdout, "uint", &str, "uint", StrLen(str), "uint*", BytesWritten, "uint", NULL) ; write into the console

 WinSet, Bottom,, ahk_id %h_stout%  ; keep % on bottom
}

DebugConsoleInitialize()
{
   global h_Stdout     ; Handle for console
   static is_open = 0  ; toogle whether opened before
   if (is_open = 1)     ; yes, so don't open again
     return

   is_open := 1
   ; two calls to open, no error check (it's debug, so you know what you are doing)
   ;~ DllCall("AttachConsole", int, -1, int)
   ;~ DllCall("AllocConsole", int)

   dllcall("SetConsoleTitle", "str","Paddy Debug Console")    ; Set the name. Example. Probably could use a_scriptname here
   h_Stdout := DllCall("GetStdHandle", "int", -11) ; get the handle
   WinSet, Bottom,, ahk_id %h_stout%      ; make sure it's on the bottom

    ;~ WinActivate,Lightroom
   return
}


;~ ^!z::				;% to test with
;~ clipboard =			;clear the clipboard
;~ send, ^c		;copy any selected.  unless there is a reason I would use sendinput
;~ msgbox,,, %clipboard%		;test if anything is there
;~ return



;~ ^!p:: ; Define a hotkey (Ctrl + Alt + P) to wrap selected text with "%"
;~ {
    ;~ ; Save the current clipboard contents
    ;~ ClipboardBackup := ClipboardAll

    ;~ ; Copy the selected text to clipboard
    ;~ Send, ^c
    ;~ ClipWait, 1

    ;~ ; Check if text is copied
    ;~ if ErrorLevel
    ;~ {
        ;~ MsgBox, No text is selected.
        ;~ return
    ;~ }

    ;~ ; Wrap the selected text with "%"
    ;~ WrappedText := WrapWithPercent(Clipboard)

    ;~ ; Replace the selected text with the wrapped text
    ;~ Clipboard := WrappedText
    ;~ Send, ^v

    ;~ ; Restore the clipboard
    ;~ Clipboard := ClipboardBackup
    ;~ ClipboardBackup =

    ;~ return
;~ }







