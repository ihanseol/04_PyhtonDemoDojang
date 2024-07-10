;==================================================

;an AHK v1 script
;AHK v1 to v2 converter by jeeswg
;[first released: 2018-02-21]

;from:
;AHK v1 to AHK v2 converter (initial work) - AutoHotkey Community
;https://autohotkey.com/boards/viewtopic.php?t=36754
;ahk v1 converter.ahk [this script]
;ahk v1 converter lib.ahk [additional library]

;from:
;commands as functions (AHK v2 functions for AHK v1) - AutoHotkey Community
;https://autohotkey.com/boards/viewtopic.php?f=37&t=29689
;JEEAhk1FC.ahk [commands as functions]
;JEEAhk1FC+.ahk [auxiliary functions expansion pack]

;==================================================

;MAIN SECTION 1 - INTRODUCTION
;MAIN SECTION 2 - OPTIONS
;MAIN SECTION 3 - INITIALISE
;MAIN SECTION 4 - HOTKEY 1
;MAIN SECTION 5 - HOTKEY 2

;==================================================

;MAIN SECTION 1 - INTRODUCTION

;==================================================

;NOTES: HOW IT WORKS

;- Ctrl+Q to convert the selected text
;(and output changes to a log file, if that option is set to on)
;- Ctrl+Win+W to check the selected text for nonstandard lines
;(i.e. lines that probably require conversion)

;- there are 3 command line parameters (paths) that can be used:
;PathIn / PathOut / PathOutLog
;here's an example script:

/*
q:: ;convert script
vPath := A_ScriptDir "\ahk v1 converter.ahk"
vPathIn := A_ScriptFullPath
SplitPath, vPathIn, vName, vDir, vExt, vNameNoExt, vDrive
vNow := A_Now
vPathOut := vDir "\" vNameNoExt "_v2 " vNow ".ahk"
vPathOutLog := vDir "\" vNameNoExt " CvtLog " vNow ".txt"
RunWait, "%A_AhkPath%" "%vPath%" "%vPathIn%" "%vPathOut%" "%vPathOutLog%"
Run, notepad.exe "%vPathOut%"
Run, notepad.exe "%vPathOutLog%"
return
*/

;- there are various options that can be set in the
;'MAIN SECTION 2 - OPTIONS' section
;- also, there is an #Include line, you can make various
;changes to the settings, by creating a file with AutoHotkey code
;with that particular filename

;==================================================

;NOTES: TYPES OF LINE TO CONVERT

;assignment
;var = value

;control flow statements
;- if + operators: between/contains/in/is type
;- if + operators: > < >= <= = <> !=
;- Loop
;- (others)

;commands

;directives
;- #IfWinXXX (#IfWin(Not)Active/#IfWin(Not)Exist)
;- (others)

;==================================================

;NOTES: MANUAL CONVERSION

;note: need to be converted manually:
;based on:
;AHK v1 to AHK v2 conversion tips/changes summary - AutoHotkey Community
;https://autohotkey.com/boards/viewtopic.php?f=37&t=36787
;functions: InStr/SubStr/RegExMatch/RegExReplace
;SetFormat
;Return: the last parameter is returned (rather than the first parameter)
;ternary operator: must specify the alternative result, see below for alternatives
;SendMessage: the reply is retrieved as the return value of the function, not as the content of ErrorLevel
;MsgBox: the choice is retrieved as the return value of the function, not via IfMsgBox
;if lines
;changes to continuation sections
;command line parameters retrieved via A_Args array not variables %0% %1% %2% etc
;var++, now fails if variable is blank, workaround: var := (var = "") ? 1 : var+1
;variable names/function names cannot start with a digit
;variable names can only contain letters/digits/underscore (and non-ASCII characters)
;deref operator removed: vNum := *var -> vNum := NumGet(var, 0, "UChar")
;old-style File/Reg loops removed
;bitwise-NOT always 64-bit, a two-way compatible workaround is: ~var -> var ^ -1
;oFile.__Handle renamed to oFile.Handle
;functions: LV_XXX/SB_XXX/TV_XXX
;functions: Asc/ComObjEnwrap/ComObjMissing/ComObjParameter/ComObjUnwrap/ObjInsert/ObjRemove
;methods: Insert/Remove
;Transform: some subcommands have no AHK v2 equivalent
;if var is type - 'type' now expects a variable, not hardcoded text
;OnExit command

;have no equivalent:
;between (use <= and/or >=)
;contains/in (may be implemented in AHK v2 in future)
;Gui/GuiControl/GuiControlGet/Menu (use objects instead)
;IfMsgBox
;Progress/SplashImage/SplashTextOff/SplashTextOn

;current two-way compatibility obstacles:
;A_AllowMainWindow/A_IconHidden/A_IconTip
;double quotes: "" v. `" [although Chr(34) is a workaround]
;Loop

;key unresolved issues:
;ControlClick/ControlGetPos/ControlMove [in AHK v2, they use client coordinates, this would break scripts, unless 'A_CoordModeControl' existed]
;PixelGetColor/PixelSearch [line cannot be converted without the use of an auxiliary function RGB to BGR function, or a 'BGR' mode]

;==================================================

;NOTES: NOT REPLACED

;operators
;not -> !
;OR -> ||
;AND -> &&

;invalid ternary operators
;(cond) ? action1 -> (cond) ? action1 : action2 ['binary ternary operator' (which causes a silent error) to ternary operator]

;parameters
;identify parameters that look numeric, but that should be wrapped in double quotes e.g. 000 but should be "000"

;functions
;to tidy functions use the DllCall script corrector instead
;identify = instead of := in custom function definitions
;check for ambiguity: InStr/SubStr/RegExMatch/RegExReplace
;cannot use "" for output variable parameters e.g. RegExMatch/StrReplace/RegExReplace

;problem lines
;- IfXXX and a 'command' on one line (these are currently ignored i.e. not converted)
;you can have two 'commands' on one line, if the first 'command' is one of these eight:
;IfEqual|IfGreater|IfGreaterOrEqual|IfLess|IfLessOrEqual|IfNotEqual
;IfInString|IfNotInString
;- if var contains ,,
;- using commas in the last parameter
;e.g. FormatTime has 3 parameters, so the script can't convert this, which it sees as 5 parameters:
;FormatTime, vDate,, dd,MM,yyyy
;- FileAppend with an output path of * or ** could potentially be a problem

;potential source of bugs
;a continuation section start/end not correctly identified
;a comment section start/end not correctly identified
;code split over multiple lines

;warning
;this script doesn't necessarily preserve whitespace between parameters

;==================================================

;NOTES: FUNCTIONS USED

;functions used/mentioned in script:
;JEE_ArrayToCmd
;JEE_ArrayToFunc
;JEE_ColRGBIsBGR
;JEE_CmdParamClean
;JEE_CmdPrepare
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
;JEE_StrUnused
;JEE_WinMergeCompareStrings

;two-way compatible functions to replace/add to AHK functionality
;- operators:
;JEE_Between
;JEE_MC
;JEE_MX
;JEE_StrIsType
;- raw read/write:
;JEE_ClipboardFromFile
;JEE_ClipboardToFile
;JEE_FileReadBin
;JEE_FileWriteBin
;- other:
;JEE_ComObjMissing
;JEE_InStr
;JEE_RegExMatch
;JEE_RegExReplace
;JEE_SubStr

;functions mentioned in script (not included):
;JEE_InputBox [different parameter order: Text, DEFAULT, Title, Options][same as InputBox but with 'AX_' variables to specify a font]
;JEE_MsgBox [same as MsgBox but with 'AX_' variables to specify a font]

;functions mentioned in script (not implemented):
;JEE_Progress
;JEE_SplashImage

;behind the scenes:
;use '% ""' with JEE_ArrayToFunc to ensure empty string cf. blank parameter

;==================================================

;NOTES: 'UGLY' CONVERSIONS

;there are some commands that *can* be converted automatically,
;but it may be better to convert these manually,
;by default such are conversions are not done
;vDoFileReadLine := 0 ;use FileRead and StrSplit
;vDoGetKeyState := 0 ;GetKeyState command to GetKeyState function
;vDoStringSplit := 0 ;StringSplit to Loop

;FileReadLine, OutputVar, % Filename, LineNum
;OutputVar := StrSplit(FileRead(Filename), "`n", "`r")[LineNum] ;file read line

;GetKeyState, OutputVar, % KeyName, % Mode
;OutputVar := {0:"U",1:"D"}[GetKeyState(KeyName, Mode)]

;StringSplit, OutputArray, InputVar, `n, `r
;Loop, Parse, InputVar, `n, `r ;string split
;	OutputArray%A_Index% := A_LoopField, OutputArray0 := A_Index

;==================================================

;MAIN SECTION 2 - OPTIONS

;INITIALISE: OPTIONS

;special options:
vDoJeeCustom := 0

;hotkeys
vHotkeyConvert := "^q" ;for SubConvert
vHotkeyCheckLines := "^#w" ;for SubCheckLines

;dir to output changelogs for converted scripts
vDirLog := A_Desktop "\z ahk convert"

;block conversions
;e.g. block conversions that would sometimes require auxiliary functions:
;vListBlock := "ControlClick,ControlGetPos,ControlMove"
;vListBlock := "InputBox"
vListBlock := ""

;comment out redundant lines (redundant commands/directives)
vListCommentOut := "#NoEnv,AutoTrim,SetBatchLines"
;vListCommentOut := ""

;AHK v1 incompatible conversions:
;current two-way compatibility problems:
;0: keep it AHK v1 compatible
;1: do the less compatible conversion 'AHK v2-ready'
;note: currently, the converter does not make Loop 'AHK v2-ready'
;note: currently, the converter always converts to Chr(34), not "" or `"
vDoLoop := 0 ;convert Loop parameters to make them AHK v2-ready
vDoLoopForceExp := 0 ;convert Loop parameters to force-expression style (otherwise leave unchanged): Loop, Parse, vText, % ","
vDoLoopTidy := 1 ;e.g. %var% to % var
vDoDoubleQuotes := 1 ;[NOT IMPLEMENTED] Chr(34): "" v. `"

;do the more backwards compatible conversion
;0: convert to the function with the more similar name (do the less compatible conversion)
vDoStringLower := 0 ;use Format instead of StrLower
vDoStringUpper := 0 ;use Format instead of StrUpper
vDoWinGetID := 0 ;use WinExist instead of WinGetID

;alternative functions
;0: use built-in functions
vDoJeeMsgBox := 0 ;to JEE_MsgBox (big font)
vDoJeeInputBox := 0 ;to JEE_InputBox (big font, different param order)

;allow 'ugly' conversions:
;can be converted automatically, but better converted manually:
;0: leave lines unconverted
vDoFileReadLine := 0 ;use FileRead and StrSplit
vDoGetKeyState := 0 ;GetKeyState command to GetKeyState function
vDoStringSplit := 0 ;StringSplit to Loop
vDoWinGetControlList := 0 ;[NOT IMPLEMENTED] use Loop to create a pseudo-array from the array
vDoWinGetControlListHwnd := 0 ;[NOT IMPLEMENTED] use Loop to create a pseudo-array from the array
vDoWinGetList := 0 ;[NOT IMPLEMENTED] use Loop to create a pseudo-array from the array

;auxiliary functions:
;allow conversions that require auxiliary functions:
;0: leave lines unconverted
vDoJeeBetween := 0 ;to JEE_Between
vDoJeeContains := 0 ;to JEE_MC (note: doesn't handle ,,)
vDoJeeIn := 0 ;to JEE_MX (note: doesn't handle ,,)
vDoJeeIsType := 0 ;to JEE_StrIsType
vDoJeeStringRight := 0 ;to JEE_SubStr
vDoJeeFileReadBin := 0 ;to JEE_FileReadBin
vDoJeeProgress := 0 ;[NOT IMPLEMENTED] to JEE_Progress
vDoJeeSplashImage := 0 ;[NOT IMPLEMENTED] to JEE_SplashImage
vDoJeeSplashText := 0 ;[NOT IMPLEMENTED] to JEE_Progress

;further auxiliary functions:
;JEE_ClipboardFromFile / JEE_ClipboardToFile ;work on both AHK v1/v2
;JEE_ComObjMissing ;works on both AHK v1/v2
;JEE_FileReadBin / JEE_FileWriteBin ;work on both AHK v1/v2
;JEE_InStr ;works like AHK v2 version on both AHK v1/v2
;JEE_RegExMatch / JEE_RegExReplace ;work like AHK v2 version on both AHK v1/v2

;further options
;0: add commas
;1: remove commas
vOptRemCommaCmd := 0 ;remove commas from commands
vOptRemCommaDrv := 1 ;remove commas from directives: '#Directive, ' -> '#Directive '
vOptRemCommaCFS := 1 ;remove commas from control flow statements (does not affect Loop)
vOptRemCommaLoop := 0 ;remove commas from Loop
vDoIfWinXXXDrv := 1 ;convert #IfWinXXX directives
vOptIndent := "`t" ;used for indentation if StringSplit is converted to a loop
vOptTidyC := 0 ;tidy commands
vOptLog := 1 ;write log file to log folder
vOptLogOmitCaseChange := 0 ;don't record info on line conversions that are simply a change of case
vOptRunLogLimit := 6 ;open log file if at least this many lines are changed
vOptRunLogAllow := 0 ;allow opening log file after conversion
vOptVarValueSimple := 1 ;convert var = value (simple instances)
vOptVarValueAll := 1 ;convert var = value (all instances)
vOptVarDoCmdNml := 1 ;convert commands that don't have a return value
vOptVarDoCmdRtn := 1 ;convert commands that do have a return value
vOptExcludeLinesInCommentSections := 0 ;correct code lines within comment sections (between /* and */)
vOptExcludeLinesThatContainString := 0
vOptExcludeString := ";[DO NOT CONVERT]"

