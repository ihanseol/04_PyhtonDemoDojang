;==================================================

;an AHK v1 script
;AHK v1 to v2 converter by jeeswg
;additional library
;[first released: 2018-02-21]

;from:
;AHK v1 to AHK v2 converter (initial work) - AutoHotkey Community
;https://autohotkey.com/boards/viewtopic.php?t=36754
;ahk v1 converter.ahk [main script]
;ahk v1 converter lib.ahk [this script]

;==================================================

;JEE_InputBox ;simple version
;JEE_MsgBox ;simple version
;JEE_ArrayToCmd
;JEE_ArrayToFunc
;JEE_CmdParamClean
;JEE_CmdPrepare
;JEE_ColRGBIsBGR
;JEE_Cvt
;JEE_CvtCmdGetList
;JEE_CvtJoin
;JEE_ExpTrim
;JEE_GetSelectedText
;JEE_ObjList
;JEE_ObjPopBlank
;JEE_ObjShuffleFrom
;JEE_StrCount
;JEE_StrJoin
;JEE_StrRept
;JEE_StrUnused
;JEE_WinMergeCompareStrings

;==================================================

;simple version of function
;the full version allows a custom font
JEE_InputBox(vText:="", vDefault:="", vWinTitle:="", vOpt:="")
{
	hWnd := WinGetID("A")
	if (vWinTitle = "")
		SplitPath(A_ScriptName,,,, vWinTitle)
	vRet := InputBox(vText, vWinTitle, vOpt, vDefault) ;[DO NOT CONVERT]
	WinActivate("ahk_id " hWnd)
	return vRet
}

;==================================================

;simple version of function
;the full version allows a custom font
JEE_MsgBox(vText:="Press OK to continue.", vWinTitle:="", vOpt:="")
{
	hWnd := WinGetID("A")
	;note: Ctrl+C on a MsgBox, converts `n to `r`n
	vText := StrReplace(vText, "`r`n", "`n")
	if (vWinTitle = "")
		SplitPath(A_ScriptName,,,, vWinTitle)
	vRet := MsgBox(vText, vWinTitle, vOpt) ;[DO NOT CONVERT]
	WinActivate("ahk_id " hWnd)
	return vRet
}

;==================================================

JEE_ArrayToCmd(oArray, vParams:="")
{
	vOutput := Trim(oArray.1) ","
	Loop, % oArray.Length()-1
	{
		vType := SubStr(vParams, A_Index, 1)
		vTemp := JEE_CmdParamClean(oArray[A_Index+1], vType)
		if (vTemp = "")
			vOutput .= vTemp ","
		else
			vOutput .= " " vTemp ","
	}
	return SubStr(vOutput, 1, -1)
}

;==================================================

JEE_ArrayToFunc(oArray, vParams:="")
{
	if (oArray.Length() = 1)
		return Trim(oArray.1) "()"
	vOutput := Trim(oArray.1) "("
	Loop, % oArray.Length()-1
	{
		vType := SubStr(vParams, A_Index, 1)
		vTemp := JEE_Cvt(oArray[A_Index+1], vType)
		if (A_Index = 1) || (vTemp = "")
			vOutput .= vTemp ","
		else
			vOutput .= " " vTemp ","
	}
	return SubStr(vOutput, 1, -1) ")"
}

;==================================================

JEE_CmdParamClean(vText, vType)
{
	vText := Trim(vText)
	if (SubStr(vText, 1, 2) = "% ")
	|| (vType = "I") || (vType = "O")
		return vText
	;if RegExMatch(vText, "[`` `t;,%]")
	if RegExMatch(vText, "%")
	&& !InStr(vText, "``")
		return "% " JEE_Cvt(vText)
	else
		return vText
}

;==================================================

;find the point where the command ends (assume first CR/LF) [CHECK: improve find end]
;replace commas with delimiter character
;start looking for command vPos within vText
;e.g.
;vText2 := JEE_CmdPrepare(vText, 1, Chr(1), vIsErrorNoEnd)

JEE_CmdPrepare(ByRef vText, vPos, vDelim, ByRef vIsErrorNoEnd)
{
	local oCommaCount,oInQuote,oQuoteCount,vChar,vCharLast,vCharLastX,vDepth,vDoReset,vIsXpn,vLen,vPos2,vPosEnd,vText2
	vIsErrorNoEnd := 0
	vLen := StrLen(vText)
	if !vPosEnd := RegExMatch(vText, "`r|`n",, vPos)
		vPosEnd := vLen+1
	vPosEnd--
	vText2 := SubStr(vText, vPos, vPosEnd-vPos+1)
	if RegExMatch(vText2, "^\w+[ `t]*,")
		vText2 := StrReplace(vText2, ",", vDelim,, 1)
	else if RegExMatch(vText2, "^\w+ ")
		vText2 := StrReplace(vText2, " ", vDelim,, 1)
	else if RegExMatch(vText2, "^\w+`t")
		vText2 := StrReplace(vText2, "`t", vDelim,, 1)
	else
		return vText2
	vPos2 := InStr(vText2, vDelim)
	vText2 := SubStr(vText2, 1, vPos2)
	vPos += vPos2
	vCharLastX := ""
	vIsXpn := 0
	Loop
	{
		vChar := SubStr(vText, vPos, 1)
		if (vPos > vPosEnd)
		{
			vIsErrorNoEnd := 0
			break
		}
		vPos++
		if vIsXpn
		{
			if (vChar = Chr(34))
				oInQuote[vDepth] := !oInQuote[vDepth], oQuoteCount.HasKey(vDepth) ? oQuoteCount[vDepth] += 1 : oQuoteCount[vDepth] := 1
			if (vCharLast = Chr(34))
			&& !(oQuoteCount[vDepth] & 1) && !(vChar = Chr(34))
				oInQuote[vDepth] := 0
			if (vChar ~= "\(|\[") && !oInQuote[vDepth]
				vDepth++
			if (vChar ~= "\)|]") && !oInQuote[vDepth]
				vDepth--
			if (vChar = ",") && !(vCharLast = "``") && !oInQuote[vDepth]
				oCommaCount[vDepth] := oCommaCount[vDepth] ? oCommaCount[vDepth]+1 : 1

			if !(vChar = " ") && !(vChar = "`t")
				vCharLastX .= vChar

			if (vChar = ",") && !(vCharLast = "``") && (vDepth = 1) && !oInQuote[1]
				vText2 .= vDelim, vCharLastX := "", vDoReset := 1, vIsXpn := 0
			else
				vText2 .= vChar
			;if !vDepth
			;	break
		}
		else
		{
			if !(vChar = " ") && !(vChar = "`t")
				vCharLastX .= vChar

			if (vChar = ",") && !(vCharLast = "``")
				vText2 .= vDelim, vCharLastX := ""
			else
				vText2 .= vChar
			if (vCharLastX = "%")
			&& ((vChar = " ") || (vChar = "`t"))
				vIsXpn := 1, vDoReset := 1
		}
		vCharLast := vChar
		if vDoReset
		{
			vDepth := 1
			vDoReset := 0
			oCommaCount := {}, oQuoteCount := {}, oInQuote := {}
		}
	}
	oCommaCount := oQuoteCount := oInQuote := ""
	return vText2
}

