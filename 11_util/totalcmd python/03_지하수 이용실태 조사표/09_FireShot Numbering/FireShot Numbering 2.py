import tkinter as tk
from tkinter import ttk

# 메인 윈도우 생성
root = tk.Tk()
root.title("MainWindow - FireShotRenamerUI")
root.geometry("400x200")

# "Enter the Starting Number" 라벨
label = tk.Label(root, text="Enter the Starting Number", font=("Arial", 10))
label.pack(pady=10)

# 입력 필드
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# 체크박스
remove_header_var = tk.BooleanVar()
checkbox = tk.Checkbutton(root, text="Remove Header", variable=remove_header_var, font=("Arial", 10))
checkbox.pack(pady=5)

# 버튼
button = tk.Button(root, text="Change File Name", width=20, height=2)
button.pack(pady=20)

# 메인 루프 실행
root.mainloop()
