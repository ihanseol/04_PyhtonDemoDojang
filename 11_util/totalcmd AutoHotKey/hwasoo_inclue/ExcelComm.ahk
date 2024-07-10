; ExcelCOM class - 2019-11-14
; Credits to FanaticGuru, Kon and Lexikos for most parts of the code
; Class put together by D Rocks
;
; FanaticGuru 	- https://www.autohotkey.com/boards/viewtopic.php?p=272861#p272861
; Kon 			- https://www.autohotkey.com/boards/viewtopic.php?p=116315#p116315
; Lexikos		- http://ahkscript.org/boards/viewtopic.php?f=6&t=6494
;
; Tested on Win10 64bits with Latest Excel and AHK versions as of creation date
;
;;Example : (uncomment to test)
;xlPath := myFolderReference . "\MyExcelFile.xlsx" ; <--- Excel workbook (file) path
;
;xlWB := ExcelCOM.GetWorkbook(xlPath, false)				; Get Workbook com object
;xlApp := xlWB.Application									; Assign Application com object from workbook ref.
;xlSheet := xlApp.Workbooks(xlFile . ".xlsm").ActiveSheet 	; Assign Sheet com object from the Application object ref
;
;xlSheet.Range("A1").Value = "Test"
;MsgBox % xlSheet.Range("A1").Value
;--------------------------------------------------------------------------------
class ExcelCOM {
;--------------------------------------------------------------------------------

	GetApp() {
		Try {
			xlApp := ComObjActive("Excel.Application")
		}
		Catch {
			Try {
				xlApp := ComObjCreate("Excel.Application")
			}
			Catch {
				return
			}
		}
		return xlApp
	}

	GetWorkbook(FullPath, isWindowVisible := true, Sheet := "ActiveSheet") {
		SplitPath, FullPath, FileName, Folder
		ComObjectsList := ExcelCOM.GetActiveObjects()
		;for name, obj in ComObjectsList
			;list .= name " -- " ComObjType(obj, "Name") "`n"
		;MsgBox %list%
		for name, obj in ComObjectsList
		{
			if (ComObjType(obj, "Name") = "_Workbook")	; If this object is a workbook...
			{
				if (obj.Path = Folder && obj.Name = FileName)	; If this workbook's path and name match...
				{
					xlWB := obj	; Save a reference to this workbook
					;MsgBox, % obj.Path "`n" obj.Name	; Show the name and path of this workbook
					xlApp := xlWB.Application
					break	; Break the for-loop
				}
			}
		}
		if (!IsObject(xlWB)) {
			Try {
				xlApp := ExcelCOM.GetApp()
				xlWB := xlApp.Workbooks.Open(FullPath)
				xlWB.Activate
				if (Sheet != "ActiveSheet") {
					try
						xlWB.Sheets(Sheet).Activate
				}
			}
			Catch {
				return ; if previous Try failed method returns Empty
			}
		}
		if (!xlApp.Visible && isWindowVisible) {
			xlApp.Visible := isWindowVisible
		}
		return xlWB ; excel WorkBook object returned
	}

	GetActiveObjects(Prefix := "", CaseSensitive := false) {
	; GetActiveObjects v1.0 by Lexikos
	; http://ahkscript.org/boards/viewtopic.php?f=6&t=6494
		objects := {}
		DllCall("ole32\CoGetMalloc", "uint", 1, "ptr*", malloc) ; malloc: IMalloc
		DllCall("ole32\CreateBindCtx", "uint", 0, "ptr*", bindCtx) ; bindCtx: IBindCtx
		DllCall(NumGet(NumGet(bindCtx+0)+8*A_PtrSize), "ptr", bindCtx, "ptr*", rot) ; rot: IRunningObjectTable
		DllCall(NumGet(NumGet(rot+0)+9*A_PtrSize), "ptr", rot, "ptr*", enum) ; enum: IEnumMoniker
		while DllCall(NumGet(NumGet(enum+0)+3*A_PtrSize), "ptr", enum, "uint", 1, "ptr*", mon, "ptr", 0) = 0 ; mon: IMoniker
		{
			DllCall(NumGet(NumGet(mon+0)+20*A_PtrSize), "ptr", mon, "ptr", bindCtx, "ptr", 0, "ptr*", pname) ; GetDisplayName
			name := StrGet(pname, "UTF-16")
			DllCall(NumGet(NumGet(malloc+0)+5*A_PtrSize), "ptr", malloc, "ptr", pname) ; Free
			if InStr(name, Prefix, CaseSensitive) = 1 {
				DllCall(NumGet(NumGet(rot+0)+6*A_PtrSize), "ptr", rot, "ptr", mon, "ptr*", punk) ; GetObject
				; Wrap the pointer as IDispatch if available, otherwise as IUnknown.
				if (pdsp := ComObjQuery(punk, "{00020400-0000-0000-C000-000000000046}"))
					obj := ComObject(9, pdsp, 1), ObjRelease(punk)
				else
					obj := ComObject(13, punk, 1)
				; Store it in the return array by suffix.
				objects[SubStr(name, StrLen(Prefix) + 1)] := obj
			}
			ObjRelease(mon)
		}
		ObjRelease(enum)
		ObjRelease(rot)
		ObjRelease(bindCtx)
		ObjRelease(malloc)
		return objects
	}
}