;==================================================

;do red/blue colour values match
JEE_ColRGBIsBGR(vNum)
{
	if RegExMatch(vNum, "^0x\d{6}$")
		return (SubStr(vNum, 3, 2) = SubStr(vNum, 7, 2))
	else if RegExMatch(vNum, "^\d+$")
		return ((vNum && 0xFF0000 >> 16) = (vNum && 0xFF))
	else
		return 0
}

;==================================================

;23:38 22/11/2017

;possible types: blank/S, I, O, E, Z, T
;parameters names (SIOE) based on: https://github.com/Lexikos/Scintillua-ahk/blob/master/ahk1.lua
;S: output as "text" or num
;S2: output as "text" or num (same as S, but as num less often)
;I: input variable
;O: output variable
;E: can be an expression
;Z: unchanged (except for cropping leading '% ')
;T: output as "text" or "num"
JEE_Cvt(vText, vType:="")
{
	vText := Trim(vText)
	if (vType = "Z")
		if (SubStr(vText, 1, 2) = "% ")
			return SubStr(vText, 3)
		else
			return vText

	if (vType = "I") && (SubStr(vText, 1, 2) = "% ")
		vText := SubStr(vText, 3)
	if (vType = "O") && (vText = Chr(34) Chr(34))
		return
	if (vType = "I") || (vType = "O")
		return vText

;MsgBox, % vType " [" vText "]"
	;check: handle 'can be an expression'
	if (vType = "E") && (SubStr(vText, 1, 2) = "% ")
		vText := SubStr(vText, 3)
;MsgBox, % vType " [" vText "]"
	if (vType = "E") && RegExMatch(vText, "^%\w+%$")
		return SubStr(vText, 2, -1)
;MsgBox, % vType " [" vText "]"
	if (vType = "E")
		return vText

	if (vType = "S2")
		if (vText = "0")
		|| RegExMatch(vText, "^-?[1-9]\d*$") ;e.g. -123
			return vText

	if !(vType = "T")
	&& !(vType = "S2")
		if RegExMatch(vText, "^-?\d+((\.)?\d+)?$") ;e.g. -123.123
		|| RegExMatch(vText, "^-?0x[\dA-Fa-f]+$") ;e.g. -0x123ABC
			return vText
	if (vText = "") ;blank
		return
	;if (vText = "") ;blank text
	;	return Chr(34) Chr(34)
	if (vText = Chr(34))
		return "Chr(34)"
	if (vText = "%A_Space%")
		return Chr(34) " " Chr(34)

	vText := StrReplace(vText, "%A_Tab%", "``t")
	vUnused := JEE_StrUnused(1, vText)
	vText := StrReplace(vText, "```,", ",")
	vText := StrReplace(vText, "```;", ";")
	vText := StrReplace(vText, " `;", " ```;")
	if (SubStr(vText, 1, 2) = "% ")
		return SubStr(vText, 3)
	vText := StrReplace(vText, "```%", vUnused)
	vText := StrReplace(vText, " ", "%A_Space%")
	vText := RegExReplace(vText, "(?<!%A_Space%)%A_Space%(?!%A_Space%)", " ")

	vOutput := ""
	Loop, Parse, vText, % "%"
	{
		vTemp := A_LoopField
		if (vTemp = "")
			continue
		if (A_Index & 1)
		{
			vTemp := StrReplace(vTemp, Chr(34), Chr(34) " Chr(34) " Chr(34))
			while RegExMatch(vTemp, " \x22\x22 ")
				vTemp := RegExReplace(vTemp, " \x22\x22 ", " ")
			if !(vTemp = "")
				vTemp := Chr(34) vTemp Chr(34)
			vTemp := RegExReplace(vTemp, "^\x22\x22 | \x22\x22$")
			vOutput .= vTemp " "
		}
		else
			vOutput .= Trim(A_LoopField) " "
	}
	vOutput := StrReplace(vOutput, vUnused, "%")
	return Trim(vOutput)
}

;==================================================

