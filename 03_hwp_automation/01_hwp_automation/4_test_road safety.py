

import shutil  # 파일복사용 모듈
import win32com.client as win32  # 한/글 열기 위한 모듈
import pandas as pd  # 그 유명한 판다스. 엑셀파일을 다루기 위함
import numpy as np
import get_field as gf

excel = pd.read_excel(r"C:\Users\minhwasoo\Desktop\data.xlsx")  # 엑셀로 데이터프레임 생성
hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")

hwp.XHwpWindows.Item(0).Visible = True

hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")  # 보안모듈 적용(파일 열고닫을 때 팝업이 안나타남)
hwp.Open(r"C:\Users\minhwasoo\Desktop\data.hwp")  # 수정할 한/글 파일 열기

# field_list = hwp.GetFieldList(1, 0x02)

field_list = [i for i in hwp.GetFieldList(1, 0x02).split("\x02")]
return_field = gf.getindex_n_count(field_list)

page = 0

for field, n in return_field.items():  # 모든 누름틀에 각각,
    data: object = excel[field].iloc[page]
    if type(data) == str:
        write_data = data
    else:
        write_data = " "

    for i in range(n):
        str_field = f'{field}{{{{{i}}}}}'
        hwp.MoveToField(str_field)
        hwp.PutFieldText(str_field, data)

    # PutFieldText(hwp, field, n, write_data)


# print(f'{page + 1}:{excel.id[page]}')




#
# for page in range(len(excel)):
#     for field, n in return_field:  # 모든 누름틀에 각각,
#         data = excel[field].iloc[page]
#         if type(data) == str:
#             write_data = data
#         else:
#             write_data = " "
#         myPutFieldText(field, n, write_data)
#     print(f'{page + 1}:{excel.id[page]}')



hwp.Save()  # 한/글 파일(award_result.hwp)을 저장하고,
hwp.Quit()  # 한/글 종료. (저장하지 않고 종료하는 방법은 7강에서~)

