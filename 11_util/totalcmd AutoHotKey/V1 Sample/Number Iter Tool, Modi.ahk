;**************************************************************************************
; Author:               How To Work From Home                                         *
; Script Function:      Iteration Tool that prints numbers based on Radio Button      *
;**************************************************************************************

#NoEnv                                                                            ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn                                                                           ; Enable warnings to assist with detecting common errors.
SendMode Input                                                                    ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%                                                       ; Ensures a consistent starting directory.
filePath := A_ScriptFullPath                                                      ; Returns the full path to this file


;**************************************** Configurations for Popup Box ****************************************
Gui, Font, s13, Tahoma                                                            ; Message font family and size
Gui, Add, Text, , Please enter the number of times you would like to loop:        ; Text above Input box
Gui, Font, s13, Tahoma                                                            ; Font size and type
Gui, Add, Edit, vNUM w335 Number,                                                 ; Input box - only number allowed
Gui, Add, Text, xm, H=Horizontal --         V=Vertical |

Gui, Add, Radio, vMyRadioCommaH xm, -- H: Comma ,                                  ; Radio buttons
Gui, Add, Radio, vMyRadioSpaceH xm, -- H: Space
Gui, Add, Radio, vMyRadioTabH xm, -- H: Tab
Gui, Add, Radio, vMyRadioPipeH xm, -- H: Pipe |
Gui, Add, Radio, vMyRadioPeriodH xm, -- H: Period .
Gui, Add, Radio, vMyRadioCommaV xm, | V: Comma ,
Gui, Add, Radio, vMyRadioSpaceV xm, | V: Space
Gui, Add, Radio, vMyRadioTabV xm, | V: Tab
Gui, Add, Radio, vMyRadioPipeV xm, | V: Pipe |
Gui, Add, Radio, vMyRadioPeriodV xm, | V:  Period .
Gui, Add, Radio, vMyRadioParenthesesV Checked xm, | V: Parentheses )

Gui, Add, Button, default xm, OK                                                  ; OK button selected by default
Gui, Add, Button, x+m, Quit                                                       ; Quit Button
Gui, Add, Button, x+m, Edit                                                       ; Edit Button
Gui, Show, , Iteration Number Tool                                                ; Title of Popup Box
Return

ButtonOK:
Gui, Submit


;**************************************** Logic after OK button is clicked ****************************************
OnSelect:
Gui, Submit, nohide

If (MyRadioCommaH = 1)
{
	If (NUM != "") {
		Loop % NUM {
		Send %A_Index%{,}
		}
	}
}

If (MyRadioSpaceH = 1)
{
	If (NUM != "") {
		Loop % NUM {
		Send %A_Index%{Space}
		}
	}
}

If (MyRadioTabH = 1)
{
	If (NUM != "") {
		Loop % NUM {
		Send %A_Index%{Tab}
		}
	}
}

If (MyRadioPipeH = 1)
{
	If (NUM != "") {
		Loop % NUM {
		Send %A_Index%{|}
		}
	}
}

If (MyRadioPeriodH = 1)
{
	If (NUM != "") {
		Loop % NUM {
		Send %A_Index%{.}
		}
	}
}

If (MyRadioCommaV = 1)
{
	If (NUM != "") {
		Loop % NUM {
		Send %A_Index%{,}{Enter}
		}
	}
}

If (MyRadioSpaceV = 1)
{
	If (NUM != "") {
		Loop % NUM {
		Send %A_Index%{Space}{Enter}
		}
	}
}

If (MyRadioTabV = 1)
{
	If (NUM != "") {
		Loop % NUM {
		Send %A_Index%{Tab}{Enter}
		}
	}
}

If (MyRadioPipeV = 1)
{
	If (NUM != "") {
		Loop % NUM {
		Send %A_Index%{|}{Enter}
		}
	}
}

If (MyRadioPeriodV = 1)
{
	If (NUM != "") {
		Loop % NUM {
		Send %A_Index%{.}{Space}{Enter}
		}
	}
}

If (MyRadioParenthesesV = 1)
{
	If (NUM != "") {
		Loop % NUM {
		Send %A_Index%{)}{Space}{Enter}
		}
	}
}
Return:
ExitApp


;**************************************** Button Edit logic ****************************************
ButtonEdit:
MsgBox, 4, Warning!!!, Are you sure you want to Edit this File?
IfMsgBox Yes
	Run, notepad++.exe "%filePath%"                                               ; Edit in Notepad++
	;Run, notepad.exe "%filePath%"                                                ; Edit in default Notepad
else
Return



;**************************************** Exiting App ****************************************
GuiClose:
ExitApp

Quit:
ExitApp

esc::ExitApp						                                              ; Press Esc key to abort application

ButtonQuit:
ExitApp

Return