JEE_CvtCmdGetList()
{
	;command types:
	;P,,#,# - parameters shuffled
	;XM - need custom replace, parameters modified
	;XP - need custom replace, parameters shuffled
	;R - unchanged, but drop the first parameter (it becomes the return value)
	;U - unchanged
	;X - removed, have an equivalent function
	;XI - removed, if control flow statements
	;XX - removed, have no direct equivalent
	;XS - removed, split (subcommands to separate functions)

	;command info:
	;Cmd=CmdType,NewName,NewOrder,ParamTypes

	;[Thread subcommands not added]
	;Thread-Interrupt
	;Thread-NoTimers
	;Thread-Priority

	;[Transform subcommands: not available]
	;Transform-Deref
	;Transform-FromCodePage
	;Transform-HTML
	;Transform-ToCodePage
	;Transform-Unicode

	;[Transform subcommands: available]
	;Transform-Abs
	;Transform-ACos
	;Transform-Asc
	;Transform-ASin
	;Transform-ATan
	;Transform-BitAnd
	;Transform-BitNot
	;Transform-BitOr
	;Transform-BitShiftLeft
	;Transform-BitShiftRight
	;Transform-BitXOr
	;Transform-Ceil
	;Transform-Chr
	;Transform-Cos
	;Transform-Exp
	;Transform-Floor
	;Transform-Ln
	;Transform-Log
	;Transform-Mod
	;Transform-Pow
	;Transform-Round
	;Transform-Sin
	;Transform-Sqrt
	;Transform-Tan

	vText1 := " ;continuation section
	(LTrim
	[ahk1toahk2]
	ControlMove=P,,234516789,EEEESSSSS
	ControlSend=P,,213456,SSSSSS
	ControlSendRaw=P,,213456,SSSSSS
	ControlSetText=P,,213456,SSSSSS
	GroupAdd=P,,12356,SSSSS
	Sort=XPR
	WinMove=XP
	WinSetTitle=XP

	FileAppend=XM
	FileRead=XMR
	FileSetAttrib=XM
	Input=XMR
	InputBox=XMR
	MsgBox=XM
	PixelGetColor=XMR
	PixelSearch=XM
	Random=XMR
	RegDelete=XM
	RegRead=XMR
	RegWrite=XM
	SysGet=XMR
	TrayTip=XM

	Control=XSU
	ControlGet=XSR
	Drive=XSU
	DriveGet=XSR
	Process=XSU
	WinGet=XSR
	WinSet=XSU

	IfEqual=XI,if
	IfExist=XI,if FileExist
	IfGreater=XI,if
	IfGreaterOrEqual=XI,if
	IfInString=XI,if InStr
	IfLess=XI,if
	IfLessOrEqual=XI,if
	IfMsgBox=XI
	IfNotEqual=XI,if
	IfNotExist=XI,if !FileExist
	IfNotInString=XI,if !InStr
	IfWinActive=XI,if WinActive
	IfWinExist=XI,if WinExist
	IfWinNotActive=XI,if !WinActive
	IfWinNotExist=XI,if !WinExist

	AutoTrim=XX
	EnvUpdate=XX
	FileReadLine=XXR
	Gui=XX
	GuiControl=XX
	GuiControlGet=XXR
	Menu=XX
	Progress=XX
	SetBatchLines=XX
	SetFormat=XX
	SplashImage=XX
	SplashTextOff=XX
	SplashTextOn=XX
	StringSplit=XXR
	Transform=XX

	EnvAdd=XR,DateAdd
	EnvDiv=XR
	EnvMult=XR
	EnvSub=XR,DateDiff
	GetKeyState=XR
	OnExit=X
	SetEnv=X
	SoundGetWaveVolume=XR
	SoundSetWaveVolume=X
	StringGetPos=XR,InStr
	StringLeft=XR,SubStr
	StringMid=XR,SubStr
	StringReplace=XR,StrReplace
	StringRight=XR,SubStr
	StringTrimLeft=XR,SubStr
	StringTrimRight=XR,SubStr
	WinGetActiveStats=XR
	WinGetActiveTitle=XR

	ControlGetFocus=R
	ControlGetText=R
	DriveSpaceFree=R,DriveGetSpaceFree
	EnvGet=R
	FileGetAttrib=R
	FileGetSize=R
	FileGetTime=R
	FileGetVersion=R
	FileSelectFile=R,FileSelect
	FileSelectFolder=R,DirSelect
	FormatTime=R
	IniRead=R
	SoundGet=R
	StatusBarGetText=R
	StringLen=R,StrLen
	StringLower=R,StrLower
	StringUpper=R,StrUpper
	WinGetClass=R
	WinGetText=R
	WinGetTitle=R

	BlockInput=U
	Click=U
	ClipWait=U
	ControlClick=U
	ControlFocus=U
	ControlGetPos=U
	CoordMode=U
	Critical=U
	DetectHiddenText=U
	DetectHiddenWindows=U
	Edit=U
	EnvSet=U
	Exit=U
	ExitApp=U
	FileCopy=U
	FileCopyDir=U,DirCopy
	FileCreateDir=U,DirCreate
	FileCreateShortcut=U
	FileDelete=U
	FileEncoding=U
	FileGetShortcut=U
	FileInstall=U
	FileMove=U
	FileMoveDir=U,DirMove
	FileRecycle=U
	FileRecycleEmpty=U
	FileRemoveDir=U,DirDelete
	FileSetTime=U
	GroupActivate=U
	GroupClose=U
	GroupDeactivate=U
	Hotkey=U
	ImageSearch=U
	IniDelete=U
	IniWrite=U
	KeyHistory=U
	KeyWait=U
	ListHotkeys=U
	ListLines=U
	ListVars=U
	MouseClick=U
	MouseClickDrag=U
	MouseGetPos=U
	MouseMove=U
	OutputDebug=U
	Pause=U
	PostMessage=U
	Reload=U
	Run=U
	RunAs=U
	RunWait=U
	Send=U
	SendEvent=U
	SendInput=U
	SendLevel=U
	SendMessage=U
	SendMode=U
	SendPlay=U
	SendRaw=U
	SetCapsLockState=U
	SetControlDelay=U
	SetDefaultMouseSpeed=U
	SetKeyDelay=U
	SetMouseDelay=U
	SetNumLockState=U
	SetRegView=U
	SetScrollLockState=U
	SetStoreCapsLockMode=U
	SetTimer=U
	SetTitleMatchMode=U
	SetWinDelay=U
	SetWorkingDir=U
	Shutdown=U
	Sleep=U
	SoundBeep=U
	SoundPlay=U
	SoundSet=U
	SplitPath=U
	StatusBarWait=U
	StringCaseSense=U
	Suspend=U
	Thread=U
	ToolTip=U
	UrlDownloadToFile=U,Download
	WinActivate=U
	WinActivateBottom=U
	WinClose=U
	WinGetPos=U
	WinHide=U
	WinKill=U
	WinMaximize=U
	WinMenuSelectItem=U,MenuSelect
	WinMinimize=U
	WinMinimizeAll=U
	WinMinimizeAllUndo=U
	WinRestore=U
	WinShow=U
	WinWait=U
	WinWaitActive=U
	WinWaitClose=U
	WinWaitNotActive=U
	)"

	vText2 := " ;continuation section
	(LTrim
	;[ahk1 subcommands]
	Control-Add=XSU,ControlAddItem
	Control-Check=XSU,ControlSetChecked
	Control-Choose=XSU,ControlChoose
	Control-ChooseString=XSU,ControlChooseString
	Control-Delete=XSU,ControlDeleteItem
	Control-Disable=XSU,ControlSetEnabled
	Control-EditPaste=XSU,ControlEditPaste
	Control-Enable=XSU,ControlSetEnabled
	Control-ExStyle=XSU,ControlSetExStyle
	Control-Hide=XSU,ControlHide
	Control-HideDropDown=XSU,ControlHideDropDown
	Control-Show=XSU,ControlShow
	Control-ShowDropDown=XSU,ControlShowDropDown
	Control-Style=XSU,ControlSetStyle
	Control-TabLeft=XSU,ControlSetTab
	Control-TabRight=XSU,ControlSetTab
	Control-Uncheck=XSU,ControlSetChecked

	ControlGet-Checked=XSR,ControlGetChecked
	ControlGet-Choice=XSR,ControlGetChoice
	ControlGet-CurrentCol=XSR,ControlGetCurrentCol
	ControlGet-CurrentLine=XSR,ControlGetCurrentLine
	ControlGet-Enabled=XSR,ControlGetEnabled
	ControlGet-ExStyle=XSR,ControlGetExStyle
	ControlGet-FindString=XSR,ControlFindItem
	ControlGet-Hwnd=XSR,ControlGetHwnd
	ControlGet-Line=XSR,ControlGetLine
	ControlGet-LineCount=XSR,ControlGetLineCount
	ControlGet-List=XSR,ControlGetList
	ControlGet-Selected=XSR,ControlGetSelected
	ControlGet-Style=XSR,ControlGetStyle
	ControlGet-Tab=XSR,ControlGetTab
	ControlGet-Visible=XSR,ControlGetVisible

	;see also: DriveSpaceFree=XSR,DriveGetSpaceFree
	DriveGet-Capacity=XSR,DriveGetCapacity
	DriveGet-Filesystem=XSR,DriveGetFilesystem
	DriveGet-Label=XSR,DriveGetLabel
	DriveGet-List=XSR,DriveGetList
	DriveGet-Serial=XSR,DriveGetSerial
	DriveGet-Status=XSR,DriveGetStatus
	DriveGet-StatusCD=XSR,DriveGetStatusCD
	DriveGet-Type=XSR,DriveGetType

	Drive-Eject=XSU,DriveEject
	Drive-Label=XSU,DriveSetLabel
	Drive-Lock=XSU,DriveLock
	Drive-Unlock=XSU,DriveUnlock

	Process-Close=XSU,ProcessClose
	Process-Exist=XSU,ProcessExist
	Process-Priority=XSU,ProcessSetPriority
	Process-Wait=XSU,ProcessWait
	Process-WaitClose=XSU,ProcessWaitClose

	WinGet-ControlList=XSR,WinGetControls
	WinGet-ControlListHwnd=XSR,WinGetControlsHwnd
	WinGet-Count=XSR,WinGetCount
	WinGet-ExStyle=XSR,WinGetExStyle
	WinGet-ID=XSR,WinGetID
	WinGet-IDLast=XSR,WinGetIDLast
	WinGet-List=XSR,WinGetList
	WinGet-MinMax=XSR,WinGetMinMax
	WinGet-PID=XSR,WinGetPID
	WinGet-ProcessName=XSR,WinGetProcessName
	WinGet-ProcessPath=XSR,WinGetProcessPath
	WinGet-Style=XSR,WinGetStyle
	WinGet-TransColor=XSR,WinGetTransColor
	WinGet-Transparent=XSR,WinGetTransparent

	WinSet-AlwaysOnTop=XSU,WinSetAlwaysOnTop
	WinSet-Bottom=XSU,WinMoveBottom
	WinSet-Disable=XSU,WinSetEnabled
	WinSet-Enable=XSU,WinSetEnabled
	WinSet-ExStyle=XSU,WinSetExStyle
	WinSet-Redraw=XSU,WinRedraw
	WinSet-Region=XSU,WinSetRegion
	WinSet-Style=XSU,WinSetStyle
	WinSet-Top=XSU,WinMoveTop
	WinSet-TransColor=XSU,WinSetTransColor
	WinSet-Transparent=XSU,WinSetTransparent

	[ahk1 commands]
	AutoTrim=S
	BlockInput=S
	Click=S
	ClipWait=EE
	Control=SSSSSSS
	ControlClick=SSSSESSS
	ControlFocus=SSSSS
	ControlGet=OSSSSSSS
	ControlGetFocus=OSSSS
	ControlGetPos=OOOOSSSSS
	ControlGetText=OSSSSS
	ControlMove=SEEEESSSS
	ControlSend=SSSSSS
	ControlSendRaw=SSSSSS
	ControlSetText=SSSSSS
	CoordMode=SS
	Critical=S
	DetectHiddenText=S
	DetectHiddenWindows=S
	Drive=SSS
	DriveGet=OSS
	DriveSpaceFree=OS
	Edit=
	EnvAdd=OES
	EnvDiv=OE
	EnvGet=OS
	EnvMult=OE
	EnvSet=SS
	EnvSub=OES
	EnvUpdate=
	Exit=E
	ExitApp=E
	FileAppend=SSS
	FileCopy=SSE
	FileCopyDir=SSE
	FileCreateDir=S
	FileCreateShortcut=SSSSSSSEE
	FileDelete=S
	FileEncoding=S
	FileGetAttrib=OS
	FileGetShortcut=SOOOOOOO
	FileGetSize=OSS
	FileGetTime=OSS
	FileGetVersion=OS
	FileInstall=SSE
	FileMove=SSE
	FileMoveDir=SSS
	FileRead=OS
	FileReadLine=OSE
	FileRecycle=S
	FileRecycleEmpty=S
	FileRemoveDir=SE
	FileSelectFile=OSSSS
	FileSelectFolder=OSES
	FileSetAttrib=SSEE
	FileSetTime=ESSEE
	FormatTime=OSS
	GetKeyState=OSS
	GroupActivate=SS
	GroupAdd=SSSSSS
	GroupClose=SS
	GroupDeactivate=SS
	Gui=SSSS
	GuiControl=SSS
	GuiControlGet=OSSS
	Hotkey=SSS
	IfEqual=IS
	IfExist=S
	IfGreater=IS
	IfGreaterOrEqual=IS
	IfInString=IS
	IfLess=IS
	IfLessOrEqual=IS
	IfMsgBox=S
	IfNotEqual=IS
	IfNotExist=S
	IfNotInString=IS
	IfWinActive=SSSS
	IfWinExist=SSSS
	IfWinNotActive=SSSS
	IfWinNotExist=SSSS
	ImageSearch=OOEEEES
	IniDelete=SSS
	IniRead=OSSSS
	IniWrite=SSSS
	Input=OSSS
	InputBox=OSSSEEEESES
	KeyHistory=
	KeyWait=SS
	ListHotkeys=
	ListLines=S
	ListVars=
	Menu=SSSSSS
	MouseClick=SEEEESS
	MouseClickDrag=SEEEEES
	MouseGetPos=OOOOE
	MouseMove=EEES
	MsgBox=SSSS
	OnExit=SS
	OutputDebug=S
	Pause=SS
	PixelGetColor=OEES
	PixelSearch=OOEEEEEES
	PostMessage=EEESSSSS
	Process=SSS
	Progress=SSSSSS
	Random=OEE
	RegDelete=SSS
	RegRead=OSSS
	RegWrite=SSSSS
	Reload=
	Run=SSSO
	RunAs=SSS
	RunWait=SSSO
	Send=S
	SendEvent=S
	SendInput=S
	SendLevel=E
	SendMessage=EEESSSSSE
	SendMode=S
	SendPlay=S
	SendRaw=S
	SetBatchLines=S
	SetCapsLockState=S
	SetControlDelay=E
	SetDefaultMouseSpeed=E
	SetEnv=OS
	SetFormat=SS
	SetKeyDelay=EES
	SetMouseDelay=ES
	SetNumLockState=S
	SetRegView=S
	SetScrollLockState=S
	SetStoreCapsLockMode=S
	SetTimer=SSE
	SetTitleMatchMode=S
	SetWinDelay=E
	SetWorkingDir=S
	Shutdown=E
	Sleep=E
	Sort=IS
	SoundBeep=EE
	SoundGet=OSSE
	SoundGetWaveVolume=OE
	SoundPlay=SS
	SoundSet=ESSE
	SoundSetWaveVolume=EE
	SplashImage=SSSSSSS
	SplashTextOff=
	SplashTextOn=EESS
	SplitPath=IOOOOO
	StatusBarGetText=OESSSS
	StatusBarWait=SEESSESS
	StringCaseSense=S
	StringGetPos=OISSE
	StringLeft=OIE
	StringLen=OI
	StringLower=OIS
	StringMid=OIEES
	StringReplace=OISSS
	StringRight=OIE
	StringSplit=SISSS
	StringTrimLeft=OIE
	StringTrimRight=OIE
	StringUpper=OIS
	Suspend=S
	SysGet=OSSS
	Thread=SEE
	ToolTip=SEEE
	Transform=OSSS
	TrayTip=SSEE
	UrlDownloadToFile=SS
	WinActivate=SSSS
	WinActivateBottom=SSSS
	WinClose=SSESS
	WinGet=OSSSSS
	WinGetActiveStats=OOOOO
	WinGetActiveTitle=O
	WinGetClass=OSSSS
	WinGetPos=OOOOSSSS
	WinGetText=OSSSS
	WinGetTitle=OSSSS
	WinHide=SSSS
	WinKill=SSESS
	WinMaximize=SSSS
	WinMenuSelectItem=SSSSSSSSSSS
	WinMinimize=SSSS
	WinMinimizeAll=
	WinMinimizeAllUndo=
	WinMove=SSSSSSSS
	WinRestore=SSSS
	WinSet=SSSSSS
	WinSetTitle=SSSSS
	WinShow=SSSS
	WinWait=SSESS
	WinWaitActive=SSESS
	WinWaitClose=SSESS
	WinWaitNotActive=SSESS

	[ahk1 functions]
	Abs=S
	ACos=S
	Array=SSSSSSSSSSSSSSSSSSSS
	Asc=S
	ASin=S
	ATan=S
	Ceil=S
	Chr=S
	ComObjActive=S
	ComObjArray=SSSSSSSSS
	ComObjConnect=SS
	ComObjCreate=SS
	ComObject=SSS
	ComObjEnwrap=S
	ComObjError=S
	ComObjFlags=SSS
	ComObjGet=S
	ComObjMissing=
	ComObjParameter=SS
	ComObjQuery=SSS
	ComObjType=SS
	ComObjUnwrap=S
	ComObjValue=S
	Cos=S
	DllCall=SSSSSSSSSSSSSSSSSSSS
	Exception=SSS
	Exp=S
	FileExist=S
	FileOpen=SSS
	Floor=S
	Format=SSSSSSSSSSSSSSSSSSSS
	Func=S
	GetKeyName=S
	GetKeySC=S
	GetKeyState=SS
	GetKeyVK=S
	IL_Add=SSSS
	IL_Create=SSS
	IL_Destroy=S
	InStr=SSSSS
	IsByRef=S
	IsFunc=S
	IsLabel=S
	IsObject=S
	Ln=S
	LoadPicture=SSS
	Log=S
	LTrim=SS
	LV_Add=SSSSSSSSSSSSSSSSSSSS
	LV_Delete=S
	LV_DeleteCol=S
	LV_GetCount=S
	LV_GetNext=SS
	LV_GetText=SSS
	LV_Insert=SSSSSSSSSSSSSSSSSSSS
	LV_InsertCol=SSS
	LV_Modify=SSSSSSSSSSSSSSSSSSSS
	LV_ModifyCol=SSS
	LV_SetImageList=SS
	MenuGetHandle=S
	MenuGetName=S
	Mod=SS
	NumGet=SSS
	NumPut=SSSS
	ObjAddRef=S
	ObjBindMethod=SSSSSSSSSSSSSSSSSSSS
	ObjClone=S
	ObjDelete=SSS
	Object=SSSSSSSSSSSSSSSSSSSS
	ObjGetAddress=SS
	ObjGetCapacity=SS
	ObjHasKey=SS
	ObjInsert=SSSSSSSSSSSSSSSSSSSS
	ObjInsertAt=SSSSSSSSSSSSSSSSSSSS
	ObjLength=S
	ObjMaxIndex=S
	ObjMinIndex=S
	ObjNewEnum=S
	ObjPop=S
	ObjPush=SSSSSSSSSSSSSSSSSSSS
	ObjRawSet=SSS
	ObjRelease=S
	ObjRemove=SSS
	ObjRemoveAt=SSS
	ObjSetCapacity=SSS
	OnClipboardChange=SS
	OnExit=SS
	OnMessage=SSS
	Ord=S
	RegExMatch=SSSS
	RegExReplace=SSSSSS
	RegisterCallback=SSSS
	Round=SS
	RTrim=SS
	SB_SetIcon=SSS
	SB_SetParts=SSSSSSSSSSSSSSSSSSSS
	SB_SetText=SSS
	Sin=S
	Sqrt=S
	StrGet=SSS
	StrLen=S
	StrPut=SSSS
	StrReplace=SSSOS
	StrSplit=SSS
	SubStr=SSS
	Tan=S
	Trim=SS
	TV_Add=SSS
	TV_Delete=S
	TV_Get=SS
	TV_GetChild=S
	TV_GetCount=
	TV_GetNext=SS
	TV_GetParent=S
	TV_GetPrev=S
	TV_GetSelection=
	TV_GetText=SS
	TV_Modify=SSS
	TV_SetImageList=SS
	VarSetCapacity=SSS
	WinActive=SSSS
	WinExist=SSSS

	[ahk2 functions]
	Abs=S
	ACos=S
	Array=SSSSSSSSSSSSSSSSSSSS
	ASin=S
	ATan=S
	BlockInput=S
	Ceil=S
	Chr=S
	Click=SSSSSS
	ClipboardAll=SS
	ClipWait=SS
	ComObjActive=S
	ComObjArray=SSSSSSSSS
	ComObjConnect=SS
	ComObjCreate=SS
	ComObject=SSS
	ComObjError=S
	ComObjFlags=SSS
	ComObjGet=S
	ComObjQuery=SSS
	ComObjType=SS
	ComObjValue=S
	ControlAddItem=SSSSSS
	ControlChoose=SSSSS
	ControlChooseString=SSSSSS
	ControlClick=SSSSSSSS
	ControlDeleteItem=SSSSSS
	ControlEditPaste=SSSSSS
	ControlFindItem=SSSSSS
	ControlFocus=SSSSS
	ControlGetChecked=SSSSS
	ControlGetChoice=SSSSS
	ControlGetCurrentCol=SSSSS
	ControlGetCurrentLine=SSSSS
	ControlGetEnabled=SSSSS
	ControlGetExStyle=SSSSS
	ControlGetFocus=SSSS
	ControlGetHwnd=SSSSS
	ControlGetLine=SSSSSS
	ControlGetLineCount=SSSSS
	ControlGetList=SSSSSS
	ControlGetPos=OOOOSSSSS
	ControlGetSelected=SSSSS
	ControlGetStyle=SSSSS
	ControlGetTab=SSSSS
	ControlGetText=SSSSS
	ControlGetVisible=SSSSS
	ControlHide=SSSSS
	ControlHideDropDown=SSSSS
	ControlMove=SSSSSSSSS
	ControlSend=SSSSSS
	ControlSendRaw=SSSSSS
	ControlSetChecked=SSSSSS
	ControlSetEnabled=SSSSSS
	ControlSetExStyle=SSSSSS
	ControlSetStyle=SSSSSS
	ControlSetTab=SSSSSS
	ControlSetText=SSSSSS
	ControlShow=SSSSS
	ControlShowDropDown=SSSSS
	CoordMode=SS
	Cos=S
	Critical=S
	DateAdd=SSS
	DateDiff=SSS
	DetectHiddenText=S
	DetectHiddenWindows=S
	DirCopy=SSS
	DirCreate=S
	DirDelete=SS
	DirExist=S
	DirMove=SSS
	DirSelect=SSS
	DllCall=SSSSSSSSSSSSSSSSSSSS
	Download=SS
	DriveEject=SS
	DriveGetCapacity=S
	DriveGetFilesystem=S
	DriveGetLabel=S
	DriveGetList=S
	DriveGetSerial=S
	DriveGetSpaceFree=S
	DriveGetStatus=S
	DriveGetStatusCD=S
	DriveGetType=S
	DriveLock=S
	DriveSetLabel=SS
	DriveUnlock=S
	Edit=
	EnvGet=S
	EnvSet=SS
	Exception=SSS
	Exit=S
	ExitApp=S
	Exp=S
	FileAppend=SSS
	FileCopy=SSS
	FileCreateShortcut=SSSSSSSSS
	FileDelete=S
	FileEncoding=S
	FileExist=S
	FileGetAttrib=S
	FileGetShortcut=SOOOOOOO
	FileGetSize=SS
	FileGetTime=SS
	FileGetVersion=S
	FileInstall=SSS
	FileMove=SSS
	FileOpen=SSS
	FileRead=S
	FileRecycle=S
	FileRecycleEmpty=S
	FileSelect=SSSS
	FileSetAttrib=SSS
	FileSetTime=SSSS
	Floor=S
	Format=SSSSSSSSSSSSSSSSSSSS
	FormatTime=SS
	Func=S
	GetKeyName=S
	GetKeySC=S
	GetKeyState=SS
	GetKeyVK=S
	GroupActivate=SS
	GroupAdd=SSSSS
	GroupClose=SS
	GroupDeactivate=SS
	GuiCreate=SS
	GuiCtrlFromHwnd=SSS
	GuiFromHwnd=S
	Hotkey=SSS
	ImageSearch=OOSSSSS
	IniDelete=SSS
	IniRead=SSSS
	IniWrite=SSSS
	Input=SSS
	InputBox=SSSS
	InputEnd=
	InStr=SSSSS
	IsByRef=S
	IsFunc=S
	IsLabel=S
	IsObject=S
	KeyHistory=
	KeyWait=SS
	ListHotkeys=
	ListLines=S
	ListVars=
	Ln=S
	LoadPicture=SSS
	Log=S
	LTrim=SS
	MenuGetHandle=S
	MenuGetName=S
	MenuSelect=SSSSSSSSSSS
	Mod=SS
	MonitorGet=SSSSS
	MonitorGetCount=
	MonitorGetName=S
	MonitorGetPrimary=
	MonitorGetWorkArea=SSSSS
	MouseClick=SSSSSSS
	MouseClickDrag=SSSSSSS
	MouseGetPos=OOOOS
	MouseMove=SSSS
	MsgBox=SSS
	NumGet=SSS
	NumPut=SSSS
	ObjAddRef=S
	ObjBindMethod=SSSSSSSSSSSSSSSSSSSS
	ObjClone=S
	ObjDelete=SSS
	Object=SSSSSSSSSSSSSSSSSSSS
	ObjGetAddress=SS
	ObjGetCapacity=SS
	ObjHasKey=SS
	ObjInsertAt=SSSSSSSSSSSSSSSSSSSS
	ObjLength=S
	ObjMaxIndex=S
	ObjMinIndex=S
	ObjNewEnum=S
	ObjPop=S
	ObjPush=SSSSSSSSSSSSSSSSSSSS
	ObjRawSet=SSS
	ObjRelease=S
	ObjRemoveAt=SSS
	ObjSetCapacity=SSS
	OnClipboardChange=SS
	OnExit=SS
	OnMessage=SSS
	Ord=S
	OutputDebug=S
	Pause=SS
	PixelGetColor=SSS
	PixelSearch=OOSSSSSSS
	PostMessage=SSSSSSSS
	ProcessClose=S
	ProcessExist=S
	ProcessSetPriority=SS
	ProcessWait=SS
	ProcessWaitClose=SS
	Random=SS
	RandomSeed=S
	RegDelete=SS
	RegDeleteKey=S
	RegExMatch=SSSS
	RegExReplace=SSSSSS
	RegisterCallback=SSSS
	RegRead=SS
	RegWrite=SSSS
	Reload=
	Round=SS
	RTrim=SS
	Run=SSSO
	RunAs=SSS
	RunWait=SSSO
	Send=S
	SendEvent=S
	SendInput=S
	SendLevel=S
	SendMessage=SSSSSSSSS
	SendMode=S
	SendPlay=S
	SendRaw=S
	SetCapsLockState=S
	SetControlDelay=S
	SetDefaultMouseSpeed=S
	SetKeyDelay=SSS
	SetMouseDelay=SS
	SetNumLockState=S
	SetRegView=S
	SetScrollLockState=S
	SetStoreCapsLockMode=S
	SetTimer=SSS
	SetTitleMatchMode=S
	SetWinDelay=S
	SetWorkingDir=S
	Shutdown=S
	Sin=S
	Sleep=S
	Sort=SS
	SoundBeep=SS
	SoundGet=SSS
	SoundPlay=SS
	SoundSet=SSSS
	SplitPath=SOOOOO
	Sqrt=S
	StatusBarGetText=SSSSS
	StatusBarWait=SSSSSSSS
	StrGet=SSS
	StringCaseSense=S
	StrLen=S
	StrLower=SS
	StrPut=SSSS
	StrReplace=SSSOS
	StrSplit=SSS
	StrUpper=SS
	SubStr=SSS
	Suspend=S
	SysGet=S
	Tan=S
	Thread=SSS
	ToolTip=SSSS
	TrayTip=SSS
	Trim=SS
	Type=S
	VarSetCapacity=SSS
	WinActivate=SSSS
	WinActivateBottom=SSSS
	WinActive=SSSS
	WinClose=SSSSS
	WinExist=SSSS
	WinGetClass=SSSS
	WinGetControls=SSSS
	WinGetControlsHwnd=SSSS
	WinGetCount=SSSS
	WinGetExStyle=SSSS
	WinGetID=SSSS
	WinGetIDLast=SSSS
	WinGetList=SSSS
	WinGetMinMax=SSSS
	WinGetPID=SSSS
	WinGetPos=OOOOSSSS
	WinGetProcessName=SSSS
	WinGetProcessPath=SSSS
	WinGetStyle=SSSS
	WinGetText=SSSS
	WinGetTitle=SSSS
	WinGetTransColor=SSSS
	WinGetTransparent=SSSS
	WinHide=SSSS
	WinKill=SSSSS
	WinMaximize=SSSS
	WinMinimize=SSSS
	WinMinimizeAll=
	WinMinimizeAllUndo=
	WinMove=SSSSSSSS
	WinMoveBottom=SSSS
	WinMoveTop=SSSS
	WinRedraw=SSSS
	WinRestore=SSSS
	WinSetAlwaysOnTop=SSSSS
	WinSetEnabled=SSSSS
	WinSetExStyle=SSSSS
	WinSetRegion=SSSSS
	WinSetStyle=SSSSS
	WinSetTitle=SSSSS
	WinSetTransColor=SSSSS
	WinSetTransparent=SSSSS
	WinShow=SSSS
	WinWait=SSSSS
	WinWaitActive=SSSSS
	WinWaitClose=SSSSS
	WinWaitNotActive=SSSSS
	)"

	return vText1 "`n" vText2
}

