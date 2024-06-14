import pywin32
import pythoncom
import win32com.client


def getWorkbook(workbookName):
    lenstr = len(workbookName)
    workbook = None
    rot = pythoncom.GetRunningObjectTable()
    rotenum = rot.EnumRunning()

    while True:
        monikers = rotenum.Next()

        if not monikers: break
        ctx = pythoncom.CreateBindCtx(0)

    name = monikers[0].GetDisplayName(ctx, None)

    if name[-lenstr:] == workbookName:
        obj = rot.GetObject(monikers[0])
        workbook = win32com.client.Dispatch(obj.QueryInterface(pythoncom.IID_IDispatch))

        return workbook
