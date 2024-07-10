;==================================================

;AHK v2 functions for AHK v1
;auxiliary functions expansion pack
;these functions are AHK v1/v2 two-way compatible
;[first released: 2018-02-21]

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

;==================================================

;if vNum between %vLim1% and %vLim2%
JEE_Between(vNum, vLim1, vLim2, vOpt="ii")
{
	if (vOpt = "ii")
		return (vLim1 <= vNum && vNum <= vLim2)
	if (vOpt = "xx")
		return (vLim1 < vNum && vNum < vLim2)
	if (vOpt = "xi")
		return (vLim1 < vNum && vNum <= vLim2)
	if (vOpt = "ix")
		return (vLim1 <= vNum && vNum < vLim2)
}

;==================================================

;set clipboard contents based on a clp file
JEE_ClipboardFromFile(vPath)
{
	static vFunc := "ClipboardAll", vFunc2 := "FileRead"
	if !(SubStr(A_AhkVersion, 1, 2) = "1.")
		Clipboard := %vFunc%(%vFunc2%(vPath, "RAW"))
	else
	{
		if !oFile := FileOpen(vPath, "r")
			return
		hWnd := A_ScriptHwnd ? A_ScriptHwnd : WinExist("ahk_pid " DllCall("kernel32\GetCurrentProcessId", UInt))
		DllCall("user32\OpenClipboard", Ptr,hWnd)
		DllCall("user32\EmptyClipboard")
		oFile.Pos := 0
		while (vFormat := oFile.ReadUIntType())
		{
			;GMEM_ZEROINIT := 0x40, GMEM_MOVEABLE := 0x2
			vSize := oFile.ReadUIntType()
			hData := DllCall("kernel32\GlobalAlloc", UInt,0x42, UPtr,vSize, Ptr)
			pData := DllCall("kernel32\GlobalLock", Ptr,hData, Ptr)
			oFile.RawRead(pData+0, vSize)
			DllCall("user32\SetClipboardData", UInt,vFormat, Ptr,hData, Ptr)
			DllCall("kernel32\GlobalUnlock", Ptr,hData)
		}
		DllCall("user32\CloseClipboard")
		oFile.Close()
	}
}

;==================================================

;save current clipboard contents to a clp file
JEE_ClipboardToFile(vPath)
{
	static vFunc := "ClipboardAll"
	if !oFile := FileOpen(vPath, "w") ;empties file
		return
	if !(SubStr(A_AhkVersion, 1, 2) = "1.")
		oFile.RawWrite(%vFunc%().Data)
	else
	{
		ClipSaved := ClipboardAll
		vSize := StrLen(ClipSaved) << !!A_IsUnicode
		oFile.RawWrite(&ClipSaved, vSize) ;appends data, advances pointer
	}
	oFile.Close()
}

;==================================================

;conversion logic, v1 = -> v1 := -> v2, two-way compatibility - Page 3 - AutoHotkey Community
;https://autohotkey.com/boards/viewtopic.php?f=37&t=27069&p=131336#p131336
;One of my favorite error codes: Optional parameter missing – The Old New Thing
;https://blogs.msdn.microsoft.com/oldnewthing/20140129-00/?p=1933/

JEE_ComObjMissing()
{
	;VT_ERROR := 0xA ;DISP_E_PARAMNOTFOUND := 0x80020004
	return ComObject(0xA, 0x80020004)
}

;==================================================

JEE_FileReadBin(ByRef vData, vPath)
{
	oFile := FileOpen(vPath, "r")
	oFile.Pos := 0
	oFile.RawRead(vData, oFile.Length)
	oFile.Close()
}

;==================================================

JEE_FileWriteBin(ByRef vData, vSize, vPath)
{
	if !oFile := FileOpen(vPath, "w") ;empties file
		return
	oFile.RawWrite(&vData, vSize) ;appends data, advances pointer
	oFile.Close()
}

;==================================================

;works like InStr (AHK v2) (on AHK v1/v2)
JEE_InStr(ByRef vText, vNeedle, vCaseSen:=0, vPos:=1, vOcc:=1)
{
	static vIsV1 := !!InStr(1,1,1,0)
	if (vPos = 0)
		return
	if vIsV1 && (vPos <= -1)
		vPos++
	return InStr(vText, vNeedle, vCaseSen, vPos, vOcc)
}

;==================================================

;string contains one of comma-separated list
;unlike AHK v1: no special handling for ',,'
JEE_MC(ByRef vText, ByRef vNeedles)
{
	;Loop is not two-way compatible at present
	;Loop, Parse, vNeedles, % ","
	;	if InStr(vText, A_LoopField)
	;		return A_Index
	for vKey, vValue in StrSplit(vNeedles, ",")
		if InStr(vText, vValue)
			return vKey
	return 0
}

;==================================================

;exact match, comma-separated list
JEE_MX(ByRef vText, ByRef vNeedles)
{
	;Loop is not two-way compatible at present
	;Loop, Parse, vNeedles, % ","
	;	if !("" vText != A_LoopField)
	;		return A_Index
	for vKey, vValue in StrSplit(vNeedles, ",")
		if !("" vText != vValue)
			return vKey
	return 0
}

;==================================================

;works like RegExMatch (AHK v2) (on AHK v1/v2)
JEE_RegExMatch(ByRef vText, vNeedle, ByRef oArray:="", vPos:=1)
{
	;we're not interested in the return value, but we need it to get RegExMatch to take place
	static vRet := RegExMatch("","",o), vIsV1 := !IsObject(o)
	if !vIsV1
		return RegExMatch(vText, vNeedle, oArray, vPos)
	if (vPos = 0)
		return
	if vIsV1 && (vPos <= -1)
		vPos++
	if RegExMatch(vNeedle, "^[A-Za-z`a`n`r `t]*\)")
		vNeedle := "O" vNeedle
	else
		vNeedle := "O)" vNeedle
	return RegExMatch(vText, vNeedle, oArray, vPos)
}

;==================================================

;works like RegExReplace (AHK v2) (on AHK v1/v2)
JEE_RegExReplace(ByRef vText, vNeedle, vReplaceText, ByRef vCount, vLimit:=-1, vPos:=1)
{
	static vIsV1 := !RegExReplace(10, 1,,,, -1)
	if (vPos = 0)
		return
	if vIsV1 && (vPos <= -1)
		vPos++
	return RegExReplace(vText, vNeedle, vReplaceText, vCount, vLimit, vPos)
}

;==================================================

;If Var is [not] integer|float|number|digit|xdigit|alpha|upper|lower|alnum|space|time
;e.g. if JEE_StrIsType(vText, "digit")
JEE_StrIsType(vText, vType)
{
	%vType% := vType ;for AHK v2
	;if JEE_StrIsType(vText, vType) ;[appearance of line below if converted, warning: this would cause an infinite loop]
	if vText is %vType% ;[DO NOT CONVERT]
		return 1
	else
		return 0
}

;==================================================

;works like SubStr (AHK v2) (on AHK v1/v2)
JEE_SubStr(ByRef vText, vPos, vLen:="")
{
	static vIsV1 := !!SubStr(1,0)
	if (vPos = 0)
		return
	if vIsV1 && (vPos <= -1)
		vPos++
	if (vLen = "")
		return SubStr(vText, vPos)
	return SubStr(vText, vPos, vLen)
}

;==================================================