;==================================================

JEE_CvtJoin(vParams, oArray*)
{
	vOutput := ""
	Loop, Parse, vParams
	{
		vTemp := JEE_Cvt(oArray[A_Index], A_LoopField)
		if (vTemp = "")
			continue
		if (JEE_SubStr(vOutput, -1) = Chr(34))
		&& (JEE_SubStr(vTemp, 1, 1) = Chr(34))
			vOutput := SubStr(vOutput, 1, -1) SubStr(vTemp, 2)
		else
			vOutput .= " " vTemp
	}
	return LTrim(vOutput)
}

;==================================================

JEE_ExpTrim(vText)
{
	while (SubStr(vText, 1, 2) = Chr(34) " ")
		vText := Chr(34) SubStr(vText, 3)
	while (JEE_SubStr(vText, -2) = " " Chr(34))
		vText := SubStr(vText, 1, -2) Chr(34)
	return vText
}

;==================================================

; ;===============
; ;e.g.
; vText := JEE_GetSelectedText()
; ;===============

; ;===============
; ;e.g. get selected text simple alternative
; Clipboard := ""
; SendInput, ^c
; ClipWait, 3
; if ErrorLevel
; {
; 	MsgBox, % "error: failed to retrieve clipboard text"
; 	return
; }
; vText := Clipboard
; ;===============

