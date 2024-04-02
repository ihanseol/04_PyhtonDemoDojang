import pythoncom
import re


def get_hwp_objects():
    context = pythoncom.CreateBindCtx(0)

    # 현재 실행중인 프로세스를 가져옵니다. 
    running_coms = pythoncom.GetRunningObjectTable()
    monikers = running_coms.EnumRunning()

    hwp_objects = []
    for moniker in monikers:
        name = moniker.GetDisplayName(context, moniker);
        # moniker의 DisplayName을 통해 한글을 가져옵니다
        # 한글의 경우 HwpObject.버전으로 각 버전별 실행 이름을 설정합니다. 
        if re.match("!HwpObject", name):
            # 120은 한글 2022의 경우입니다. 
            # 현재 moniker를 통해 ROT에서 한글의 object를 가져옵니다. 
            obje = running_coms.GetObject(moniker)
            # 가져온 object를 Dispatch를 통해 사용할수 있는 객체로 변환시킵니다. 
            hwp_objects.append(obje.QueryInterface(pythoncom.IID_IDispatch))
    return hwp_objects



import pythoncom
import re

def get_name_rot():
    context = pythoncom.CreateBindCtx(0)
    running_coms = pythoncom.GetRunningObjectTable()
    monikers = running_coms.EnumRunning()

    for moniker in monikers:
        name = moniker.GetDisplayName(context, moniker);
        obje = running_coms.GetObject(moniker)
        print(name, obje)




# obj = get_hwp_objects()
get_name_rot()



