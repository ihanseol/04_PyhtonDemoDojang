import tkinter as tk

# 메인 윈도우 생성
root = tk.Tk()
root.title("MainWindow - FireShotRenamerUI")
root.geometry("400x200")
root.resizable(False, False)

# "Enter the Starting Number" 라벨
label = tk.Label(root, text="Enter the Starting Number", font=("Arial", 10))
label.place(x=20, y=20)

# 입력 필드
entry = tk.Entry(root, width=50)
entry.place(x=20, y=50)

# 체크박스
remove_header_var = tk.BooleanVar()


def handle_checkbox():
    if remove_header_var.get():
        print("Checkbox selected: Perform some action!")
    else:
        print("Checkbox deselected.")


checkbox = tk.Checkbutton(
    root, text="Remove Header", variable=remove_header_var, command=handle_checkbox, font=("Arial", 10)
)
checkbox.place(x=20, y=90)


# 버튼
def on_button_click():
    print("Button clicked!")
    if remove_header_var.get():
        print("Remove Header option is selected, performing action...")


button = tk.Button(root, text="Change File Name", width=15, height=1, command=on_button_click)
button.place(x=200, y=140)

# 메인 루프 실행
root.mainloop()
