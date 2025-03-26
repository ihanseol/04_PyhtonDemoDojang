import os
from pathlib import Path
import re
import time
from pyhwpx import Hwp
from FileProcessing_V4_20250211 import FileBase


class WellType:
    """Class for determining and storing well configuration properties."""

    def __init__(self, directory='D:\\05_Send\\'):
        self.DANGYE_INCLUDE = False
        self.REPORT_YES = True
        self.N_WELL = 1
        self.WELL_LIST = []
        self.Directory = directory
        self.determine_well_type()

    def get_welllist(self):
        fb = FileBase(self.Directory)
        jpg_files = fb.get_file_filter(".", "*-1_page1*.jpg")

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
        fb = FileBase(self.Directory)

        first_well = self.get_welllist()[0]
        print(" first well ;", first_well)

        jpg_files = fb.get_file_filter(".", f"w{self.WELL_LIST[0]}-*.jpg")

        if not jpg_files:
            jpg_files = fb.get_file_filter(".", f"w{self.WELL_LIST[0]}-1*.jpg")

        self.DANGYE_INCLUDE = len(jpg_files) == 6

        # Determine number of wells from file naming pattern
        jpg_files = fb.get_jpg_filter(".", "w*.jpg")
        if jpg_files:
            last_string = ''.join(jpg_files[-1:])
            extracted_number = self._extract_well_number(last_string)
            self.N_WELL = int(extracted_number)

    def _extract_well_number(self, filename):
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

    # Define constants
    SEND_DIR = Path("D:\\05_Send")
    DATA_BASE_DIR = Path(
        "D:\\09_hardRain\\10_ihanseol - 2025\\00_data\\04_Reference Data\\12_보고서, 부록\\A3_YangSoo_Report")

    def __init__(self, well_type):
        self.well_type = well_type
        self.fb = FileBase()
        self.hwp = None

    def prepare_template_files(self):
        """Copy appropriate template files based on well configuration."""
        for i in self.well_type.WELL_LIST:
            if self.well_type.DANGYE_INCLUDE:
                filename = f"A{i}_YangSoo_Step.hwpx"
            else:
                filename = f"B{i}_YangSoo_Long.hwpx"

            source_file = self.DATA_BASE_DIR / filename
            self.fb.copy_file(str(source_file), str(self.SEND_DIR))

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
        file_path = os.path.join(str(self.SEND_DIR), filename)
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
            jpg_files = self.fb.get_jpg_filter(str(self.SEND_DIR), f"w{well_no}-*.jpg")
        else:
            # 단계제외, 장기양수시험일보만
            jpg_files = self.fb.get_jpg_filter(str(self.SEND_DIR), f"w{well_no}_*.jpg")
            if not jpg_files:
                jpg_files = self.fb.get_jpg_filter(str(self.SEND_DIR), f"w-{well_no}_*.jpg")

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
        image_path = os.path.join(str(self.SEND_DIR), image_filename)
        print(image_filename)
        self.hwp.insert_picture(image_path, treat_as_char=True, embedded=True, sizeoption=0)


def main():
    """Main program entry point."""
    # Initialize well configuration
    wt = WellType()
    wt.print()

    # Generate reports
    report_generator = ReportGenerator(wt)
    report_generator.prepare_template_files()
    report_generator.generate_reports()


if __name__ == "__main__":
    main()
