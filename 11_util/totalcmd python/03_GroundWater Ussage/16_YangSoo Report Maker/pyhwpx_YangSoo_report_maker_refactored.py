import os
import re
from pyhwpx import Hwp
from FileProcessing_V4_20250211 import FileBase
from pathlib import Path


class WellType:
    """Class for determining and storing well configuration properties."""

    def __init__(self, directory='D:\\05_Send\\'):
        self.DANGYE_INCLUDE = False
        self.REPORT_YES = True
        self.N_WELL = 1
        self.WELL_LIST = []
        self.Directory = directory
        self.fb = FileBase()
        self.determine_well_type()

    def get_welllist(self):
        jpg_files = self.fb.get_file_filter(".", "*1_page1*.jpg")

        print("number of jpgfiles :", len(jpg_files))
        print(jpg_files)
        print("-" * 50)

        return_well_list = []
        for well in jpg_files:
            # print(well)
            return_well_list.append(well.split("-1")[0])
            match = re.search(r"(\d+)", well)
            self.WELL_LIST.append(int(match.group(1)))

        return return_well_list

    def determine_well_type(self):
        """Determine well type and count based on available image files."""

        first_well = self.get_welllist()[0]
        print(" first well ;", first_well)

        jpg_files = self.fb.get_file_filter(".", f"w{self.WELL_LIST[0]}-*.jpg")

        if not jpg_files:
            jpg_files = self.fb.get_file_filter(".", f"w{self.WELL_LIST[0]}-1*.jpg")

        self.DANGYE_INCLUDE = len(jpg_files) == 6

        # Determine number of wells from file naming pattern
        jpg_files = self.fb.get_jpg_filter(".", "w*.jpg")
        if jpg_files:
            last_string = ''.join(jpg_files[-1:])
            extracted_number = self._extract_well_number(last_string)
            self.N_WELL = int(extracted_number)

    @staticmethod
    def _extract_well_number(filename):
        """Extract well number from filename using regex."""
        # First try to match digits followed by hyphen
        match = re.search(r"(\d+)-", filename)
        if match:
            return match.group(1)

        # If not found, try to match any digits
        match = re.search(r"(\d+)", filename)
        if match:
            return match.group(1)

        # Default to 1 if no match found
        return "1"

    def print(self):
        """Print well configuration information."""
        if self.DANGYE_INCLUDE:
            print("-- 단계포함, include dangye --")
        else:
            print("-- 단계제외, exclude dangye --")

        print(f"Number of Well : {self.N_WELL}")


class ReportGenerator:
    """Class for generating well reports using HWP files."""

    def __init__(self, well_type):
        self.send_dir = Path("d:/05_Send")
        self.database_dir = Path(
            "D:/09_hardRain/10_ihanseol - 2025/00_data/04_Reference Data/12_보고서, 부록/A3_YangSoo_Report")
        self.well_type = well_type
        self.fb = FileBase()
        self.hwp = None

    @staticmethod
    def line_print(msg):
        print('-' * 80)
        print(msg)
        print('-' * 80)

    def pagesetup(self):
        my_page = {'위쪽': 20, '머리말': 10, '왼쪽': 20, '오른쪽': 20, '제본여백': 0, '꼬리말': 10, '아래쪽': 13, '제본타입': 0, '용지방향': 0,
                   '용지길이': 297, '용지폭': 210}

        self.hwp.set_pagedef(my_page, "cur")
        print(my_page)

    def merge_hwp_files(self):
        self.hwp = Hwp()  # 한/글 실행

        file_list = self.fb.get_file_filter(".", "*.hwpx")
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

        self.line_print(' delete left over hwpx files ....')
        for _ in file_list:
            file = self.send_dir / _
            self.fb.delete_file(file)

    def prepare_template_files(self):
        """Copy appropriate template files based on well configuration."""
        for i in self.well_type.WELL_LIST:
            if self.well_type.DANGYE_INCLUDE:
                filename = f"A{i}_YangSoo_Step.hwpx"
            else:
                filename = f"B{i}_YangSoo_Long.hwpx"

            source_file = self.database_dir / filename
            self.fb.copy_file(str(source_file), str(self.send_dir))

    def generate_reports(self):
        """Generate reports for all wells."""
        self.hwp = Hwp(visible=False)

        try:
            for i in self.well_type.WELL_LIST:
                self._process_well_report(i)
        finally:
            if self.hwp:
                self.hwp.quit()

    def _process_well_report(self, well_no):
        """Process report for a specific well."""
        # Determine the filename based on well configuration
        if self.well_type.DANGYE_INCLUDE:
            filename = f"A{well_no}_YangSoo_Step.hwpx"
        else:
            filename = f"B{well_no}_YangSoo_Long.hwpx"

        # Open the file and insert images
        file_path = os.path.join(str(self.send_dir), filename)
        self.hwp.open(file_path)
        print(f"w{well_no} Report ...")
        self._insert_images(well_no)
        self.hwp.close()

    def _insert_images(self, well_no):
        """Insert appropriate images into the report."""
        jpg_files = self._get_well_images(well_no)

        # Insert images at each page
        for i in range(1, len(jpg_files) + 1):
            self._goto_page(i)
            self._insert_image(jpg_files[i - 1])

        self.hwp.Save()

    def _get_well_images(self, well_no):
        """Get the list of images for a specific well."""
        if self.well_type.DANGYE_INCLUDE:
            # 단계포함
            jpg_files = self.fb.get_jpg_filter(str(self.send_dir), f"w{well_no}-*.jpg")
        else:
            # 단계제외, 장기양수시험일보만
            jpg_files = self.fb.get_jpg_filter(str(self.send_dir), f"w{well_no}_*.jpg")

        print("jpg_files", jpg_files)
        return jpg_files

    def _goto_page(self, page_num):
        """Navigate to specific page in HWP document."""
        self.hwp.goto_page(page_num)
        if page_num == 1:
            self.hwp.HAction.Run("MoveRight")
            self.hwp.HAction.Run("MoveDown")
        else:
            self.hwp.HAction.Run("MoveRight")

    def _insert_image(self, image_filename):
        """Insert an image into the current position in the document."""
        image_path = self.send_dir / image_filename
        print(f'image_path: {image_path}, image_filename : {image_filename}')
        # self.hwp.insert_picture(image_path, treat_as_char=True, embedded=True, sizeoption=0)
        # pass by image_path cause error , i don't know why
        self.hwp.insert_picture(image_filename, treat_as_char=True, embedded=True, sizeoption=0)


def main():
    """Main program entry point."""
    # Initialize well configuration
    wt = WellType()
    wt.print()

    # Generate reports
    report_generator = ReportGenerator(wt)
    report_generator.prepare_template_files()
    report_generator.generate_reports()
    report_generator.merge_hwp_files()


if __name__ == "__main__":
    main()