;conversion mode:
;0 ;no changes: identify lines that are not AHK v2-ready
;11 ;AHK v1 (tidy script)
;12 ;AHK v1 to AHK v1 (convert)
;21 ;AHK v2 to AHK v1 ('unconvert') [NOT IMPLEMENTED]
;22 ;AHK v2 (tidy script) [NOT IMPLEMENTED]
vOptMode := 12

;==================================================

;MAIN SECTION 3 - INITIALISE

;==================================================

;INITIALISE: MAIN SCRIPT SETTINGS

#SingleInstance force
ListLines, Off
#KeyHistory 0
Menu, Tray, Click, 1
#NoEnv
AutoTrim, Off
#UseHook

SplitPath, A_ScriptName,,,, vScriptNameNoExt
Menu, Tray, Tip, % vScriptNameNoExt

#Include *i %A_ScriptDir%\Lib\ahk v1 converter lib.ahk
#Include *i %A_ScriptDir%\Lib\JEEAhk1FC.ahk
#Include *i %A_ScriptDir%\Lib\JEEAhk1FC+.ahk

;==================================================

;INITIALISE: COMMAND-LINE PARAMETERS (PATHS)

;vOptSpecial ;specify 'jee' for special JEE options (or set the contents of the #Include file (see lower down) to specify other options)
;vPathIn ;input file: script to be converted
;vPathOut ;output file: converted script output destination
;vPathOutLog ;output file: log of changes made

;MsgBox, % DllCall("kernel32\GetCommandLineW", Str)
vArgCount = %0%
if IsObject(A_Args)
{
	vArgCount := A_Args.Length()
	if vArgCount
		vIsCdLn := 1
	vPathIn := A_Args[1]
	vPathOut := A_Args[2]
	vPathOutLog := A_Args[3]
}
else if vArgCount
{
	vIsCdLn := 1
	vPathIn = %1%
	vPathOut = %2%
	vPathOutLog = %3%
}

if vIsCdLn
{
	if !FileExist(vPathIn)
	{
		MsgBox, % "error: input file not found:`r`n" vPathIn
		ExitApp
	}
	if FileExist(vPathOut)
	&& !(vPathOut = "*")
	&& !(vPathOut = "**")
	{
		MsgBox, % "error: output file already exists:`r`n" vPathOut
		ExitApp
	}
}

;==================================================

;INITIALISE: HOTKEYS

if !vIsCdLn
{
	if !(vHotkeyConvert = "")
		Hotkey, % vHotkeyConvert, SubConvert
	if !(vHotkeyCheckLines = "")
		Hotkey, % vHotkeyCheckLines, SubCheckLines
}

;==================================================

;INITIALISE: PREPARE VARIABLES/LISTS

vText := JEE_CvtCmdGetList()

;the double quote character
;vDQ := Chr(34)
vMode := vOptMode
;commands that require special handling:
vListCmd1X := "EnvAdd|EnvDiv|EnvMult|EnvSub|EnvUpdate|FileAppend|FileRead|FileReadLine|FileSetAttrib|GetKeyState|IfEqual|IfExist|IfGreater|IfGreaterOrEqual|IfInString|IfLess|IfLessOrEqual|IfNotEqual|IfNotExist|IfNotInString|IfWinActive|IfWinExist|IfWinNotActive|IfWinNotExist|Input|InputBox|Menu|MsgBox|PixelGetColor|PixelSearch|Random|RegDelete|RegRead|RegWrite|SetEnv|Sort|SoundGetWaveVolume|SoundSetWaveVolume|StringGetPos|StringLeft|StringLower|StringMid|StringReplace|StringRight|StringSplit|StringTrimLeft|StringTrimRight|StringUpper|SysGet|Transform|TrayTip|WinGetActiveStats|WinGetActiveTitle|WinMove|WinSetTitle" ;doesn't include: "Control|ControlGet|Drive|DriveGet|Process|WinGet|WinSet"
;commands that can specified with no parameters in AHK v1 and AHK v2:
vListCmd1NP := "Click|ClipWait|ControlClick|ControlFocus|ControlGetPos|ControlMove|Critical|Edit|Exit|ExitApp|FileEncoding|FileRecycleEmpty|FileSetTime|Input|KeyHistory|ListHotkeys|ListLines|ListVars|MouseClick|MouseGetPos|MsgBox|Pause|Random|RegDelete|RegWrite|Reload|RunAs|SetCapsLockState|SetKeyDelay|SetNumLockState|SetScrollLockState|SetTimer|SoundBeep|StatusBarWait|Suspend|ToolTip|TrayTip|WinActivate|WinClose|WinGetPos|WinHide|WinKill|WinMaximize|WinMinimize|WinMinimizeAll|WinMinimizeAllUndo|WinMove|WinRestore|WinShow|WinWaitActive|WinWaitClose|WinWaitNotActive"
;commands that can be 0-parameter in AHK v1, but not in AHK v2:
;ControlSetText|EnvUpdate|FileAppend|IfWinActive|IfWinExist|IfWinNotActive|IfWinNotExist|OnExit|Progress|SplashImage|SplashTextOff|SplashTextOn|WinSetTitle

oParams := {}
Loop, Parse, vText, `n, `r
{
	if (A_LoopField = "[ahk2 functions]")
		break
	oTemp := StrSplit(A_LoopField, "=")
	oParams[oTemp.1] := oTemp.2
}

vListFnc2 := "", oFnc2 := {}
vListCmd1 := "", oCmd1 := {}
vXtra := "", oXtra := {}
Loop, Parse, vText, `n, `r
{
	vTemp := A_LoopField
	oTemp := StrSplit(A_LoopField, "=")
	oParams[oTemp.1] := oTemp.2
	if (SubStr(vTemp, 1, 1) = "[")
		vTempVar := ""
	if (SubStr(vTemp, 1, 16) = "[ahk2 functions]")
		vTempVar := "vListFnc2"
	else if (SubStr(vTemp, 1, 15) = "[ahk1 commands]")
		vTempVar := "vListCmd1"
	else if (SubStr(vTemp, 1, 12) = "[ahk1toahk2]")
		vTempVar := "vXtra"
	else if (vTempVar) && (oTemp.1)
	{
		%vTempVar% .= oTemp.1 "|"
		if (vTempVar = "vListFnc2")
			oFnc2[oTemp.1] := oTemp.2
		if (vTempVar = "vListCmd1")
			oCmd1[oTemp.1] := oTemp.2
		if (vTempVar = "vXtra")
		{
			oXtra[oTemp.1] := StrSplit(oTemp.2, ",")
			if (oXtra[oTemp.1].1 ~= "[URP]$")
				vXtra .= oTemp.1 "|"
		}
	}
}
oTemp := ""
vListFnc2 := RTrim(vListFnc2, "|")
vListCmd1 := RTrim(vListCmd1, "|")
vXtra := RTrim(vXtra, "|")
;MsgBox, % Clipboard := JEE_ObjList(oFnc2) ;e.g. key: FormatTime, value: SS
;MsgBox, % Clipboard := JEE_ObjList(oCmd1) ;e.g. key: FormatTime, value: OSS
;MsgBox, % Clipboard := JEE_ObjList(oXtra) ;e.g. key: FileSelectFolder, value: ["R", "DirSelect"]

;list commands/control flow statements/directives
;but not functions/methods/operators/variables
vListCFS := "break,continue,else,Gosub,Goto,if,Loop,return,while"
vListCFS .= ",catch,finally,for,throw,try,until"

vListCmd := "GetKeyState"
vListCmd .= ",BlockInput,Click,ClipWait,ControlClick,ControlFocus,ControlGetFocus,ControlGetPos,ControlGetText,ControlMove,ControlSend,ControlSendRaw,ControlSetText,CoordMode,Critical,DetectHiddenText,DetectHiddenWindows,Edit,EnvGet,EnvSet,Exit,ExitApp,FileAppend,FileCopy,FileCreateShortcut,FileDelete,FileGetAttrib,FileGetShortcut,FileGetSize,FileGetTime,FileGetVersion,FileInstall,FileMove,FileRead,FileRecycle,FileRecycleEmpty,FileSetAttrib,FileSetTime,FormatTime,GroupActivate,GroupAdd,GroupClose,GroupDeactivate,Hotkey,ImageSearch,IniDelete,IniRead,IniWrite,Input,InputBox,KeyHistory,KeyWait,ListHotkeys,ListLines,ListVars,Menu,MouseClick,MouseClickDrag,MouseGetPos,MouseMove,MsgBox,OutputDebug,Pause,PixelGetColor,PixelSearch,PostMessage,Random,RegDelete,RegRead,RegWrite,Reload,Run,RunAs,RunWait,Send,SendEvent,SendInput,SendMessage,SendMode,SendPlay,SendRaw,SetCapsLockState,SetControlDelay,SetDefaultMouseSpeed,SetKeyDelay,SetMouseDelay,SetNumLockState,SetScrollLockState,SetStoreCapsLockMode,SetTimer,SetTitleMatchMode,SetWinDelay,SetWorkingDir,Shutdown,Sleep,Sort,SoundBeep,SoundGet,SoundPlay,SoundSet,SplitPath,StatusBarGetText,StatusBarWait,StringCaseSense,Suspend,SysGet,Thread,ToolTip,TrayTip,WinActivate,WinActivateBottom,WinClose,WinGetClass,WinGetPos,WinGetText,WinGetTitle,WinHide,WinKill,WinMaximize,WinMinimize,WinMinimizeAll,WinMinimizeAllUndo,WinMove,WinRestore,WinSetTitle,WinShow,WinWait,WinWaitActive,WinWaitClose,WinWaitNotActive"
vListCmd .= ",AutoTrim,Control,ControlGet,Drive,DriveGet,DriveSpaceFree,EnvAdd,EnvDiv,EnvMult,EnvSub,EnvUpdate,FileCopyDir,FileCreateDir,FileMoveDir,FileReadLine,FileRemoveDir,FileSelectFile,FileSelectFolder,Gui,GuiControl,GuiControlGet,IfEqual,IfExist,IfGreater,IfGreaterOrEqual,IfInString,IfLess,IfLessOrEqual,IfMsgBox,IfNotEqual,IfNotExist,IfNotInString,IfWinActive,IfWinExist,IfWinNotActive,IfWinNotExist,Process,Progress,SetBatchLines,SetEnv,SetFormat,SoundGetWaveVolume,SoundSetWaveVolume,SplashImage,SplashTextOff,SplashTextOn,StringGetPos,StringLeft,StringLen,StringLower,StringMid,StringReplace,StringRight,StringSplit,StringTrimLeft,StringTrimRight,StringUpper,Transform,UrlDownloadToFile,WinGet,WinGetActiveStats,WinGetActiveTitle,WinMenuSelectItem,WinSet"
vListCmd .= "FileEncoding,SendLevel,SetRegView"

vListDrv := "#ClipboardTimeout,#ErrorStdOut,#HotkeyInterval,#HotkeyModifierTimeout,#Hotstring,#IfWinActive,#IfWinExist,#IfWinNotActive,#IfWinNotExist,#Include,#IncludeAgain,#InstallKeybdHook,#InstallMouseHook,#KeyHistory,#MaxHotkeysPerInterval,#MaxThreads,#MaxThreadsBuffer,#MaxThreadsPerHotkey,#NoTrayIcon,#Persistent,#SingleInstance,#UseHook,#WinActivateForce"
vListDrv .= ",#AllowSameLineComments,#CommentFlag,#Delimiter,#DerefChar,#EscapeChar,#LTrim,#MaxMem,#NoEnv"
vListDrv .= ",#If,#IfTimeout,#InputLevel,#MenuMaskKey,#Warn"

vListCFS := StrReplace(vListCFS, ",", "|")
vListCmd := StrReplace(vListCmd, ",", "|")
vListDrv := StrReplace(vListDrv, ",", "|")
vListAll := vListCFS "|" vListCmd "|" vListDrv
vListBlock := StrReplace(vListBlock, ",", "|")
vListCommentOut := StrReplace(vListCommentOut, ",", "|")

oName := {}
Loop, Parse, vListAll, |
{
	oName[A_LoopField] := A_LoopField
}
;MsgBox, % Clipboard := JEE_ObjList(oName)

;notes on valid variable names:

;Concepts and Conventions
;https://autohotkey.com/docs/Concepts.htm#variables
;Maximum length: 253 characters.
;Allowed characters: Letters, numbers, non-ASCII characters, and the following symbols: _ # @ $

;Regular Expressions (RegEx) - Quick Reference
;https://autohotkey.com/docs/misc/RegEx-QuickRef.htm#subpat
;To use the parentheses without the side-effect of capturing a subpattern, specify ?: as the first two characters inside the parentheses; for example: (?:.*)

;RegEx for a variable name:
;vVar := "[_A-Za-z]\w*" ;an underscore/letter followed by 0 or more underscores/letters/digits
;vVar := "[_A-Za-z]\w{0,252}" ;more precise: initial character, then 0-252 characters
vVar := "(?:[_A-Za-z]|[^[:ascii:]])(?:\w|[^[:ascii:]]){0,252}" ;if allow non-ASCII characters

vIsInit := 1

if vIsCdLn
{
	Gosub SubConvert
	ExitApp
}
return

;==================================================

;MAIN SECTION 4 - HOTKEY 1

;==================================================

SubConvert: ;convert selected code
if !vIsInit
{
	MsgBox, % "error: script not yet initialised"
	return
}

#Include *i %A_ScriptDir%\ahk converter options.txt
;#Include *i %A_ScriptDir%\%A_ScriptNameNoExt% Options.txt ;no such variable as 'A_ScriptNameNoExt'
;e.g. included file could consist of:
;vDoJeeCustom := 1

;STAGE - INITIALISE
if vDoJeeCustom ;JEE custom settings
{
	vDoJeeMsgBox := 1, vDoJeeInputBox := 1
	vDoJeeStringRight := 1
	vDoJeeFileReadBin := 1
	vDoStringSplit := 1
	vDoIfWinXXXDrv := 1
	vOptRemCommaLoop := 0
	vDoLoopTidy := 1
	vDoLoopForceExp := 0
	vDoLoop := 0, vDoDoubleQuotes := 0 ;AHK v1 incompatible

	vOptExcludeLinesThatContainString := 1
	vOptExcludeString := ";[DO NOT CONVERT]"

	vOptVarValueSimple := 1, vOptVarValueAll := 1
	vOptVarDoCmdNml := 1, vOptVarDoCmdRtn := 1
	vDoJeeBetween := 1, vDoJeeIsType := 1
	vDoJeeContains := 1, vDoJeeIn := 1
	;vOptLogOmitCaseChange := 1
}

WinGetTitle, vWinTitle, A
if !vIsCdLn
	vText := JEE_GetSelectedText()
	;ControlGet, vText, Selected,, Edit1, A
else
	FileRead, vText, % vPathIn

oChange := {}
VarSetCapacity(vListChange, 1000000*2)
if vIsCdLn
	vListChange := vPathIn "`r`n"
else
	vListChange := vWinTitle "`r`n"

vTextOrig := vText
vOutput := ""
VarSetCapacity(vOutput, StrLen(vText)*2)
vText := StrReplace(vText, "`r`n", "`n")
oArrayOrig := StrSplit(vText, "`n")
oArrayNew := StrSplit(vText, "`n")
vIsConSec := 0
vLastCodeLine := 0
vConSecPfx := ""
vConSecSfx := ""
vUnused := JEE_StrUnused(1, vText)

;if vDoWinGetID applied, change definition, from:
;WinGet-ID=XSR,WinGetID
;to:
;WinGet-ID=XSR,WinExist
oXtra["WinGet-ID"].2 := vDoWinGetID ? "WinExist" : "WinGetID"

;STAGE - CHECK EACH LINE
Loop, % oArrayNew.Length()
{
	vTemp := oArrayNew[A_Index]
	if (SubStr(vTemp, 1, 1) = ";")
		vTempCode := "", vComments := vTemp
	else if (vPos := RegExMatch(vTemp, "[ `t]+;"))
		vTempCode := SubStr(vTemp, 1, vPos-1), vComments := SubStr(vTemp, vPos)
	else
		vTempCode := vTemp, vComments := ""
	vCode := LTrim(vTempCode)
	vWhitespace := SubStr(vTempCode, 1, StrLen(vTempCode)-StrLen(vCode))
	;==============================
	;HANDLE CONTINUATION SECTIONS
	if (SubStr(vCode, 1, 1) = "(") && !InStr(vCode, ")")
	{
		vIsConSec := 1
		if !vLastCodeLine || !(vLastCodeLine < A_Index)
		{
			MsgBox, % "error: " vLastCodeLine " " A_Index
			return
		}
		Loop, % A_Index - vLastCodeLine
			oArrayNew[vLastCodeLine-1+A_Index] := vConSecPfx oArrayOrig[vLastCodeLine-1+A_Index] vConSecSfx
	}
	if vIsConSec && !(vConSecPfx vConSecSfx = "")
		oArrayNew[A_Index] := vConSecPfx vTemp vConSecSfx
	if (SubStr(vCode, 1, 1) = ")")
		vIsConSec := 0
	if vIsConSec
		continue
	if !(vCode = "")
		vLastCodeLine := A_Index
	;==============================
	vCodeOrig := vCode
	;==============================
	if !vOptExcludeLinesInCommentSections
		if (SubStr(vCode, 1, 2) = "*/")
			vIsComment := 0
		else if (SubStr(vCode, 1, 2) = "/*")
			vIsComment := 1
	if vIsComment
		continue
	if vOptExcludeLinesThatContainString
	&& InStr(vComments, vOptExcludeString)
		continue
	;==============================
	;STAGE - COMMANDS - TIDY PARAMETERS (NO CONVERSION TAKES PLACES)
	;off by default
	if vOptTidyC
	&& (vCode ~= "^\w+, ")
	&& !(vCode ~= "Click, ") ;exclude Click because of the nonstandard parameters it uses
	{
		vCodeX := JEE_CmdPrepare(vCode, 1, vUnused, vIsErrorNoEnd)
		oTemp := StrSplit(vCodeX, vUnused)
		vCode := oTemp.1
		vParams := oCmd1[oTemp.1]
		Loop, % oTemp.Length() - 1
		{
			vTemp2 := Trim(oTemp[A_Index+1])
			vTemp2X := vTemp2
			if !(SubStr(vTemp2, 1, 2) = "% ")
			&& (vTemp2 ~= "%") && !(SubStr(vParams, A_Index, 1) ~= "[OI]")
				vTemp2 := JEE_Cvt(vTemp2)
			if (vTemp2 = "")
				vCode .= ","
			else if !(vTemp2 = vTemp2X)
				vCode .= ", % " vTemp2
			else
				vCode .= ", " vTemp2
		}
	}
	;==============================
	;STAGE - VAR = VALUE -> VAR := VALUE (ASSIGNMENT)
	if !(vCode = vCodeOrig)
		Sleep, 0

	;var = string -> var := "string"
	else if (vOptVarValueSimple || vOptVarValueAll)
	&& RegExMatch(vCode, vRx := "^(" vVar ") = ([A-Za-z]+)$")
		vCode := RegExReplace(vCode, vRx, "$1 := " Chr(34) "$2" Chr(34))
	;var = % value -> var := value
	else if (vOptVarValueSimple || vOptVarValueAll)
	&& RegExMatch(vCode, vRx := "^(" vVar ") ?= ?%[ `t]+(.*)$")
		vCode := RegExReplace(vCode, vRx, "$1 := $2")

	else if vOptVarValueAll
	{
		;var = 0 -> var := 0
		if RegExMatch(vCode, vRx := "^(" vVar ") = 0$")
			vCode := RegExReplace(vCode, vRx, "$1 := 0")
		;var = 123 -> var := 123
		else if RegExMatch(vCode, vRx := "^(" vVar ") = ([1-9]\d*)$")
			vCode := RegExReplace(vCode, vRx, "$1 := $2")
		;var = 0123 -> var := "0123" (num with leading zeros)
		else if RegExMatch(vCode, vRx := "^(" vVar ") = (0\d*)$")
			vCode := RegExReplace(vCode, vRx, "$1 := " Chr(34) "$2" Chr(34))
		;var = 123.123 -> var := 123.123
		else if RegExMatch(vCode, vRx := "^(" vVar ") = ([1-9]\d*\.\d*[1-9])$")
			vCode := RegExReplace(vCode, vRx, "$1 := $2")
		;var = 0123.123 -> var := "0123.123" (num with leading/trailing zeros)
		;var = 123.1230 -> var := "123.1230" (num with leading/trailing zeros)
		else if RegExMatch(vCode, vRx := "^(" vVar ") = (\d+)\.(\d+)$")
			vCode := RegExReplace(vCode, vRx, "$1 := " Chr(34) "$2.$3" Chr(34))
		;var = 0x123 -> var := 0x123
		else if RegExMatch(vCode, vRx := "^(" vVar ") = (0x[0-9A-Fa-f]+)$")
			vCode := RegExReplace(vCode, vRx, "$1 := $2")

		;var = -123 -> var := -123
		else if RegExMatch(vCode, vRx := "^(" vVar ") = (-[1-9]\d*)$")
			vCode := RegExReplace(vCode, vRx, "$1 := $2")
		;var = -0123 -> var := "-0123" (num with leading zeros)
		else if RegExMatch(vCode, vRx := "^(" vVar ") = (-0\d*)$")
			vCode := RegExReplace(vCode, vRx, "$1 := " Chr(34) "$2" Chr(34))
		;var = -123.123 -> var := -123.123
		else if RegExMatch(vCode, vRx := "^(" vVar ") = (-[1-9]\d*\.\d*[1-9])$")
			vCode := RegExReplace(vCode, vRx, "$1 := $2")
		;var = -0123.123 -> var := "-0123.123" (num with leading/trailing zeros)
		;var = -123.1230 -> var := "-123.1230" (num with leading/trailing zeros)
		else if RegExMatch(vCode, vRx := "^(" vVar ") = (-\d+\.\d+)$")
			vCode := RegExReplace(vCode, vRx, "$1 := " Chr(34) "$2" Chr(34))
		;var = -0x123 -> var := -0x123
		else if RegExMatch(vCode, vRx := "^(" vVar ") = (-0x[0-9A-Fa-f]+)$")
			vCode := RegExReplace(vCode, vRx, "$1 := $2")

		;var = string -> var := "string"
		else if RegExMatch(vCode, vRx := "^(" vVar ") =( +)([A-Za-z ,'_]+)$")
			vCode := RegExReplace(vCode, vRx, "$1 :=" "$2" Chr(34) "$3" Chr(34))
		else if RegExMatch(vCode, vRx := "^(" vVar ") =( +)([\w ,']+)$")
			vCode := RegExReplace(vCode, vRx, "$1 :=" "$2" Chr(34) "$3" Chr(34))
		else if RegExMatch(vCode, vRx := "^(" vVar ") =( +)([\w ,':\\.]+)$")
			vCode := RegExReplace(vCode, vRx, "$1 :=" "$2" Chr(34) "$3" Chr(34))
		else if RegExMatch(vCode, vRx := "^(" vVar ") =( +)([^%``""]+)$")
			vCode := RegExReplace(vCode, vRx, "$1 :=" "$2" Chr(34) "$3" Chr(34))
		else if RegExMatch(vCode, vRx := "O)^(" vVar ") =( +)([^``""]+)$", o)
			vCode := o.1 " :=" o.2 JEE_Cvt(o.3)
		else if RegExMatch(vCode, vRx := "O)^(" vVar ") =( +)([^``]+)$", o)
			vCode := o.1 " :=" o.2 JEE_Cvt(o.3)
		else if RegExMatch(vCode, vRx := "O)^(" vVar ") =( +)(.+)$", o)
		&& !RegExMatch(vCode, "``[;,%]")
			vCode := o.1 " :=" o.2 JEE_Cvt(o.3)
		else if RegExMatch(vCode, vRx := "O)^(" vVar ") =( +)(.+)$", o)
			vCode := o.1 " :=" o.2 JEE_Cvt(o.3)
	}
	;==============================
	;STAGE - +=/-= (DATEADD/DATEDIFF) (INCREMENT/DECREMENT)
	;off always
	;commented out (via '&& 0') because of false positives
	;DateAdd(DateTime, Time, TimeUnits)
	if RegExMatch(vCode, vRx := "^" vVar " \+= ")
	&& !InStr(vCode, "``")
	&& 0
	{
		vCodeX := "Cmd, " StrReplace(vCode, " += ", ", ", "", 1)
		vCodeX := JEE_CmdPrepare(vCodeX, 1, vUnused, vIsErrorNoEnd)
		oTemp := StrSplit(vCodeX, vUnused)
		if (oTemp.Length() = 4)
			vCode := Trim(oTemp.2) " := DateAdd(" Trim(oTemp.2) ", " JEE_Cvt(oTemp.3, "E") ", " JEE_Cvt(oTemp.4) ")"
	}
	;commented out (via '&& 0') because of false positives
	;DateDiff
	else if RegExMatch(vCode, vRx := "^" vVar " -= ")
	&& !InStr(vCode, "``")
	&& 0
	{
		vCodeX := "Cmd, " StrReplace(vCode, " -= ", ", ", "", 1)
		vCodeX := JEE_CmdPrepare(vCodeX, 1, vUnused, vIsErrorNoEnd)
		oTemp := StrSplit(vCodeX, vUnused)
		if (oTemp.Length() = 4)
			vCode := Trim(oTemp.2) " := DateDiff(" Trim(oTemp.2) ", " JEE_Cvt(oTemp.3, "E") ", " JEE_Cvt(oTemp.4) ")"
	}
	;==============================
	;STAGE - IF (CONTROL FLOW STATEMENT)
	;STAGE - IF VAR OPERATOR VALUE
	;STAGE - IF VAR BETWEEN/CONTAINS/IN/IS TYPE
	;if var = string
	;if var = %var%
	if RegExMatch(vCode, vRx := "iO)^if[ `t]+(" vVar ")[ `t]*(>|<|>=|<=|=|<>|!=)[ `t]*(.*)$", o)
	{
		vCode := "if (" o.1 " " o.2 " " JEE_Cvt(o.3) ")"
	}

	;between
	;if var [not] between %lbound% and %ubound%
	else if vDoJeeBetween
	&& RegExMatch(vCode, vRx := "iO)^if (" vVar ")( not|) between (.*?) and (.*)$", o)
	{
		vPfx := (o.2 = "") ? "" : "!"
		v3 := JEE_Cvt(o.3), v4 := JEE_Cvt(o.4)
		if vDoJeeBetween
			vCode := "if " vPfx "JEE_Between(" o.1 ", " v3 ", " v4 ")"
		else if !vPfx
			vCode := "if (" o.1 " >= " v3 ") && (" o.1 " <= " v4 ")"
		else
			vCode := "if (" o.1 " < " v3 ") || (" o.1 " > " v4 ")"
	}

	;type
	;is type
	;if var is [not] type
	else if vDoJeeIsType
	&& RegExMatch(vCode, vRx := "iO)^if (" vVar ") is( not|) (.*)$", o)
	{
		vPfx := (o.2 = "") ? "" : "!"
		vCode := "if " vPfx "JEE_StrIsType(" o.1 ", " JEE_Cvt(o.3) ")"
	}

	;in/contains
	;conditional on: vDoJeeIn / vDoJeeContains
	;if var [not] contains %list%
	;if var [not] in %list%
	else if RegExMatch(vCode, vRx := "iO)^if[ `t]+(" vVar ")([ `t]+not|)[ `t]+(in|contains)[ `t]+(.*)$", o)
	&& !InStr(vCode, ",,")
	&& ((o.3 = "in") && vDoJeeIn || (o.3 = "contains") && vDoJeeContains)
	{
		vPfx := (o.2 = "") ? "" : "!"
		vFunc := (o.3 = "in") ? "JEE_MX" : "JEE_MC"

		;trying to convert to InStr where possible, is not necessarily a good idea,
		;e.g. there might be a force expression containing variables, that may or may not contain literal commas intended as delimiters
		;if (o.3 = "contains") && !InStr(o.4, ",")
		;	vFunc := "InStr"

		vCode := "if " vPfx vFunc "(" o.1 ", " JEE_Cvt(o.4, "S2") ")"
	}
	;==============================
	;STAGE - CONTROL FLOW STATEMENTS WITH PARENTHESES
	;e.g. 'if(' -> 'if ('
	if RegExMatch(vCode, "iO)^(" vListCFS ")[ `t]*(\(.*)", o)
	{
		vMatch := oName[o.1] " " o.2
	}
	;==============================
	;STAGE - COMMANDS - ADD COMMAS (AND CASE CORRECT COMMAND/CONTROL FLOW STATEMENT/DIRECTIVE NAMES)
	;note: if the script does 'continue' at any point, these changes are ignored
	;add initial commas to commands/control flow statements/directives
	;the converter expects the commas,
	;for conversion later,
	;they are optionally removed at the end
	if RegExMatch(vCode, vRx := "iO)^(" vListAll ")[ `t]+(?!:=)", o)
	{
		if (oName[o.1] ~= "^(" vListCFS ")$")
			vCode := oName[o.1] SubStr(vCode, StrLen(o.1)+1)
		else
			vCode := oName[o.1] ", " LTrim(SubStr(vCode, StrLen(o.1)+1))
	}
	else if RegExMatch(vCode, vRx := "iO)^(" vListAll "),", o)
	{
		vCode := oName[o.1] SubStr(vCode, StrLen(o.1)+1)
	}
	else if RegExMatch(vCode, vRx := "iO)^(" vListAll ")$", o)
	{
		vCode := oName[o.1]
	}
	;==============================
	;STAGE - AHK v1 TO AHK v2
	if (vCode ~= "^\w+,[ ,]")
	&& (vOptMode = 12)
	{
		vCodeX := JEE_CmdPrepare(vCode, 1, vUnused, vIsErrorNoEnd)
		oTemp := StrSplit(vCodeX, vUnused)
	}

	if !(vListCommentOut = "")
	&& (vCode ~= "^(" vListCommentOut ")( |,|$)")
	{
		vCode := ";" vCode
	}
	;==================================================
	;STAGE - LOOP (CONTROL FLOW STATEMENT)
	;Loop
	;Loop [Count]
	;Loop Parse, String [, Delimiters, OmitChars]
	;Loop Files, FilePattern [, Mode]
	;Loop Reg, KeyName [, Mode]
	;Loop Read, InputFile [, OutputFile]
	if (vDoLoopForceExp || vDoLoop || vDoLoopTidy)
	&& (vCode ~= "^Loop ")
	{
		vCode := StrReplace(vCode, " ", ", ", "", 1)
	}
	if (vDoLoopForceExp || vDoLoop)
	&& (vCode ~= "^Loop, ")
	{
		;this script uses '% ' as a coding trick,
		;e.g. if JEE_Cvt() sees a leading '% ',
		;it returns the parameter minus the leading '% '
		vCodeX := JEE_CmdPrepare(vCode, 1, vUnused, vIsErrorNoEnd)
		oTemp := StrSplit(vCodeX, vUnused)
		vParams := "SSSSS"
		oTemp.2 := Trim(oTemp.2)
		if (oTemp.2 = "Parse")
			vParams := "SISSS"
		if (oTemp.2 ~= "^(Parse|Files|Reg|Read)$")
			oTemp.2 := "% " oTemp.2
		else if !(oTemp.Length() = 2)
			continue
		if vDoLoopForceExp && !vDoLoop
		{
			if (oTemp.Length() = 2) && !(oTemp.2 ~= "^\d+$")
				oTemp.2 := "% % " JEE_Cvt(oTemp.2)
			Loop, 3
			{
				if (oTemp.2 = "% Parse") && (A_Index = 1)
				{
					oTemp.3 := "% " Trim(oTemp.3)
					continue
				}
				vTemp := JEE_Cvt(oTemp[A_Index+2])
				if !(vTemp = "")
					oTemp[A_Index+2] := "% % " vTemp
			}
		}
		vCode := JEE_ArrayToFunc(oTemp, vParams)
		vCode := StrReplace(vCode, "(", ", ", "", 1)
		vCode := SubStr(vCode, 1, -1)
	}
	if vDoLoopTidy && !vDoLoopForceExp && !vDoLoop
	&& (vCode ~= "^Loop, ")
	{
		;this script uses '% ' as a coding trick,
		;e.g. if JEE_Cvt() sees a leading '% ',
		;it returns the parameter minus the leading '% '
		vCodeX := JEE_CmdPrepare(vCode, 1, vUnused, vIsErrorNoEnd)
		oTemp := StrSplit(vCodeX, vUnused)
		Loop, % oTemp.Length()
		{
			oTemp[A_Index] := Trim(oTemp[A_Index])
			if (oTemp[A_Index] ~= "``,")
				oTemp[A_Index] := "% " JEE_Cvt(oTemp[A_Index])
			if (A_Index = 1)
				continue
			else if (Trim(oTemp.2) = "% Parse") && (A_Index = 3)
				oTemp.3 := "% " Trim(oTemp.3)
			else if !(SubStr(oTemp[A_Index], 1, 2) = "% ")
			&& InStr(oTemp[A_Index], "%")
				oTemp[A_Index] := "% % " JEE_Cvt(oTemp[A_Index])
			else
				oTemp[A_Index] := "% " oTemp[A_Index]
		}
		vCode := JEE_ArrayToFunc(oTemp, vParams)
		vCode := StrReplace(vCode, "(", ", ", "", 1)
		vCode := SubStr(vCode, 1, -1)
	}
	;==================================================
	;STAGE - DIRECTIVES
	;#IfWin(Not)Active/IfWin(Not)Exist
	if vDoIfWinXXXDrv
	&& (vCode ~= "^#IfWin(Not)?(Active|Exist)$")
		vCode := "#If"
	if vDoIfWinXXXDrv
	&& RegExMatch(vCode, "O)^#IfWin(Not)?(Active|Exist),[ ,]", o)
	{
		vCodeX := SubStr(vCode, 2)
		vCodeX := JEE_CmdPrepare(vCodeX, 1, vUnused, vIsErrorNoEnd)
		oTemp := StrSplit(vCodeX, vUnused)
		vPfx := (o.1 = "") ? "" : "!"
		oTemp.1 := "#If " vPfx "Win" o.2
		vCode := JEE_ArrayToFunc(oTemp, "SSSSSS")
	}
	if vDoIfWinXXXDrv
	&& RegExMatch(vCode, "O)^#IfWin(Not)?(Active|Exist) ", o)
	{
		vCodeX := StrReplace(vCode, " ", ", ", "", 1)
		vCodeX := SubStr(vCodeX, 2)
		vCodeX := JEE_CmdPrepare(vCodeX, 1, vUnused, vIsErrorNoEnd)
		oTemp := StrSplit(vCodeX, vUnused)
		vPfx := (o.1 = "") ? "" : "!"
		oTemp.1 := "#If " vPfx "Win" o.2
		vCode := JEE_ArrayToFunc(oTemp, "SSSS")
	}
	;==================================================
	;STAGE - GENERAL CONVERT COMMANDS / CONVERT SPECIFIC COMMANDS / CONVERT IFXXX CONTROL FLOW STATEMENTS
	;COMMAND - (no-parameter commands)
	;COMMAND - EnvUpdate
	if (vCode = "EnvUpdate")
	&& vOptVarDoCmdNml
		vCode := "SendMessage(0x1A,,,, ""ahk_id 0xFFFF"") `;env update"
	else if (vCode = "Input")
	&& vOptVarDoCmdNml
		vCode .= "End()"
	else if (vCode = "MsgBox")
	&& vDoJeeMsgBox
		vCode := "JEE_MsgBox()"
	else if (vCode ~= "^(" vListCmd1NP ")$")
	&& vOptVarDoCmdNml
		vCode .= "()"
	else if (oXtra[oTemp.1].1 ~= "R") && !vOptVarDoCmdRtn
		continue
	else if !(oXtra[oTemp.1].1 ~= "R") && !vOptVarDoCmdNml
	&& oXtra.HasKey(oTemp.1)
		continue

	;COMMAND - Control|ControlGet|Drive|DriveGet|Process|WinGet|WinSet
	;note: this section ignores commands with an 'X' label (apart from the 7 commands listed in the line above)
	;ignored commands are handled in 'COMMAND - MULTIPLE - FURTHER' if they have a code block there (otherwise they are ignored)
	;COMMAND - MULTIPLE e.g.:
	;... BlockInput
	;... Click
	;... ClipWait
	;... ControlClick|ControlFocus|ControlGetFocus|ControlGetPos|ControlGetText|ControlMove|ControlSend|ControlSendRaw|ControlSetText
	;... CoordMode
	;... Critical
	;... DetectHiddenText|DetectHiddenWindows
	;... DriveSpaceFree
	;... EnvGet|EnvSet
	;... Exit|ExitApp
	;... FileCopy|FileCopyDir|FileCreateDir|FileCreateShortcut|FileDelete|FileEncoding|FileGetAttrib|FileGetShortcut|FileGetSize|FileGetTime|FileGetVersion|FileInstall|FileMove|FileMoveDir|FileRecycle|FileRecycleEmpty|FileRemoveDir|FileSelectFile|FileSelectFolder|FileSetTime
	;... FormatTime
	;... GroupActivate|GroupAdd|GroupClose|GroupDeactivate
	;... Hotkey
	;... ImageSearch
	;... IniDelete|IniRead|IniWrite
	;... KeyWait
	;... ListLines
	;... MouseClick|MouseClickDrag|MouseGetPos|MouseMove
	;... OutputDebug
	;... Pause
	;... PostMessage
	;... Run|RunAs|RunWait
	;... Send|SendEvent|SendInput|SendLevel|SendMode|SendPlay|SendRaw
	;... SendMessage
	;... SetCapsLockState|SetControlDelay|SetDefaultMouseSpeed|SetKeyDelay|SetMouseDelay|SetNumLockState|SetRegView|SetScrollLockState|SetStoreCapsLockMode|SetTitleMatchMode|SetWinDelay|SetWorkingDir
	;... SetTimer
	;... Shutdown
	;... Sleep
	;... SoundBeep|SoundGet|SoundPlay|SoundSet
	;... SplitPath
	;... StatusBarGetText|StatusBarWait
	;... StringCaseSense|StringLen
	;... Suspend
	;... Thread
	;... ToolTip
	;... UrlDownloadToFile
	;... WinActivate|WinActivateBottom|WinClose|WinGetClass|WinGetPos|WinGetText|WinGetTitle|WinHide|WinKill|WinMaximize|WinMenuSelectItem|WinMinimize|WinRestore|WinShow|WinWait|WinWaitActive|WinWaitClose|WinWaitNotActive
	else if (vCode ~= "^(" vXtra "),[ ,]")
	&& (oXtra[oTemp.1].1 ~= "[URP]$")
	&& (!InStr(oXtra[oTemp.1].1, "X") || (vCode ~= "^(Control|ControlGet|Drive|DriveGet|Process|WinGet|WinSet),"))
	&& (vOptMode = 12)
	&& !(vCode ~= "^(StringLower|StringUpper),[ ,]")
	&& ((vListBlock = "") || !(vCode ~= "^(" vListBlock "),[ ,]"))
	{
		vParams := oCmd1[oTemp.1]
		vCmdX := ""

		if (oXtra[oTemp.1].1 = "P")
		{
			vParams := oXtra[oTemp.1].3
			vCmdX := oTemp.RemoveAt(1)
			oTemp := JEE_ObjShuffleFrom(oTemp, vParams)
			oTemp.InsertAt(1, vCmdX)
			Loop, % oTemp.Length()
			{
				vTempXX := oTemp.Pop()
				if !(vTempXX = "")
				{
					oTemp.Push(vTempXX)
					break
				}
			}
		}

		if (oXtra[oTemp.1].1 = "XSR")
		{
			if (Trim(oTemp.1) ~= "^(WinGet)$")
				if (Trim(oTemp.3) ~= "^(List)$")
					continue
			if (Trim(oTemp.3) ~= "^(ControlList|ControlListHwnd)$")
				continue

			vParams := oCmd1[oTemp.1]
			vParams := SubStr(vParams, 1, 1) SubStr(vParams, 3)
			vCmdX := oTemp.1 "-" Trim(oTemp.3)
			if !oXtra.HasKey(vCmdX)
				continue
			vSubCmd := oTemp.RemoveAt(3)

			if (oTemp.1 = "ControlGet") && !(Trim(vSubCmd) ~= "^(List|FindString|Line)$")
				oTemp.RemoveAt(3), vParams := SubStr(vParams, 1, -1)
		}
		else if (oXtra[oTemp.1].1 = "XSU")
		{

			if (oTemp.1 = "Control")
				if (Trim(oTemp.2) ~= "^(Enable|Check)$")
					oTemp.3 := 1
				else if (Trim(oTemp.2) ~= "^(Disable|Uncheck)$")
					oTemp.3 := 0
				else if (Trim(oTemp.2) ~= "^(TabLeft|TabRight)$")
				{
					oTabX := oTemp.Clone()
					oTabX.RemoveAt(2, 2)
					oTabX.1 := "ControlGetTab"
					vPfxX := (Trim(oTemp.2) ~= "^(TabLeft)$") ? "-" : ""
					oTemp.3 := "% " vPfxX JEE_Cvt(oTemp.3, "E") "+" JEE_ArrayToFunc(oTabX, "SSSSS")
				}
				else if (Trim(oTemp.2) ~= "^(Hide|HideDropDown|Show|ShowDropDown)$")
					oTemp.RemoveAt(3)
				;other: Add|Choose|ChooseString|Delete|EditPaste|ExStyle|Style

			if (oTemp.1 = "WinSet")
				if (Trim(oTemp.2) ~= "^(Bottom|Redraw|Top)$")
					oTemp.RemoveAt(3)
				else if (Trim(oTemp.2) ~= "^(Enable)$")
					oTemp.3 := 1
				else if (Trim(oTemp.2) ~= "^(Disable)$")
					oTemp.3 := 0

			vParams := oCmd1[oTemp.1]
			vParams := SubStr(vParams, 2)
			vCmdX := oTemp.1 "-" Trim(oTemp.RemoveAt(2))
			if !oXtra.HasKey(vCmdX)
				continue
		}

		if (oXtra[oTemp.1].1 ~= "R$")
			vPfx := Trim(oTemp.RemoveAt(2)) " := ", vParams := SubStr(vParams, 2)
		else
			vPfx := ""

		if !(vCmdX = "")
			oTemp.1 := vCmdX
		if !(oXtra[oTemp.1].2 = "")
			oTemp.1 := oXtra[oTemp.1].2
		if (oTemp.Length() <= StrLen(vParams)+1)
			vCode := vPfx JEE_ArrayToFunc(oTemp, vParams)
		else
			vCode := vCodeOrig
	}

	;COMMAND - MULTIPLE - FURTHER
	;note: this will tidy parameters in any commands that haven't been converted to functions
	else if (vCode ~= "^(" vListCmd1 "),[ ,]")
	&& oCmd1.HasKey(oTemp.1)
	&& !(vCode ~= "^(" vListCmd1X "),[ ,]")
	&& (vOptMode = 12)
	{
		vParams := oCmd1[oTemp.1]
		if (oTemp.Length() <= StrLen(vParams)+1)
			vCode := JEE_ArrayToCmd(oTemp, vParams)
		else
			vCode := vCodeOrig
	}

	;COMMAND - MULTIPLE - SPECIAL
	;... EnvAdd|EnvSub|EnvMult|EnvDiv
	;... FileAppend
	;... FileRead
	;... FileReadLine
	;... FileSetAttrib
	;... GetKeyState
	;... IfEqual|IfGreater|IfGreaterOrEqual|IfLess|IfLessOrEqual|IfNotEqual
	;... IfExist|IfNotExist
	;... IfInString|IfNotInString
	;... IfWinActive|IfWinNotActive
	;... IfWinExist|IfWinNotExist
	;... Input
	;... InputBox
	;... Menu
	;... MsgBox
	;... PixelGetColor
	;... PixelSearch
	;... Progress
	;... Random
	;... RegDelete
	;... RegRead
	;... RegWrite
	;... SetEnv
	;... Sort
	;... SoundGetWaveVolume|SoundSetWaveVolume
	;... SplashImage
	;... SplashTextOff
	;... SplashTextOn
	;... StringGetPos
	;... StringLeft|StringRight
	;... StringLower|StringUpper
	;... StringMid
	;... StringReplace
	;... StringSplit
	;... StringTrimLeft|StringTrimRight
	;... SysGet
	;... Transform
	;... TrayTip
	;... WinGetActiveStats
	;... WinGetActiveTitle
	;... WinMove
	;... WinSetTitle
	else if (vCode ~= "^(" vListCmd1X "),[ ,]")
	&& oCmd1.HasKey(oTemp.1)
	&& (vOptMode = 12)
	&& ((vListBlock = "") || !(vCode ~= "^(" vListBlock "),[ ,]"))
	{
		vCodeX := JEE_CmdPrepare(vCode, 1, vUnused, vIsErrorNoEnd)
		oTemp := StrSplit(vCodeX, vUnused)
		if oXtra[oTemp.1].HasKey(2)
			vCmdX := oXtra[oTemp.1].2
		else
			vCmdX := oTemp.1
		for vKey, vValue in oTemp
			oTemp[vKey] := Trim(vValue)

		;COMMAND - EnvAdd|EnvSub|EnvMult|EnvDiv
		if (oTemp.1 ~= "^(EnvAdd|EnvSub|EnvMult|EnvDiv)$")
		&& (oTemp.Length() = 3)
		{
			vOp := {Add:"+",Sub:"-",Mult:"*",Div:"/"}[SubStr(oTemp.1, 4)]
			vCode := oTemp.2 " " vOp "= " JEE_Cvt(oTemp.3, "E")
		}
		if (oTemp.1 ~= "^(EnvAdd|EnvSub)$")
		&& (oTemp.Length() = 4)
			vCode := oTemp.2 " := " vCmdX "(" oTemp.2 ", " JEE_Cvt(oTemp.3, "E") ", " JEE_Cvt(oTemp.4) ")"

		;COMMAND - FileAppend
		;Text, EOL/Filename, Encoding
		;Text, Filename, Options
		if (oTemp.1 = "FileAppend")
		{
			if InStr(vCode, "ClipboardAll")
				continue
			if (oTemp.2 = "")
				oTemp.2 := "% """""
			oTemp.3 := JEE_Cvt(oTemp.3)
			if (SubStr(oTemp.3, 1, 4) = """*"" ")
				vOpt := "", oTemp.3 := "% " SubStr(oTemp.3, 5)
			else
				oTemp.3 := "% " oTemp.3, oTemp.4 := "% " JEE_CvtJoin("SS", "``n ", oTemp.4)
			;handle: FileAppend,, % vPath -> FileAppend("", vPath)
			if (oTemp.2 = "% """"") && (oTemp.4 = "% ""``n""")
				oTemp.4 := ""
			JEE_ObjPopBlank(oTemp)
			vCode := JEE_ArrayToFunc(oTemp, "SSS")
		}

		;COMMAND - FileRead
		;v1: OutputVar Options/Filename
		;v2: Filename Options
		;from: FileRead, vData, *c %vPath%
		;to: JEE_FileReadBin(vData, vPath)
		if (oTemp.1 = "FileRead") && vDoJeeFileReadBin
		&& RegExMatch(vCode, "O)FileRead, (" vVar "), \*c %(" vVar ")%", o)
		{
			vCode := "JEE_FileReadBin(" o.1 ", " o.2 ")"
		}
		else if (oTemp.1 = "FileRead")
		{
			vCode := Trim(oTemp.RemoveAt(2)) " := "
			vOpt := ""
			if RegExMatch(oTemp.2, "O)\*(m\d+)", o)
				vOpt := o.1, oTemp.2 := RegExReplace(oTemp.2, "\*(m\d+)")
			if InStr(oTemp.2, "*t")
				vOpt .= " ``n", oTemp.2 := StrReplace(oTemp.2, "*t")
			if RegExMatch(oTemp.2, "O)\*(P\d+)", o)
				vOpt .= " C" o.1, oTemp.2 := RegExReplace(oTemp.2, "\*(P\d+)")
			if InStr(oTemp.2, "*")
				continue
			if (vOpt = "")
				oTemp.3 := vOpt

			JEE_ObjPopBlank(oTemp)
			vCode .= JEE_ArrayToFunc(oTemp, "SS")
		}

		;COMMAND - FileReadLine
		if (oTemp.1 = "FileReadLine") && vDoFileReadLine
		{
			vCode := oTemp.2 " := StrSplit(FileRead(" JEE_Cvt(oTemp.3) "), ""``n"", ""``r"")[" JEE_Cvt(oTemp.4, "E") "] `;file read line"
		}

		;COMMAND - FileSetAttrib
		if (oTemp.1 = "FileSetAttrib")
		{
			if !(oTemp.4 ~= "^(|0|1|2)$")
			|| !(oTemp.5 ~= "^(|0|1)$")
				continue
			vNew := ""
			(oTemp.4 = 1) && vNew .= "FD"
			(oTemp.4 = 2) && vNew .= "D"
			(oTemp.5 = 1) && vNew .= "R"
			oTemp.4 := vNew, oTemp.5 := ""
			JEE_ObjPopBlank(oTemp)
			vCode := JEE_ArrayToFunc(oTemp, "SSS")
		}

		;COMMAND - GetKeyState
		if (oTemp.1 = "GetKeyState") && vDoGetKeyState
		{
			vPfx := (oTemp.RemoveAt(2)) " := "
			vCode := vPfx "{0:""U"",1:""D""}[" JEE_ArrayToFunc(oTemp) "]"
		}

		;COMMAND - IfEqual|IfGreater|IfGreaterOrEqual|IfLess|IfLessOrEqual|IfNotEqual
		if (oTemp.1 ~= "^(IfEqual|IfGreater|IfGreaterOrEqual|IfLess|IfLessOrEqual|IfNotEqual)$")
		&& (oTemp.Length() = 3)
		{
			vOp := {IfEqual:"=",IfGreater:">",IfGreaterOrEqual:">=",IfLess:"<",IfLessOrEqual:"<=",IfNotEqual:"<>"}[oTemp.1]
			vCode := "if (" oTemp.2 " " vOp " " JEE_Cvt(oTemp.3) ")"
		}

		;COMMAND - IfExist|IfNotExist
		;COMMAND - IfWinActive|IfWinNotActive
		;COMMAND - IfWinExist|IfWinNotExist
		if (oTemp.1 ~= "^If.*(Active|Exist)$") ;If(Not)Exist/IfWin(Not)Active/IfWin(Not)Exist
		{
			oTemp.1 := oXtra[oTemp.1].2
			JEE_ObjPopBlank(oTemp)
			vCode := JEE_ArrayToFunc(oTemp, "SSSS")
		}

		;COMMAND - IfInString|IfNotInString
		if (oTemp.1 = "IfInString")
		&& (oTemp.Length() = 3)
		{
			vCode := "if InStr(" oTemp.2 ", " JEE_Cvt(oTemp.3) ")"
		}
		if (oTemp.1 = "IfNotInString")
		&& (oTemp.Length() = 3)
		{
			vCode := "if !InStr(" oTemp.2 ", " JEE_Cvt(oTemp.3) ")"
		}

		;COMMAND - Input
		if (oTemp.1 = "Input")
		{
			vCode := Trim(oTemp.RemoveAt(2)) " := "
			vCode .= JEE_ArrayToFunc(oTemp, "SSS")
		}

		;COMMAND - InputBox
		;InputBox, OutputVar [, Title, Prompt, HIDE, Width, Height, X, Y, Font, Timeout, Default]
		;InputBox([Text, Title, Options, Default])
		;1:OutputVar 2:Title 3:Prompt[Text] 4:HIDE
		;5678: Width Height X Y
		;9,10,11: Font Timeout Default
		;2:Text[Prompt] 3:Title 4:Options 5:Default
		if (oTemp.1 = "InputBox")
		{
			Loop, % oTemp.Length()
				oTemp[A_Index] := Trim(oTemp[A_Index])
			oTemp.RemoveAt(1)
			vVar := Trim(oTemp.1)
			oNew := ["InputBox"]
			if !(oTemp.2 = "")
				oNew.3 := "% " JEE_Cvt(oTemp.2)
			if !(oTemp.3 = "")
				oNew.2 := "% " JEE_Cvt(oTemp.3)
			if !(oTemp.7 = "")
				oNew.4 .= " "" X"" " JEE_Cvt(oTemp.7)
			if !(oTemp.8 = "")
				oNew.4 .= " "" Y"" " JEE_Cvt(oTemp.8)
			if !(oTemp.5 = "")
				oNew.4 .= " "" W"" " JEE_Cvt(oTemp.5)
			if !(oTemp.6 = "")
				oNew.4 .= " "" H"" " JEE_Cvt(oTemp.6)
			if !(oTemp.10 = "")
				oNew.4 .= " "" T"" " JEE_Cvt(oTemp.10)
			if (oTemp.4 = "HIDE")
				oNew.4 .= " "" Password*"""
			else if !(oTemp.4 = "")
				oNew.4 .= " (" JEE_Cvt(oTemp.4) " = ""HIDE"" ? "" Password*"" : """")"
			if !(oTemp.11 = "")
				oNew.5 := "% " JEE_Cvt(oTemp.11)
			if !(oNew.4 = "")
				oNew.4 := Trim(oNew.4), oNew.4 := JEE_ExpTrim(oNew.4)
			if (SubStr(oNew.4, 1, 2) = Chr(34) " ")
				oNew.4 := Chr(34) SubStr(oNew.4, 3)
			if !(oNew.4 = "")
				oNew.4 := "% " oNew.4

			if vDoJeeInputBox
			{
				vDefault := oNew.RemoveAt(5)
				oNew.InsertAt(3, vDefault)
				vPfx := "JEE_"
			}
			else
				vPfx := ""
			JEE_ObjPopBlank(oNew)
			vCode := vVar " := " vPfx JEE_ArrayToFunc(oNew, "SSSS")
		}

		;COMMAND - Menu
		if (oTemp.1 = "Menu")
		{
			;Menu, Tray, Click, 1 -> A_TrayMenu.ClickCount := 1
			if (oTemp.1 = "Menu")
			&& (oTemp.2 = "Tray")
			&& (oTemp.3 = "Click")
				vCode := "A_TrayMenu.ClickCount := " JEE_Cvt(oTemp.4)
		}

		;COMMAND - MsgBox
		;Type, Title, Text, Timeout
		;Text, Title, Options
		if (oTemp.1 = "MsgBox")
		{
			vPfx := vDoJeeMsgBox ? "JEE_" : ""
			if (oTemp.Length() = 2)
				vCode := vPfx JEE_ArrayToFunc(oTemp, "S")
			else
			{
				if (oTemp.5 = "")
					vOpt := JEE_Cvt(oTemp.2)
				else
					vOpt := JEE_ExpTrim(JEE_CvtJoin("SSS", oTemp.2, "% "" T""", oTemp.5))
				if !(vOpt = "")
					vOpt := "% " vOpt
				oNew := ["MsgBox", oTemp.4, oTemp.3, vOpt]
				JEE_ObjPopBlank(oNew)
				vCode := "JEE_" JEE_ArrayToFunc(oNew, "SSS")
			}
		}

		;COMMAND - PixelGetColor
		if (oTemp.1 = "PixelGetColor")
		{
			if !(JEE_Cvt(oTemp.5) = Chr(34) "RGB" Chr(34))
				continue
			oTemp.5 := ""
			vCode := Trim(oTemp.RemoveAt(2)) " := "
			JEE_ObjPopBlank(oTemp)
			vCode .= JEE_ArrayToFunc(oTemp, "EES")
		}

		;COMMAND - PixelSearch
		if (oTemp.1 = "PixelSearch")
		{
			if !(JEE_Cvt(oTemp.10) = Chr(34) "RGB" Chr(34) )
			&& !(JEE_ColRGBIsBGR(Trim(oTemp.8)) && (oTemp.10 = ""))
				continue
			oTemp.10 := ""
			JEE_ObjPopBlank(oTemp)
			vCode := JEE_ArrayToFunc(oTemp, "OOEEEEEES")
		}

		;COMMAND - Progress
		if (oTemp.1 = "Progress")
		&& vDoJeeProgress
		{
			oTemp.1 := "JEE_Progress" ;[NOT IMPLEMENTED]
			vCode := JEE_ArrayToFunc(oTemp, "SSSSS")
		}

		;COMMAND - Random
		if (oTemp.1 = "Random")
		{
			if (oTemp.2 = "")
				vCode := "RandomSeed(" JEE_Cvt(oTemp.3, "E") ")"
			else
				vTemp := oTemp.RemoveAt(2), vCode := vTemp " := " JEE_ArrayToFunc(oTemp, "EE")
		}

		;COMMAND - RegDelete
		;v1o: RegDelete RK SK   ValueName
		;v1n: RegDelete KeyName ValueName
		;v2:  RegDelete KeyName ValueName
		;v2:  RegDeleteKey KeyName
		if (oTemp.1 = "RegDelete")
		{
			vIsReady := 0
			if !vIsReady && (oTemp.Length() = 4)
				if (oTemp.3 = "")
					oTemp.RemoveAt(3), vIsReady := 1
				else
					oTemp.2 := "% " JEE_CvtJoin("SSS", oTemp.2, "\", oTemp.RemoveAt(3)),, vIsReady := 1
			if !vIsReady && (oTemp.Length() = 3)
			&& InStr(oTemp.2, "\")
				vIsReady := 1
			if !vIsReady
				continue
			if (JEE_Cvt(oTemp.4) = Chr(34) "AHK_DEFAULT" Chr(34))
				oTemp.4 := ""
			JEE_ObjPopBlank(oTemp)
			vCode := JEE_ArrayToFunc(oTemp, "SSS")
		}

		;COMMAND - RegRead
		;v1o: OutputVar KeyName ValueName
		;v1n: OutputVar RK SK   ValueName
		;v2:            KeyName ValueName
		if (oTemp.1 = "RegRead")
		{
			vCode := Trim(oTemp.RemoveAt(2)) " := "
			vIsReady := 0
			if (oTemp.Length() = 1) || (oTemp.Length() = 2)
				vIsReady := 1
			if !vIsReady && (oTemp.Length() = 4)
				if (oTemp.3 = "")
					oTemp.RemoveAt(3), vIsReady := 1
				else
					oTemp.2 := "% " JEE_CvtJoin("SSS", oTemp.2, "\", oTemp.RemoveAt(3)), vIsReady := 1
			if !vIsReady && (oTemp.Length() = 3)
			&& InStr(oTemp.2, "\")
				vIsReady := 1
			if !vIsReady && (oTemp.Length() = 3)
			&& !RegExMatch(oTemp.2, "[\%]")
				oTemp.2 := "% " JEE_CvtJoin("SSS", oTemp.2, "\", oTemp.RemoveAt(3)), vIsReady := 1
			if !vIsReady
				continue
			JEE_ObjPopBlank(oTemp)
			vCode .= JEE_ArrayToFunc(oTemp, "SS")
		}

		;COMMAND - RegWrite
		;[4] v1o       ValueType KeyName ValueName Value
		;[5] v1n       ValueType RK SK   ValueName Value
		;[1] v1L Value
		;[4] v2  Value ValueType KeyName ValueName
		if (oTemp.1 = "RegWrite")
		{
			vIsReady := 0
			if (oTemp.Length() = 2)
				vIsReady := 1
			if !vIsReady && (oTemp.Length() = 6)
				if (oTemp.4 = "")
					oTemp.RemoveAt(4), vIsReady := 1
				else
					oTemp.3 := "% " JEE_CvtJoin("SSS", oTemp.3, "\", oTemp.RemoveAt(4)), vIsReady := 1
			if !vIsReady && (oTemp.Length() = 5)
			&& InStr(oTemp.3, "\")
				vIsReady := 1
			if !vIsReady && (oTemp.Length() = 5)
			&& !RegExMatch(oTemp.3, "[\%]")
				oTemp.3 := "% " JEE_CvtJoin("SSS", oTemp.3, "\", oTemp.RemoveAt(4)), vIsReady := 1
			if !vIsReady
				continue
			if (!oTemp.HasKey(5) || (oTemp.5 = "")) && (JEE_Cvt(oTemp.2) ~= "\x22(REG_SZ|REG_EXPAND_SZ|REG_MULTI_SZ|REG_BINARY)\x22")
				oTemp.5 := "% """""
			else if (!oTemp.HasKey(5) || (oTemp.5 = "")) && (JEE_Cvt(oTemp.2) = Chr(34) "REG_DWORD" Chr(34))
				oTemp.5 := 0
			else if (!oTemp.HasKey(5) || (oTemp.5 = ""))
				continue
			vValue := oTemp.RemoveAt(5), oTemp.InsertAt(2, vValue)
			JEE_ObjPopBlank(oTemp)
			vCode := JEE_ArrayToFunc(oTemp, "SSSS")
		}

		;COMMAND - SetEnv
		if (oTemp.1 = "SetEnv")
		{
			vCode := oTemp.2 " := " JEE_Cvt(oTemp.3)
		}

		;COMMAND - Sort
		if (oTemp.1 = "Sort")
		&& (oTemp.Length() = 3)
			vCode := oTemp.2 " := " vCmdX "(" oTemp.2 ", " JEE_Cvt(oTemp.3) ")"
		if (oTemp.1 = "Sort")
		&& (oTemp.Length() = 2)
			vCode := oTemp.2 " := " vCmdX "(" oTemp.2 ")"

		;COMMAND - SoundGetWaveVolume|SoundSetWaveVolume
		;SoundGetWaveVolume, OutputVar [, DeviceNumber]
		;SoundGet, OutputVar, Wave, Volume [, DeviceNumber]
		;SoundSetWaveVolume, Percent [, DeviceNumber]
		;SoundSet, NewSetting, Wave, Volume [, DeviceNumber]
		if (oTemp.1 = "SoundGetWaveVolume")
		{
			vTemp := oTemp.RemoveAt(2)
			oTemp.1 := "SoundGet"
			oTemp.InsertAt(2, "Wave", "Volume")
			JEE_ObjPopBlank(oTemp)
			vCode := Trim(vTemp) " := " JEE_ArrayToFunc(oTemp, "SSE")
		}
		if (oTemp.1 = "SoundSetWaveVolume")
		{
			oTemp.1 := "SoundSet"
			oTemp.InsertAt(3, "Wave", "Volume")
			JEE_ObjPopBlank(oTemp)
			vCode := JEE_ArrayToFunc(oTemp, "ESSE")
		}

		;COMMAND - SplashImage
		if (oTemp.1 = "SplashImage")
		&& vDoJeeSplashImage
		{
			oTemp.1 := "JEE_SplashImage" ;[NOT IMPLEMENTED]
			vCode := JEE_ArrayToFunc(oTemp, "SSSSSS")
		}

		;COMMAND - SplashImage
		if (oTemp.1 = "SplashImage")
		&& vDoJeeSplashImage
		{
			oTemp.1 := "JEE_SplashImage" ;[NOT IMPLEMENTED]
			vCode := JEE_ArrayToFunc(oTemp, "SSSSSS")
		}

		;COMMAND - SplashTextOff
		if (oTemp.1 = "SplashTextOff")
		&& vDoJeeSplashText
		{
		}

		;COMMAND - SplashTextOn
		if (oTemp.1 = "SplashTextOn")
		&& vDoJeeSplashText
		{
		}

		;COMMAND - StringGetPos
		;StringGetPos, OutputVar, InputVar, SearchText [, L#|R#, Offset]
		if (oTemp.1 = "StringGetPos")
		{
			(oTemp.5 = "1") && (oTemp.5 := "R1")
			if !(oTemp.5 = "") & !(oTemp.5 ~= "^[LR]\d+")
				continue
			vIsR := InStr(oTemp.5, "R")
			vOcc := SubStr(oTemp.5, 2)
			oTemp.5 := RegExReplace(oTemp.5, "[LR]")
			if vIsR && (oTemp.6 = "")
				oTemp.6 := 0
			if vIsR && !(oTemp.6 = "")
				oTemp.6 := "% -1-" JEE_Cvt(oTemp.6, "E")
			else if oTemp.6
				oTemp.6 := "% 1+" JEE_Cvt(oTemp.6, "E")
			oTemp2 := ["InStr", oTemp.3, oTemp.4, "", oTemp.6, oTemp.5]
			JEE_ObjPopBlank(oTemp2)
			vCode := oTemp.2 " := " JEE_ArrayToFunc(oTemp2, "OSSS")
		}

		;COMMAND - StringLeft|StringRight
		if (oTemp.1 = "StringLeft")
		{
			vCode := oTemp.2 " := SubStr(" oTemp.3 ", 1, " JEE_Cvt(oTemp.4, "E") ")"
		}
		if (oTemp.1 = "StringRight") && vDoJeeStringRight
		{
			vCode := oTemp.2 " := JEE_SubStr(" oTemp.3 ", -" JEE_Cvt(oTemp.4, "E") ")"
		}

		;COMMAND - StringLower|StringUpper
		if ((oTemp.1 = "StringLower") && vDoStringLower)
		|| ((oTemp.1 = "StringUpper") && vDoStringUpper)
		{
			if (Trim(oTemp.4) = "T")
				vLetter := "T"
			else if (oTemp.4 = "")
				vLetter := SubStr(oTemp.1, 7, 1)
			else
				continue
			vCode := oTemp.2 " := Format(""{:" vLetter "}"", " JEE_Cvt(oTemp.3, "I") ")"
		}
		if ((oTemp.1 = "StringLower") && !vDoStringLower)
		|| ((oTemp.1 = "StringUpper") && !vDoStringUpper)
		{
			oTemp.1 := oXtra[oTemp.1].2
			if !(oTemp.4 = "")
				vCode := oTemp.2 " := " oTemp.1 "(" JEE_Cvt(oTemp.3, "I") ", " JEE_Cvt(oTemp.4) ")"
			else
				vCode := oTemp.2 " := " oTemp.1 "(" JEE_Cvt(oTemp.3, "I") ")"
		}

		;COMMAND - StringMid
		;StringMid, OutputVar, InputVar, StartChar [, Count, L]
		if (oTemp.1 = "StringMid")
		{
			if (oTemp.Length() >= 6)
				continue
			oTemp2 := ["SubStr", oTemp.3, "% 1+" JEE_Cvt(oTemp.4, "E"), oTemp.5]
			JEE_ObjPopBlank(oTemp2)
			vCode := oTemp.2 " := " JEE_ArrayToFunc(oTemp2, "OSEE")
		}

		;COMMAND - StringReplace
		if (oTemp.1 = "StringReplace")
		{
			if RegExMatch(vCode, vRx := "^StringReplace, (" vVar "), (" vVar "), ([A-Za-z_]+), ([A-Za-z_]+),, All$")
				vCode := RegExReplace(vCode, vRx, "$1 := StrReplace($2, " Chr(34) "$3" Chr(34) ", " Chr(34) "$4" Chr(34) ")")
			else if RegExMatch(vCode, vRx := "^StringReplace, (" vVar "), (" vVar "), ([^%``""]+),, All$")
				vCode := RegExReplace(vCode, vRx, "$1 := StrReplace($2, " Chr(34) "$3" Chr(34) ")")
			else if RegExMatch(vCode, vRx := "^StringReplace, (" vVar "), (" vVar "), ([^%``""]+), ([^%``""]+), All$")
				vCode := RegExReplace(vCode, vRx, "$1 := StrReplace($2, " Chr(34) "$3" Chr(34) ", " Chr(34) "$4" Chr(34) ")")
			else if RegExMatch(vCode, vRx := "^StringReplace, (" vVar "), (" vVar "), ([^%""]+), ([^%""]+), All$")
			&& !InStr(vCode, "```,") && !InStr(vCode, "```;")
				vCode := RegExReplace(vCode, vRx, "$1 := StrReplace($2, " Chr(34) "$3" Chr(34) ", " Chr(34) "$4" Chr(34) ")")
			else if RegExMatch(vCode, vRx := "^StringReplace, (" vVar "), (" vVar "), ([^%""]+),, All$")
			&& !InStr(vCode, "```,") && !InStr(vCode, "```;")
				vCode := RegExReplace(vCode, vRx, "$1 := StrReplace($2, " Chr(34) "$3" Chr(34) ")")

			else if RegExMatch(vCode, "^StringReplace, ")
			&& !InStr(vCode, "UseErrorLevel")
			{
				if (oTemp.Length() = 4)
					oTemp.Push("")
				if (oTemp.Length() = 5)
					oTemp.Push(0)
				if !(oTemp.Length() = 6)
					continue
				oTemp.6 := Trim(oTemp.6)
				if !(oTemp.6 ~= "^(All|A|1|0)$")
					continue
				oTemp.6 := (oTemp.6 = 0) ? 1 : ""

				oTemp.InsertAt(6, "")
				oTemp.1 := "StrReplace"
				vTemp := Trim(oTemp.RemoveAt(2))
				JEE_ObjPopBlank(oTemp)
				vCode := vTemp " := " JEE_ArrayToFunc(oTemp, "ISSOS")
			}
		}

		;COMMAND - StringSplit
		;StringSplit, OutputArray, InputVar, Delimiters, OmitChars
		if (oTemp.1 = "StringSplit") && vDoStringSplit
		{
			if (oTemp.Length() = 3)
				vCode := "Loop, Parse, " oTemp.3
			else if (oTemp.Length() = 4)
				vCode := "Loop, Parse, " oTemp.3 ", % " JEE_Cvt(oTemp.4)
			else if (oTemp.Length() = 5)
				vCode := "Loop, Parse, " oTemp.3 ", % " JEE_Cvt(oTemp.4) ", % " JEE_Cvt(oTemp.5)
			else
				continue
			if (SubStr(oTemp.2, 1, 2) = "% ")
				oTemp.2 := "%" SubStr(oTemp.2, 3) "%"
			vCode .= " `;string split`r`n" vWhitespace vOptIndent oTemp.2 "%A_Index% := A_LoopField, " oTemp.2 "0 := A_Index"
		}

		;COMMAND - StringTrimLeft|StringTrimRight
		if (oTemp.1 = "StringTrimLeft")
		{
			oTemp.4 := JEE_Cvt(oTemp.4, "E")
			if (oTemp.4 ~= "^\d+")
				oTemp.4++
			else
				oTemp.4 .= "+1"
			vCode := oTemp.2 " := SubStr(" oTemp.3 ", " oTemp.4 ")"
		}
		if (oTemp.1 = "StringTrimRight")
		{
			vCode := oTemp.2 " := SubStr(" oTemp.3 ", 1, " ("-"JEE_Cvt(oTemp.4, "E")) ")"
		}

		;COMMAND - SysGet
		if (oTemp.1 = "SysGet")
		{
			vVar := oTemp.2
			vFunc := oTemp.3
			vNum := oTemp.4
			vPfx := ""
			if (vFunc = "Monitor")
				oTemp := ["MonitorGet", vNum, vVar "Left", vVar "Top", vVar "Right", vVar "Bottom"]
			else if (vFunc = "MonitorWorkArea")
				oTemp := ["MonitorGetWorkArea", vNum, vVar "Left", vVar "Top", vVar "Right", vVar "Bottom"]
			else if (vFunc = "MonitorCount")
				vPfx := vVar " := ", oTemp := ["MonitorGetCount"]
			else if (vFunc = "MonitorPrimary")
				vPfx := vVar " := ", oTemp := ["MonitorGetPrimary"]
			else if (vFunc = "MonitorName")
				vPfx := vVar " := ", oTemp := ["MonitorGetName", vNum]
			else
				vPfx := vVar " := ", oTemp := ["SysGet", vFunc]
			JEE_ObjPopBlank(oTemp)
			vCode := vPfx JEE_ArrayToFunc(oTemp, "SOOOO")
		}

		;COMMAND - Transform
		;Transform, OutputVar, Cmd, Value1 [, Value2]
		if (oTemp.1 = "Transform")
		{
			;not available (5):
			;Unicode|HTML|Deref|FromCodePage|ToCodePage

			;available (24):
			;Asc|Chr
			;Mod|Pow|Exp|Sqrt|Log|Ln
			;Round|Ceil|Floor|Abs
			;Sin|Cos|Tan|ASin|ACos|ATan
			;BitNot|BitAnd|BitOr|BitXOr|BitShiftLeft|BitShiftRight

			;note:
			;Asc (Ord)
			;Pow (**)
			;BitNot (~)/BitAnd (&)
			;BitOr (|)/BitXOr (^)
			;BitShiftLeft (<<)/BitShiftRight (>>)

			if (oTemp.3 ~= "^(Unicode|HTML|Deref|FromCodePage|ToCodePage)$")
				continue
			(oTemp.3 = "Asc") && (oTemp.3 := "Ord")
			if !(oTemp.3 = "Pow") && !(oTemp.3 ~= "^Bit")
			{
				oTemp2 := [oTemp.3, oTemp.4, oTemp.5]
				JEE_ObjPopBlank(oTemp2)
				vCode := oTemp.2 " := " JEE_ArrayToFunc(oTemp2, "EE")
			}
			else
			{
				vOp := {Pow:"**",BitNot:"~",BitAnd:"&",BitOr:"|",BitXOr:"^",BitShiftLeft:"<<",BitShiftRight:">>"}[oTemp.3]
				vCode := oTemp.2 " := " JEE_Cvt(oTemp.4, "E") " " vOp " " JEE_Cvt(oTemp.5, "E")
			}
		}

		;COMMAND - TrayTip
		if (oTemp.1 = "TrayTip")
		{
			if !(oTemp.4 = "")
				oTemp.4 := JEE_CvtJoin("SEE", "S", oTemp.4, oTemp.5)
			else
				oTemp.4 := JEE_Cvt(oTemp.5, "E")
			oTemp.5 := ""
			oTemp := JEE_ObjShuffleFrom(oTemp, 1324)
			JEE_ObjPopBlank(oTemp)
			vCode := JEE_ArrayToFunc(oTemp, "SSS")
		}

		;COMMAND - WinGetActiveStats
		if (oTemp.1 = "WinGetActiveStats")
		{
			vCode := oTemp.2 " := WinGetTitle(""A"")"
			oTemp := ["WinGetPos", oTemp.5, oTemp.6, oTemp.3, oTemp.4, "A"]
			vCode .= ", " JEE_ArrayToFunc(oTemp, "OOOO")
		}

		;COMMAND - WinGetActiveTitle
		if (oTemp.1 = "WinGetActiveTitle")
		{
			vCode := oTemp.2 " := WinGetTitle(""A"")"
		}

		;COMMAND - WinMove
		if (oTemp.1 = "WinMove")
		{
			if (oTemp.Length() > 3)
				oTemp := JEE_ObjShuffleFrom(oTemp, 145672389)
			JEE_ObjPopBlank(oTemp)
			vCode := JEE_ArrayToFunc(oTemp, "EEEESSSS")
		}

		;COMMAND - WinSetTitle
		if (oTemp.1 = "WinSetTitle")
		{
			if (oTemp.Length() > 2)
				oTemp := JEE_ObjShuffleFrom(oTemp, 142356)
			JEE_ObjPopBlank(oTemp)
			vCode := JEE_ArrayToFunc(oTemp, "SSSSS")
		}

		;OTHER COMMANDS, NOT NOT FULLY HANDLED:
		;COMMAND - AutoTrim (typically handled by vListCommentOut)
		;COMMAND - Gui|GuiControl|GuiControlGet
		;COMMAND - IfMsgBox
		;COMMAND - OnExit
		;COMMAND - SetBatchLines (typically handled by vListCommentOut)
		;COMMAND - SetFormat
	}
	;==============================
	;STAGE - COMMANDS - REMOVE COMMAS (FROM COMMAND/CONTROL FLOW STATEMENT/DIRECTIVE NAMES)
	;remove initial commas from commands/control flow statements/directives
	;removed based on settings
	;remove initial commas from commands/control flow statements/directives
	if vOptRemCommaCmd
	&& RegExMatch(vCode, vRx := "O)^(" vListCmd "),", o)
	{
		vCode := oName[o.1] " " LTrim(SubStr(vCode, StrLen(o.1)+2))
	}
	else if vOptRemCommaLoop
	&& RegExMatch(vCode, vRx := "^Loop,")
	{
		vCode := "Loop " LTrim(SubStr(vCode, StrLen(o.1)+2))
	}
	else if	vOptRemCommaCFS
	&& !(vCode ~= "^Loop")
	&& RegExMatch(vCode, vRx := "iO)^(" vListCFS "),", o)
	{
		vCode := oName[o.1] " " LTrim(SubStr(vCode, StrLen(o.1)+2))
	}
	if vOptRemCommaDrv
	&& RegExMatch(vCode, vRx := "iO)^(" vListDrv "),", o)
	{
		vCode := oName[o.1] " " LTrim(SubStr(vCode, StrLen(o.1)+2))
	}
	;==============================
	;STAGE - FINAL
	if !(vCode == vCodeOrig)
		oArrayNew[A_Index] := vWhitespace vCode vComments
	if (!vOptLogOmitCaseChange && !(vCode == vCodeOrig))
	|| (vOptLogOmitCaseChange && !(vCode = vCodeOrig))
	{
		if !oChange.HasKey("z" vCodeOrig)
		{
			oChange["z" vCodeOrig] := ""
			vCodeNext := oArrayNew[A_Index+1]
			vCodeNext := RegExReplace(vCodeNext, "^[ `t]*|[ `t]+;.*")
			;if the line has changed,
			;(and it wasn't a line that marked the assignment of a continuation section,)
			;add it to the log of changed lines
			if !(SubStr(vCodeNext, 1, 1) = "(") && !InStr(vCodeNext, ")")
				vListChange .= "[1]" vCodeOrig "`r`n[2]" vCode "`r`n"
		}
	}
}

Loop, % oArrayNew.Length()
	vOutput .= (A_Index=1?"":"`r`n") oArrayNew[A_Index]
if (vTextOrig == vOutput)
	MsgBox, % "same"
else if !vIsCdLn
{
	Clipboard := vOutput
	SendInput, ^v
}
;JEE_WinMergeCompareStrings("BEFORE`r`n" vTextOrig, "AFTER`r`n" vOutput)
if (vOptLog && !(vTextOrig == vOutput))
|| (vIsCdLn && !(vPathOutLog = ""))
{
	if vIsCdLn
	&& !(vPathOutLog = "")
	{
		vPathLog := vPathOutLog
		SplitPath, vPathLog,, vDirLog
	}
	else
		vPathLog := vDirLog "\z ahk convert " A_Now ".txt"
	if !FileExist(vDirLog)
		FileCreateDir, % vDirLog
	vPfx := (vPathLog ~= "^\*{1,2}$") ? "" : "*"
	if FileExist(vPathLog)
		FileAppend, % "`r`n" vListChange, % vPfx vPathLog, UTF-8
	else
		FileAppend, % vListChange, % vPfx vPathLog, UTF-8
	if !vIsCdLn
	&& (JEE_StrCount(vListChange, "`n") >= vOptRunLogLimit)
	&& vOptRunLogAllow
		Run, % vPathLog
}
vPfx := (vPathOut ~= "^\*{1,2}$") ? "" : "*"
if vIsCdLn && !(vPathOut = "")
	FileAppend, % vOutput, % vPfx vPathOut, UTF-8
if vIsCdLn
	ExitApp
return

;==================================================

;MAIN SECTION 5 - HOTKEY 2

;==================================================

SubCheckLines: ;check lines are standard (list nonstandard lines)
vMode := 1 ;only allow AHK v1-style lines
vMode := 2 ;only allow AHK v2-style lines
;vMode := 12 ;allow AHK v1/v2-style lines

if (vMode ~= 1)
	vV1VarValue := "| = "
else
	vV1VarValue := ""

WinGetTitle, vWinTitle, A
vText := JEE_GetSelectedText()
;ControlGet, vText, Selected,, Edit1, A
;vPath := A_ScriptDir "\AutoHotkey.ahk"
;FileRead, vText, % vPath

vTextOrig := vText
vOutput := ""
VarSetCapacity(vOutput, StrLen(vText)*2)
vText := StrReplace(vText, "`r`n", "`n")
oArrayOrig := StrSplit(vText, "`n")
oArrayNew := StrSplit(vText, "`n")
vIsConSec := 0
vLastCodeLine := 0
vConSecPfx := ""
vConSecSfx := ""
vUnused := JEE_StrUnused(1, vText)

Loop, % oArrayNew.Length()
{
	vTemp := oArrayNew[A_Index]
	if (SubStr(vTemp, 1, 1) = ";")
		vTempCode := "", vComments := vTemp
	else if (vPos := RegExMatch(vTemp, "[ `t]+;"))
		vTempCode := SubStr(vTemp, 1, vPos-1), vComments := SubStr(vTemp, vPos)
	else
		vTempCode := vTemp, vComments := ""
	vCode := LTrim(vTempCode)
	vWhitespace := SubStr(vTempCode, 1, StrLen(vTempCode)-StrLen(vCode))
	;==============================
	;HANDLE CONTINUATION SECTIONS
	if (SubStr(vCode, 1, 1) = "(") && !InStr(vCode, ")")
	{
		vIsConSec := 1
		if !vLastCodeLine || !(vLastCodeLine < A_Index)
		{
			MsgBox, % "error: " vLastCodeLine " " A_Index
			return
		}
		Loop, % A_Index - vLastCodeLine
			oArrayNew[vLastCodeLine-1+A_Index] := vConSecPfx oArrayOrig[vLastCodeLine-1+A_Index] vConSecSfx
	}
	if vIsConSec && !(vConSecPfx vConSecSfx = "")
		oArrayNew[A_Index] := vConSecPfx vTemp vConSecSfx
	if (SubStr(vCode, 1, 1) = ")")
		vIsConSec := 0
	if vIsConSec
		continue
	if !(vCode = "")
		vLastCodeLine := A_Index
	;==============================
	vCodeOrig := vCode
	;==============================
	if (vCode ~= "^(" vCmd "),[ ,]")
	{
		vCmdTemp := RegExReplace(vCode, ",.*")
		if (JEE_StrCount(vCode, ",") > StrLen(oParams[vCmdTemp]))
			vOutput .= "[PARAM COUNT]" vCode "`r`n"
	}

	if (vCode = "")
	|| (vCode ~= "^;")
	|| (vCode ~= "^\)")
	|| (vCode = "{")
	|| (vCode = "}")
	|| (vCode ~= "^(&&|\Q||\E)")
	|| (vCode ~= "^JEE_")
	|| (vCode ~= "^Gdip_")
	|| (vCode ~= "^Acc_")
	|| (vCode ~= "^(Gosub|Goto|Loop), ")
	|| (vCode ~= "^(" vListCFS ") ")
	|| ((vCode ~= "^(" vListCmd "),[ ,]") && (vMode ~= 1))
	|| ((vCode ~= "^(" vListDrv "),") && (vMode ~= 1))
	|| (vCode ~= "^(" vListDrv ") ")
	|| (vCode ~= "^(" vListFnc ")\(")
	|| (vCode ~= "^(else if ), ")
	|| (vCode ~= "^(global|static|local) ")
	|| (vCode ~= "^(global)$")
	|| (vCode ~= "^(#NoTrayIcon|#UseHook)$")
	|| (vCode ~= "^(break|continue|else|Loop|return)$")
	|| ((vMode ~= 1) && (vCode ~= "^(#IfWinActive|#NoEnv|" vListCmd1NP ")$"))
	|| (vCode ~= "::(Suspend)?$")
	|| (vCode ~= ":$")
	|| (vCode ~= "^(hCtl|hWnd|hFont|hIcon|hMenu|hSubMenu|hProc|hBuf|hDrop|hBitmap|hBrush|hDC|hFile|hData|hItem|hItemNext|_?[ov][A-Z]|Clipboard|pToken|pBitmap|pBuf|pDrop|pBrush|pData|pWndProc|pGraphics|ErrorLevel|ClipSaved|lParam|wParam|uMsg|IID_)[\w%[\]]*( := | .= " vV1VarValue "|\Q++\E|--)")
	|| (vCode ~= "^(oWB|oElt|oAcc|oYTPlayer|oWin|oDoc|oArray|oImg|oFile|oHTTP|oHTML|oTemp|oADODB|oChild|oXl|oWd|oOutput|oTrayInfo|oFontInfo)\w*[\.[]")
	|| (vCode ~= "^%v\w+%(|%v\w+%|%A_\w+%|0) (:=|.=) ")
	|| (vCode ~= "^. (\x22|v)")
		continue
	if (vMode ~= 2) && (vCode ~= "^(" vListFnc2 ")\(")
		continue
	;ignore more variables/functions
	if (vCode ~= "^\w+ := ")
	|| (vCode ~= "^\w+\(")
	|| (vCode ~= "^\w+\.\w+ := ")
		continue
	vOutput .= vCode "`r`n"
	;==============================
}

if (vOutput = "")
	MsgBox, % "same"
else
{
	Clipboard := vWinTitle "`r`n" vOutput
	MsgBox, % vOutput
}
;JEE_WinMergeCompareStrings("BEFORE`r`n" vTextOrig, "AFTER`r`n" vOutput)
return

;==================================================
