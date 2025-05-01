import os
import re
from pathlib import Path
from pyhwpx import Hwp
import time
import keyboard
from FileManger_V0_20250406 import FileBase


class WellType:
    """Class for determining and storing well configuration properties."""

    def __init__(self, directory=Path("d:/05_Send")):
        self.dangye_include = False
        self.report_yes = True
        self.n_well = 1
        self.directory = directory
        self._determine_well_type()

    def _determine_well_type(self):
        """Determine well type based on available image files."""
        fb = FileBase(self.directory)

        # Check if dangye (step) data is included
        jpg_files = fb.get_jpg_filter(".", "a1-*.jpg")
        self.dangye_include = len(jpg_files) == 4

        # Check if report files exist
        prt_files = fb.get_file_filter(".", "p*.jpg")
        self.report_yes = len(prt_files) > 0

        # Determine number of wells
        jpg_files = fb.get_jpg_filter(".", "a*.jpg")
        if jpg_files:
            last_filename = jpg_files[-1]
            match = re.search(r"a(\d+)-", last_filename)
            if match:
                self.n_well = int(match.group(1))
            else:
                self.n_well = 1

    def print_info(self):
        """Print well configuration information."""
        if self.dangye_include:
            print("-- 단계포함, include dangye --")
        else:
            print("-- 단계제외, exclude dangye --")

        print(f"Number of Well: {self.n_well}")


class ReportGenerator:
    """Class for generating well reports using HWP files."""

    def __init__(self, well_type):
        self.send_dir = Path("d:/05_Send")
        self.database_dir = Path("D:/09_hardRain/10_ihanseol - 2025/00_data/04_Reference Data/12_보고서, 부록")
        self.well_type = well_type
        self.fb = FileBase(self.send_dir)
        self.hwp = None

    @staticmethod
    def line_print(msg, n=80):
        print('-' * n)
        print(msg)
        print('-' * n)

    def pagesetup(self):
        my_page = {'위쪽': 20, '머리말': 10, '왼쪽': 20, '오른쪽': 20, '제본여백': 0, '꼬리말': 10, '아래쪽': 13, '제본타입': 0, '용지방향': 0,
                   '용지길이': 297, '용지폭': 210}

        self.hwp.set_pagedef(my_page, "cur")
        print(my_page)

    def merge_hwp_files(self):
        self.hwp = Hwp()  # 한/글 실행

        file_list = self.fb.get_file_filter(".", "*.hwp*")
        print(file_list)

        self.hwp.open(file_list[0])  # 첫 번째(0) 파일 열기
        for i in file_list[1:]:  # 첫 번째(0) 파일은 제외하고 두 번째(1)파일부터 아래 들여쓰기한 코드 반복
            self.hwp.MoveDocEnd()  # 한/글의 문서 끝으로 이동해서
            self.hwp.insert_file(i)  # 문서끼워넣기(기본값은 섹션, 글자, 문단, 스타일 모두 유지??)

        self.hwp.HAction.Run("MoveRight")
        self.hwp.HAction.Run('SelectAll')
        self.pagesetup()
        self.hwp.save_as("01_취합본.hwp")  # 반복이 끝났으면 "취합본.hwp"로 다른이름으로저장
        self.hwp.Quit()  # 한/글 프로그램 종료

        self.line_print(' delete left over hwpx files ....', 150)
        time.sleep(3)
        for _ in file_list:
            file = self.send_dir / _
            print(file)
            self.fb.delete_file(file)

    def prepare_template_files(self):
        """Copy appropriate template files based on well configuration."""
        for i in range(1, self.well_type.n_well + 1):
            if self.well_type.dangye_include:
                base_dir = self.database_dir / "A1_AQTESOLV_STEP"
                prefix = "" if self.well_type.report_yes else "00_"
                filename = f"{prefix}w{i}_AQTESOLV.hwpx"
            else:
                base_dir = self.database_dir / "A2_AQTESOLV_LONG"
                prefix = "" if self.well_type.report_yes else "00_"
                filename = f"{prefix}w{i}_AQTESOLV_Long.hwpx"

            source_file = base_dir / filename
            self.fb.copy_file(str(source_file), str(self.send_dir))

    def generate_reports(self):
        """Generate reports for all wells."""
        self.hwp = Hwp(visible=False)

        try:
            for i in range(1, self.well_type.n_well + 1):
                self._process_well_report(i)
        finally:
            if self.hwp:
                self.hwp.quit()

    def _process_well_report(self, well_no):
        """Process report for a specific well."""
        # Determine the filename based on well configuration

        self.line_print(f" _process_well_report,  Well : {well_no} ")

        if self.well_type.dangye_include:
            prefix = "" if self.well_type.report_yes else "00_"
            filename = f"{prefix}w{well_no}_AQTESOLV.hwpx"
        else:
            prefix = "" if self.well_type.report_yes else "00_"
            filename = f"{prefix}w{well_no}_AQTESOLV_Long.hwpx"

        # Open the file and insert images
        file_path = self.send_dir / filename
        self.hwp.open(str(file_path))
        print(f"Processing: {filename}")
        self._insert_images(well_no)
        self.hwp.Save()
        self.hwp.close()

    def _insert_images(self, well_no):
        """Insert appropriate images into the report."""
        # Define page configuration based on well type
        if self.well_type.dangye_include:
            insert_pages = [1, 5, 9, 13] if self.well_type.report_yes else [1, 2, 3, 4]
        else:
            insert_pages = [1, 5, 9] if self.well_type.report_yes else [1, 2, 3]

        # Get well images
        jpg_files = self.fb.get_jpg_filter(str(self.send_dir), f"a{well_no}-*.jpg")

        # Insert images at appropriate pages
        for i, page_num in enumerate(insert_pages):
            if i < len(jpg_files):
                self._goto_page(page_num)
                self._insert_image(jpg_files[i])

                # Insert additional report images if available
                pjpg_files = self.fb.get_jpg_filter(".", f"p{well_no}-{i + 1}*.jpg")
                for k, report_img in enumerate(pjpg_files):
                    self._goto_page(page_num + k + 1)
                    self._insert_image(report_img)

    def _goto_page(self, page_num):
        """Navigate to specific page in HWP document."""
        self.hwp.goto_page(page_num)
        self.hwp.HAction.Run("MoveRight")
        self.hwp.HAction.Run("MoveDown")

    def _insert_image(self, image_filename):
        """Insert an image into the current position in the document."""
        image_path = os.path.join(str(self.send_dir), image_filename)
        print(f"Inserting image: {image_filename}")
        self.hwp.insert_picture(image_path, treat_as_char=True, embedded=True, sizeoption=0)


def main():
    """Main program entry point."""
    # Initialize well configuration
    well_type = WellType()
    well_type.print_info()

    # Generate reports
    report_generator = ReportGenerator(well_type)

    report_generator.line_print(" Prepare template files  ... ", 130)
    report_generator.prepare_template_files()

    report_generator.line_print(" Generate files  ... ",130)
    report_generator.generate_reports()

    report_generator.line_print(" Merge HWP files  ... ",130)
    report_generator.merge_hwp_files()

    while True:
        keyboard.wait('space')
        print("Spacebar pressed!")


if __name__ == "__main__":
    main()
