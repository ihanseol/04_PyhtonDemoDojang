# c:\Users\minhwasoo\AppData\Local\Programs\Python\Python311\Lib\site-packages\
# c:\Users\minhwasoo\AppData\Local\Programs\Python\Python311\Lib\site-packages\win32\lib\pywintypes.py

# combrowse.py has RunningObjectTable ...

# C:\Users\minhwasoo\AppData\Local\Programs\Python\Python311\Lib\site-packages\win32com\test
# C:\Users\minhwasoo\AppData\Local\Programs\Python\Python311\Lib\site-packages\win32com\client
# C:\Users\minhwasoo\AppData\Local\Programs\Python\Python311\Lib\site-packages\hwpapi


import pythoncom
import win32com.client
import win32com.test.util
import winerror


def testit():
    ctx = pythoncom.CreateBindCtx()
    rot = pythoncom.GetRunningObjectTable()
    num = 0
    for mk in rot:
        name = mk.GetDisplayName(ctx, None)
        num += 1
        print(name)
        # Monikers themselves can iterate their contents (sometimes :)
        try:
            for sub in mk:
                num += 1
        except pythoncom.com_error as exc:
            if exc.hresult != winerror.E_NOTIMPL:
                raise


def get_excel_instances():
    '''
    Returns a list of the running Microsoft Excel application
    instances as component object model (COM) objects.
    '''
    running_object_table_com_interface = get_running_object_table_com_interface()
    bind_context_com_interface = create_bind_context_com_interface()
    excel_application_class_clsid = '{00024500-0000-0000-C000-000000000046}'
    excel_application_clsid = '{000208D5-0000-0000-C000-000000000046}'

    excel_instance_com_objects = []

    for moniker_com_interface in running_object_table_com_interface:
        display_name = moniker_com_interface.GetDisplayName(bind_context_com_interface, None)
        if excel_application_class_clsid not in display_name:
            continue
        unknown_com_interface = running_object_table_com_interface.GetObject(moniker_com_interface)
        dispatch_com_interface = unknown_com_interface.QueryInterface(dispatch_com_interface_iid)
        dispatch_clsid = str(object=dispatch_com_interface.GetTypeInfo().GetTypeAttr().iid)
        if dispatch_clsid != excel_application_clsid:
            continue
        excel_instance_com_object = dispatch(dispatch=dispatch_com_interface)
        excel_instance_com_objects.append(excel_instance_com_object)
    return excel_instance_com_objects


# excel_instances = get_excel_instances()
# input()


testit()

