import tkinter as tk
from tkinter import ttk, scrolledtext


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("MainWindow")
        self.geometry("600x700")

        self.selected_company = tk.StringVar()
        self.selected_company.set("주식회사 한일지하수")  # Default value

        self.address_options = ["주소 1", "주소 2", "주소 3"]  # Example values
        self.engineering_options = ["Engineering Company A", "Engineering Company B",
                                    "Engineering Company C"]  # Example values
        self.message_options = ["Message 1", "Message 2", "Message 3"]  # Example values

        self.create_widgets()

    def create_widgets(self):
        # 프레임 생성
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)

        # 주소 콤보박스
        address_label = ttk.Label(main_frame, text="Address : ")
        address_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.address_combo = ttk.Combobox(main_frame, values=self.address_options)
        self.address_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.address_combo.set(self.address_options[0])  # Set initial value

        # Engineering Company 콤보박스
        eng_label = ttk.Label(main_frame, text="Engineering Company")
        eng_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.eng_combo = ttk.Combobox(main_frame, values=self.engineering_options)
        self.eng_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.eng_combo.set(self.engineering_options[0])  # Set initial value

        # 선택한 항목 레이블
        selected_label = ttk.Label(main_frame, text="선택한 항목:")
        selected_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.selected_item_label = ttk.Label(main_frame, text="주식회사 한일지하수")
        self.selected_item_label.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # 지하수 영향 조사자 라디오 버튼
        radio_frame = ttk.LabelFrame(main_frame, text="지하수 영향 조사자", padding=5)
        radio_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        companies = ["산수개발(주)", "대웅엔지니어링 주식회사", "(주)우경엔지니어링", "주식회사 한일지하수", "(주)동해엔지니어링", "(주)현윤이앤씨", "(주)태양이엔지",
                     "부여지하수개발 주식회사", "(주)전일", "삼원개발(주)", "마인지오 주식회사", "(합)청대개발", "주식회사 보성건설"]
        for i, company in enumerate(companies):
            radio_button = ttk.Radiobutton(radio_frame, text=company, variable=self.selected_company, value=company,
                                           command=self.update_selected_item_label)
            radio_button.grid(row=i, column=0, sticky="w")

        # 관정의 갯수 스핀박스
        count_label = ttk.Label(main_frame, text="관정의 갯수")
        count_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)

        self.count_spinbox = ttk.Spinbox(main_frame, from_=1, to=100)
        self.count_spinbox.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        self.count_spinbox.set(1)  # Set default value

        # 단계 포함 체크박스
        self.include_step_var = tk.BooleanVar()
        self.include_step_checkbox = ttk.Checkbutton(main_frame, text="단계포함", variable=self.include_step_var)
        self.include_step_checkbox.grid(row=4, column=2, sticky="w", padx=5, pady=5)

        # 탭 컨트롤
        self.tab_control = ttk.Notebook(main_frame)
        self.tab_control.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(5, weight=1)

        # Initial Generation 탭
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Initial Generation')

        # Project Info Setting 탭
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text='Projectinfo Setting')

        # Project Info Setting 탭의 텍스트 위젯
        project_info_text = """이것은, 프로젝트인포 세팅으로, 주어진 조사자(엔지니어링 회사)를 기준으로  주어진 주소값으로 필드를 채워나가는 것이다. 만일, 파일이 없으면, 파일을 복사해서와 채우고 파일이 있으면, 기존의 파일의 내용들만 업데이트를 시킨다. 그리고, 세종에머슨 포인트처럼, YanSoo.xlsx 파일이 있다면. 기존의 주소 필드는 무시하고, 엑셀파일의 데이터를 이용하고, 이것도 역시, Aqt파일이 Send 에 있으면 그냥 그파일만 업데이트 해주고 없으면, 관정의 갯수만큼 파일을 복사한뒤, 내용을 업데이트 해주게 된다."""

        self.project_info_text = scrolledtext.ScrolledText(self.tab2, wrap=tk.WORD)
        self.project_info_text.insert(tk.INSERT, project_info_text)
        self.project_info_text.config(state=tk.DISABLED)  # Make the text widget read-only
        self.project_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Message 콤보박스 (Initial Generation 탭)
        message_label = ttk.Label(self.tab1, text="Message")
        message_label.pack(side="left", padx=5, pady=5)

        self.message_combo = ttk.Combobox(self.tab1, values=self.message_options)
        self.message_combo.pack(side="left", padx=5, pady=5)
        self.message_combo.set(self.message_options[0])  # Set initial value

        # Run 및 Exit 버튼
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        run_button = ttk.Button(button_frame, text="Run", command=self.run_action)
        run_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        exit_button = ttk.Button(button_frame, text="Exit", command=self.destroy)
        exit_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    def run_action(self):
        selected_company = self.selected_company.get()
        num_wells = self.count_spinbox.get()
        include_step = self.include_step_var.get()
        print("Run Action : ")
        print(f"선택된 회사: {selected_company}")
        print(f"관정 갯수: {num_wells}")
        print(f"단계 포함: {include_step}")
        # 여기에 Run 버튼 클릭 시 실행할 코드를 작성합니다.

    def update_selected_item_label(self):
        selected_company = self.selected_company.get()
        self.selected_item_label.config(text=selected_company)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
