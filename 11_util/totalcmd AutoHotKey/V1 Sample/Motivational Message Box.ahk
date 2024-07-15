;***************************************************************************************;
; Title:          Motivational Message Box                                              ;
; Description:    AutoHotkey Message Box with randomly generated motivational quotes    ;
; Author:         How To Work From Home                                                 ;
;***************************************************************************************;


;**************************************** Default environment variables ****************************************
#NoEnv                                                                             ; Recommended for performance and compatibility with future AutoHotkey releases
SendMode Input                                                                     ; Recommended for new scripts due to its superior speed and reliability
SetWorkingDir %A_ScriptDir%                                                        ; Ensures a consistent starting directory
filePath := A_ScriptFullPath                                                       ; Returns the full path to this file


;**************************************** CHANGE ME ****************************************
motivationFile := "C:\temp\AutoHotKey\GUI Motivational Messages\Quotes.txt"        ; Change to the location of your motivational text file


;**************************************** Logic for generating random quotes ****************************************
Loop, Read, %motivationFile%
	Total_Lines = %A_Index%
Random, Random_Number, 1, %Total_Lines%
Loop, Read, %motivationFile%
	{
		If A_Index = %Random_Number%
			{
				loopreadmessage = %A_LoopReadLine%
				clipboard = %A_LoopReadLine%                                       ; Enable/disable storing THE quote on clipboard
					Break
			}
	}


;**************************************** Message box layout and look ****************************************
Gui, -MinimizeBox -MaximizeBox
Gui, Font, s20, Tahoma                                                             ; Message font family and size
Gui, Add, Text, w1000, % loopreadmessage                                           ; Width of Message box and calling the loopreadmessage
Gui, Font, s10, Verdana                                                            ; Buttons font family and size
Gui, Add, Button, default xm, OK                                                   ; Will be selected by default
Gui, Add, Button, x+m, Edit
Gui, Add, Button, x+m, Reload-F12
Gui, Add, Button, x+m, Quit-Esc
Gui, Show,, Greetings!                                                             ; Message box title
Gui, +LastFound
WinWaitClose
ExitApp


;**************************************** Button Edit logic ****************************************
ButtonEdit:
MsgBox, 4, Warning!!!, Are you sure you want to Edit this File?
IfMsgBox Yes
	;Run, notepad++.exe "%filePath%"                                               ; Edit in Notepad++
	Run, notepad.exe "%filePath%"                                                  ; Edit in default Notepad
else
Return


;**************************************** Buttons action logic ****************************************
ButtonReload-F12:                                                                  ; Press F12 button to reload the app
F12::reload
Return

ButtonOK:
ExitApp
Return

Esc::ExitApp                                                                       ; Press Esc button to Exit the app

GuiClose:
ExitApp
Return

ButtonQuit-Esc:
ExitApp
Return