JEE_GetSelectedText(vWait:=3)
{
	hWnd := WinGetID("A")
	vCtlClassNN := ControlGetFocus("ahk_id " hWnd)
	if (RegExReplace(vCtlClassNN, "\d") = "Edit")
		vText := ControlGetSelected(vCtlClassNN, "ahk_id " hWnd)
	else
	{
		ClipSaved := ClipboardAll
		Clipboard := ""
		SendInput("^c")
		ClipWait(vWait)
		if ErrorLevel
		{
			ToolTip("ClipWait failed (" A_ThisHotkey ")")
			Clipboard := ClipSaved
			ClipSaved := ""
			Sleep(1000)
			ToolTip()
			Exit() ;terminate the thread that launched this function
		}
		vText := Clipboard
		Clipboard := ClipSaved
		ClipSaved := ""
	}
	return vText
}

;==================================================

JEE_ObjList(oArray, vSep:=" ", vRecurse:=1)
{
	if !vRecurse
	{
		for vKey, vValue in oArray
			vOutput .= vKey vSep vValue "`r`n"
		return SubStr(vOutput, 1, -2)
	}
	for vKey, vValue in oArray
	{
		;note: vRecurse is used to indicate depth, i.e. how many tabs to use
		if IsObject(vValue)
			vOutput .= JEE_StrRept("`t", vRecurse-1) vKey vSep "OBJECT`r`n" %A_ThisFunc%(vValue, vSep, vRecurse+1) "`r`n"
		else
			vOutput .= JEE_StrRept("`t", vRecurse-1) vKey vSep vValue "`r`n"
	}
	return SubStr(vOutput, 1, -2)
}

