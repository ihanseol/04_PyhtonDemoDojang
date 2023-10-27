import win32com.client as win32
import pandas as pd

hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")

hwp.XHwpWindows.Item(0).Visible = True

hwp.Open(r"c:\Users\minhwasoo\Desktop\학과심사_평가집계표_서식.hwp")

df = pd.read_excel(r"C:\Users\minhwasoo\Desktop\학생명단.xlsx")


# df["학과"] == "국어국문학과"
# df[(df["학과"] == "국어국문학과") & (df["전형"] == "석사(Master)")]



# hwp.GetFieldText("수험번호1")
# hwp.PutFieldText("수험번호1", "123400002")

# df["학과"].nunique()
# df["전형"].nunique()
# (df["학과"] + df["전형"]).nunique() #number
# (df["학과"] + df["전형"]).unique()  #array(...)




hwp.HAction.Run("CopyPage")

for _ in (19):
    hwp.HAction.Run("PastePage")

df_ = df.groupby([["학과", "전형"]]).size().reset_index().drop(0, axis=1)


for i in range(len(df_)):
    전형, 학과 = df_.iloc[i]
    print(전형, 학과)
    hwp.PutFieldText(f"지원과정{{{{{i}}}}}", 전형)
    hwp.PutFieldText(f"학과{{{{{i}}}}}", 학과)
    # hwp.PutFieldText(f"지원과정{{{{{i}}}}}\x02학과{{{{{i}}}}}", "\x02".join([전형,학과]))



# df_.iloc[0]["학과"]
# df_.iloc[0]["전형"]
# hwp.PutFieldText(f"지원과정{{{{{i}}}}}", "박사(Doctoral)")


# 전형과 학과 필드에 해당하는 학생들을 추려서
# 표안에 입력해주기


for i in range(len(df_)):
    #전형, 학과 = df_[["전형", "학과"]].iloc[i]
    지원과정 = hwp.GetFieldText(f"지원과정{{{{{i}}}}}")
    학과 = hwp.GetFieldText(f"학과{{{{{i}}}}}")

    data = df_[(df["지원과정"] == 지원과정) & (df["학과"] == 학과)]
    for j in range(1, len(data)+1):
        hwp.PutFieldText(f"수험번호{j}{{{{{i}}}}}", data["수험번호"].iloc[j-1])
        hwp.PutFieldText(f"성명{j}{{{{{i}}}}}", data["성명"].iloc[j-1])


