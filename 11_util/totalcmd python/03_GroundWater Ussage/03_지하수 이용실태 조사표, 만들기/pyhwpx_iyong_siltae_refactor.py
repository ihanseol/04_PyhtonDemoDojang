from pyhwpx import Hwp
import os
import pandas as pd
import time
import psutil


def terminate_all_hwp():
    """
    프로세스 이름이 'hwp'로 시작하는 모든 실행 파일을 찾아 종료합니다.
    """
    killed_count = 0
    print("이름이 'hwp'로 시작하는 모든 프로세스 종료를 시작합니다...")

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_name = proc.info['name']

            # 프로세스 이름이 존재하고, 'hwp'로 시작하는지 확인 (대소문자 무시)
            if process_name and process_name.lower().startswith('hwp'):
                proc.kill()
                print(f"종료됨: {process_name} (PID: {proc.info['pid']})")
                killed_count += 1

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # 프로세스가 이미 종료되었거나 권한 문제 발생 시 무시
            pass

    if killed_count > 0:
        print(f"--- 총 {killed_count}개의 프로세스를 종료했습니다. ---")
    else:
        print("대상 프로세스를 찾지 못했습니다.")


class HwpProcessor:
    XL_INPUT = "iyong_template.xlsx"
    XL_BASE = "d:\\05_Send"
    HWP_INPUT = "iyong(field).hwp"
    HWP_OUTPUT = "iyong(result).hwp"

    def __init__(self):
        self.desktop = self._get_desktop()
        self.hwp = None
        self.excel = None
        self.field_list = None

    @staticmethod
    def line_print(msg):
        print('-' * 80)
        print(msg)
        print('-' * 80)

    @staticmethod
    def _get_desktop():
        """Get the path to the desktop directory."""
        return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    def initialize(self):
        """Initialize HWP and Excel objects."""
        try:
            self.excel = pd.read_excel(f"{self.XL_BASE}\\{self.XL_INPUT}")
        except FileNotFoundError:
            print(f"Error: XLSX file must be located in your {self.XL_BASE} folder.")
            return False

        self.hwp = Hwp(visible=False)
        return True

    def open_and_copy_template(self):
        """Open HWP template and make copies for each row in Excel."""
        if not self.hwp.open(f"{self.desktop}\\{self.HWP_INPUT}"):
            print("Error: 'iyong(field).hwp' file must be located in your desktop folder.")
            return False

        # Get field list
        self.field_list = [i for i in self.hwp.get_field_list(0, 0x02).split("\x02")]
        print(f"Found {len(self.field_list)} fields: {self.field_list}")

        # Copy the template page for each row in Excel
        self.hwp.Run('SelectAll')
        self.hwp.Run('Copy')
        self.hwp.MovePos(3)

        print('-'*80)
        print('Page copy started...')
        print(f"Creating {len(self.excel)} pages")

        # Create additional pages (one less than total since we already have one page)
        for i in range(len(self.excel) - 1):
            self.hwp.Run('Paste')
            self.hwp.MovePos(3)

        self.line_print(f'{len(self.excel)} page copy completed!')
        return True

    def fill_fields(self):
        """Fill fields with data from Excel for each page."""
        for page, address in enumerate(self.excel.address):
            for field in self.field_list:
                data = self.excel[field].iloc[page]
                write_data = " " if pd.isna(data) else data

                field_tag = f'{field}{{{{{page}}}}}'
                self.hwp.MoveToField(field_tag)
                self.hwp.PutFieldText(field_tag, write_data)

            print(f'Processed page {page + 1}: {address}')

    # def save_and_close(self):
    #     """Save the document and close HWP."""
    #     self.line_print(' Delete All Fields .... ')
    #     self.hwp.delete_all_fields()
    #     self.hwp.save_as(f"{self.XL_BASE}/{self.HWP_OUTPUT}")
    #     self.hwp.quit()
    #     self.line_print(f"Document saved to {self.XL_BASE}/{self.HWP_OUTPUT}")

    def save_and_close(self):
        """Save the document and close HWP with error handling."""
        try:
            self.line_print('필드 삭제 중...')
            self.hwp.delete_all_fields()

            # 저장 경로를 OS에 맞게 정규화
            output_path = os.path.abspath(os.path.join(self.XL_BASE, self.HWP_OUTPUT))

            self.line_print(f'파일 저장 중: {output_path}')
            self.hwp.save_as(output_path)

            # 한글 서버가 작업을 마칠 수 있도록 짧은 대기 시간 부여
            time.sleep(1)

            self.line_print('프로그램 종료 중...')
            # quit() 대신 Clear() 후 종료하는 방식이 더 안전할 수 있음
            self.hwp.Clear(option=True)
            self.hwp.Quit()


        except Exception as e:
            print(f"종료 중 오류 발생: {e}")
            # 강제 종료가 필요한 경우 등에 대비
        finally:
            self.line_print(f"작업 완료: {output_path}")

    def process(self):
        """Main processing method that orchestrates the workflow."""
        if not self.initialize():
            return

        if not self.open_and_copy_template():
            return

        self.fill_fields()
        self.save_and_close()


def main():
    processor = HwpProcessor()
    processor.process()
    terminate_all_hwp()


if __name__ == "__main__":
    main()