;==================================================

JEE_ObjPopBlank(oArray)
{
	Loop, % oArray.Length()
	{
		if (oArray[oArray.Length()] = "")
			oArray.Pop()
		else
			break
	}
}

;==================================================

JEE_ObjShuffleFrom(oArray, vOrd, vSep:="")
{
	oArray2 := []
	Loop, Parse, vOrd, % vSep
		if oArray.HasKey(A_LoopField)
			oArray2[A_Index] := oArray[A_LoopField]
	return oArray2
}

;==================================================

JEE_StrCount(ByRef vText, vNeedle, vCaseSen:=0)
{
	local vSCS, vCount
	if (vNeedle = "")
		return
	vSCS := A_StringCaseSense
	StringCaseSense(vCaseSen ? "On" : "Off")
	StrReplace(vText, vNeedle, "", vCount) ;seemed to be faster than line below
	;StrReplace(vText, vNeedle, vNeedle, vCount)
	StringCaseSense(vSCS)
	return vCount
}

;==================================================

JEE_StrJoin(vSep, oArray*)
{
	vOutput := ""
	;if an ObjCount function was available,
	;this would help with estimating the needed capacity
	VarSetCapacity(vOutput, 1000000*2)
	Loop, % oArray.MaxIndex()-1
		vOutput .= oArray[A_Index] vSep
	vOutput .= oArray[oArray.MaxIndex()]
	return vOutput
}

