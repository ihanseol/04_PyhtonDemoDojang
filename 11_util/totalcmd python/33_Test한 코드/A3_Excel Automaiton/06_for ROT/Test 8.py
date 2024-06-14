import win32gui
import pythoncom
import win32com.client


WINDOW_CLASS = 'XLMAIN'
WINDOW_TITLE = 'Excel'
hwindow = win32gui.FindWindow(WINDOW_CLASS,WINDOW_TITLE)


def getWorkbook(workbookName):
    workbook = None

    rot = pythoncom.GetRunningObjectTable()
    rotenum = rot.EnumRunning()

    while True:
        monikers = rotenum.Next()

        if not monikers: break
        ctx = pythoncom.CreateBindCtx(0)
        name = monikers[0].GetDisplayName(ctx, None);

        print(name)
        if workbookName in name:
            obj = rot.GetObject(monikers[0])
            workbook = win32com.client.Dispatch(obj.QueryInterface(pythoncom.IID_IDispatch))
            return workbook
        else:
            return False


print(getWorkbook("Excel"))


