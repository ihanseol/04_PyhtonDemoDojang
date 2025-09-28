import win32gui
import win32con
import time
import pyautogui
import tkinter as tk


class SimpleWindowMover:
    def __init__(self):
        self.root = tk.Tk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.withdraw()  # 메인 윈도우 숨기기

        print(f"전체 화면 크기: {self.screen_width} x {self.screen_height}")

    def get_active_window(self):
        """현재 활성화된 윈도우 정보 가져오기"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                title = win32gui.GetWindowText(hwnd)
                rect = win32gui.GetWindowRect(hwnd)
                return hwnd, title, rect
        except:
            pass
        return None, None, None

    def move_window_to_second_monitor(self, hwnd):
        """윈도우를 2번째 모니터로 이동 (오른쪽 모니터로 가정)"""
        try:
            # 현재 윈도우 크기 가져오기
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]

            # 2번째 모니터 위치 계산 (1920x1080 해상도 가정)
            # 첫 번째 모니터가 1920px이라면 두 번째 모니터는 1920부터 시작
            primary_width = 1920  # 주 모니터 너비 (필요시 수정)

            # 2번째 모니터의 중앙 위치 계산
            second_monitor_x = primary_width + 100  # 2번째 모니터에서 100px 떨어진 위치
            second_monitor_y = 100

            # 윈도우 이동
            win32gui.SetWindowPos(
                hwnd,
                win32con.HWND_TOP,
                second_monitor_x,
                second_monitor_y,
                width,
                height,
                win32con.SWP_SHOWWINDOW
            )

            return True
        except Exception as e:
            print(f"오류 발생: {e}")
            return False

    def find_window_by_title(self, search_title):
        """창 제목으로 윈도우 찾기"""
        found_windows = []

        def enum_handler(hwnd, data):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if search_title.lower() in title.lower() and title.strip():
                    found_windows.append((hwnd, title))
            return True

        win32gui.EnumWindows(enum_handler, None)
        return found_windows


def move_with_keyboard_shortcut():
    """키보드 단축키로 윈도우 이동 (가장 간단한 방법)"""
    print("3초 후 현재 활성 윈도우를 오른쪽 모니터로 이동합니다...")
    print("이동하고 싶은 창을 활성화하세요!")

    # for i in range(3, 0, -1):
    #     print(f"{i}...")
    #     time.sleep(1)

    # Windows + Shift + 오른쪽 화살표
    pyautogui.hotkey('win', 'shift', 'right')
    print("완료! 윈도우가 오른쪽 모니터로 이동되었습니다.")


def main():
    print("=== 듀얼 모니터 윈도우 이동 도구 ===")
    print("1. 키보드 단축키 사용 (추천)")
    print("2. API 직접 제어")
    print("3. 특정 창 제목으로 찾아서 이동")

    choice = input("\n선택하세요 (1-3): ").strip()

    if choice == "1":
        move_with_keyboard_shortcut()

    elif choice == "2":
        mover = SimpleWindowMover()
        print("\n5초 후 활성 윈도우를 2번째 모니터로 이동합니다...")
        print("이동하고 싶은 창을 활성화하세요!")

        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        hwnd, title, rect = mover.get_active_window()
        if hwnd:
            print(f"'{title}' 창을 이동합니다...")
            if mover.move_window_to_second_monitor(hwnd):
                print("이동 완료!")
            else:
                print("이동 실패!")
        else:
            print("활성 윈도우를 찾을 수 없습니다.")

    elif choice == "3":
        mover = SimpleWindowMover()
        window_title = input("찾을 창의 제목을 입력하세요: ").strip()

        windows = mover.find_window_by_title(window_title)
        if windows:
            print(f"\n'{window_title}'와 관련된 창들:")
            for i, (hwnd, title) in enumerate(windows):
                print(f"{i + 1}. {title}")

            try:
                selection = int(input("이동할 창 번호: ")) - 1
                if 0 <= selection < len(windows):
                    hwnd, title = windows[selection]
                    print(f"'{title}' 창을 이동합니다...")
                    if mover.move_window_to_second_monitor(hwnd):
                        print("이동 완료!")
                    else:
                        print("이동 실패!")
                else:
                    print("잘못된 번호입니다.")
            except ValueError:
                print("숫자를 입력해주세요.")
        else:
            print(f"'{window_title}' 창을 찾을 수 없습니다.")
    else:
        print("잘못된 선택입니다.")


if __name__ == "__main__":
    # 필요한 라이브러리:
    # pip install pywin32 pyautogui

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
        input("엔터키를 눌러 종료...")