;==================================================

JEE_StrRept(vText, vNum)
{
	if (vNum <= 0)
		return
	return StrReplace(Format("{:" vNum "}", ""), " ", vText)
	;return StrReplace(Format("{:0" vNum "}", 0), 0, vText)
}

;==================================================

JEE_StrUnused(vNum, oArray*)
{
	vText := ""
	VarSetCapacity(vText, 1000*oArray.Length()*2)
	Loop, % oArray.Length()
		vText .= oArray[A_Index]
	vCount := 0
	Loop, 65535
		if !InStr(vText, Chr(A_Index))
		{
			vOutput .= Chr(A_Index)
			vCount++
			if (vCount = vNum)
				break
		}
	;return StrSplit(vOutput)
	return vOutput
}

;==================================================

;JEE_Compare2Strings
;JEE_StrCompare
;JEE_CompareStringsWinMerge
;JEE_StrCompareWinMerge
;JEE_WinMergeStrCompare
JEE_WinMergeCompareStrings(vText1, vText2, vOpt:="", vPathExe:="", vDirOut:="")
{
	global vPathWinMerge
	static vGetExePathWinMerge := Func("JEE_GetExePathWinMerge")
	;local oFile,vPathTemp1,vPathTemp2
	if (vText1 == vText2)
	{
		JEE_MsgBox("same (case sensitive)")
		return
	}
	;if (vText1 = vText2)
	;	MsgBox, % "same (case insensitive)"
	if !FileExist(vPathExe)
	&& !FileExist(vPathExe := vPathWinMerge)
	&& (!vGetExePathWinMerge || !FileExist(vPathExe := %vGetExePathWinMerge%()))
	{
		JEE_MsgBox("error: WinMerge not found")
		return
	}
	if (vDirOut = "")
		vDirOut := A_ScriptDir "\Temp"
	if !FileExist(vDirOut)
		DirCreate(vDirOut)
	Loop, 2
	{
		vPathTemp%A_Index% := vDirOut "\z wc" A_Index ".txt"
		oFile := FileOpen(vPathTemp%A_Index%, "w")
		oFile.Length := 0 ;empty file
		oFile.Encoding := "UTF-8"
		oFile.Write(Chr(0xFEFF) vText%A_Index%)
		oFile.Close()
	}
	;/s single instance
	;/wl opens the left side as read-only
	;/wr opens the right side as read-only
	if InStr(vOpt, "ro")
		Run(Chr(34) vPathExe Chr(34) " /s /wl /wr " Chr(34) vPathTemp1 Chr(34) " " Chr(34) vPathTemp2 Chr(34))
	else
		Run(Chr(34) vPathExe Chr(34) " /s " Chr(34) vPathTemp1 Chr(34) " " Chr(34) vPathTemp2 Chr(34))
}

;==================================================
