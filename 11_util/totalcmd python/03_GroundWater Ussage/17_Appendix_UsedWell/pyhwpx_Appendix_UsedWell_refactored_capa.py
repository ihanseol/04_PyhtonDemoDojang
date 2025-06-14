import time
import os
import glob
import pandas as pd
from pyhwpx import Hwp
import shutil
import merge_hwp_files as mh


class HwpReportGenerator:
    """
    A class for generating HWP reports from Excel data.
    Handles both AA and SS report types.
    """
    # Constants
    SS_INPUT = "ss_out.xlsx"
    AA_INPUT = "aa_out.xlsx"
    II_INPUT = "ii_out.xlsx"
    XL_BASE = "d:\\05_Send"
    HWP_BASE = r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\00_UsedWell"

    def __init__(self):
        """Initialize the HwpReportGenerator"""
        self.df = None
        self.hwp = None
        self.mode = None

    @staticmethod
    def get_desktop():
        """Get the path to the desktop folder"""
        return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    @staticmethod
    def countdown(n):
        """Display a countdown timer"""
        print(' Please Move the Command Window to Side ! ')
        while n > 0:
            print(n)
            time.sleep(1)
            n -= 1
        print("Time's up!")

    def load_excel_data(self, mode):
        """
        Load data from Excel file based on mode (aa or ss)
        
        Args:
            mode (str): 'aa' or 'ss' mode selection
        
        Returns:
            bool: True if successful, False otherwise
        """
        self.mode = mode
        # file_name = self.AA_INPUT if mode == "aa" else self.SS_INPUT

        file_name = self.SS_INPUT

        match mode:
            case "ss":
                print("mode is ss ...")
                file_name = self.SS_INPUT
            case "aa":
                print("mode is aa ...")
                file_name = self.AA_INPUT
            case "ii":
                print("mode is ii ...")
                file_name = self.II_INPUT
            case _:  # The wildcard pattern, catches anything else
                print(f"Unknown command: {mode}")

        try:
            self.df = pd.read_excel(f"{self.XL_BASE}\\{file_name}")
        except FileNotFoundError:
            print(f"Error: {file_name} must be located in your {self.XL_BASE} folder.")
            return False

        self._display_data_summary()
        return True

    def _display_data_summary(self):
        """Display a summary of the loaded data"""
        if self.df is None:
            return

        length = len(self.df)
        format_string = "{:<6} {:<15} {:<5} {:<5} {:<5} {:<5} {:<7} {:<5} {:<5}"

        # Print header
        print(format_string.format("gong", "address", "simdo", "well", "hp", "q", "purpose", "inout", "capa"))
        print("-" * 80)  # Separator line

        # Print each row with aligned columns
        for i in range(length):
            print(format_string.format(
                self.df.iloc[i]['gong'],
                self.df.iloc[i]['address'],
                self.df.iloc[i]['simdo'],
                self.df.iloc[i]['well_diameter'],
                self.df.iloc[i]['hp'],
                self.df.iloc[i]['q'],
                self.df.iloc[i]['purpose'],
                self.df.iloc[i]['inout'],
                self.df.iloc[i]['capa']
            ))

        print("-" * 80)  # Separator line
        print()

    def prepare_hwp_files(self):
        """Prepare HWP template files based on data length"""
        if self.df is None or self.mode is None:
            print("Error: Data not loaded. Call load_excel_data first.")
            return

        length = len(self.df)
        nquo, remainder = divmod(length, 25)
        # file_prefix = "aa" if self.mode == "aa" else "ss"

        file_prefix = "ss"

        match self.mode:
            case "ss":
                print("<prepare_hwp_files> : mode is ss ...")
                file_prefix = "ss"
            case "aa":
                print("<prepare_hwp_files> : mode is aa ...")
                file_prefix = "aa"
            case "ii":
                print("<prepare_hwp_files> : mode is ii ...")
                file_prefix = "ii"
            case _:  # The wildcard pattern, catches anything else
                print(f"Unknown command: {self.mode}")

        general_template = f"01_{file_prefix.upper()}_General.hwpx"
        final_template = f"02_{file_prefix.upper()}_Final.hwpx"

        # Clean existing HWP files
        self.delete_hwp_files(f"{file_prefix}_*.hwpx")

        # Copy appropriate templates
        if length <= 24:
            shutil.copy(f"{self.HWP_BASE}\\{final_template}", f"{self.XL_BASE}\\{file_prefix}_00.hwpx")
        else:
            i = 0
            for i in range(nquo):
                source_file = f"{self.HWP_BASE}\\{general_template}"
                print(f"Copying template: {source_file}")
                shutil.copy(source_file, f"{self.XL_BASE}\\{file_prefix}_0{i}.hwpx")

            shutil.copy(f"{self.HWP_BASE}\\{final_template}", f"{self.XL_BASE}\\{file_prefix}_0{i + 1}.hwpx")

    def fill_report_data(self):
        """Fill the report with data from Excel"""
        if self.df is None or self.mode is None:
            print("Error: Data not loaded. Call load_excel_data first.")
            return

        # Change to output directory
        os.chdir(self.XL_BASE)

        # Merge HWP files first
        mh.merge_hwp_files()

        # Calculate summary values
        q_sum_in = round(self.df.loc[self.df['inout'] == "O", 'q'].sum(), 2)
        q_sum_out = round(self.df.loc[self.df['inout'] == "X", 'q'].sum(), 2)
        qo_count = len(self.df.loc[self.df['inout'] == "O", 'q'])
        qx_count = len(self.df.loc[self.df['inout'] == "X", 'q'])

        # Open HWP file
        self.hwp = Hwp(visible=False)
        self.hwp.open("01_취합본.hwp")

        # Fill data
        length = len(self.df)
        nquo, remainder = divmod(length, 25)

        # Fill full pages (25 rows each)
        for i in range(1, nquo + 1):
            self._fill_page_data(i)
            print("-" * 80)

        # Fill remaining rows on the last page
        self.hwp.goto_page(nquo + 1)
        self._fill_partial_page_data(nquo, remainder)

        # Fill summary information
        self.hwp.goto_addr("b27")
        self.hwp.insert_text(f"{qo_count}개소(유역내)")

        self.hwp.goto_addr("b28")
        if q_sum_out == 0:
            self.hwp.insert_text(f"0개소(유역외)")
        else:
            self.hwp.insert_text(f"{qx_count}개소(유역외)")

        self.hwp.goto_addr("g27")
        self.hwp.insert_text(str(q_sum_in))

        self.hwp.goto_addr("g28")
        if q_sum_out == 0:
            self.hwp.insert_text("-")
        else:
            self.hwp.insert_text(str(q_sum_out))

        # Save the report
        output_filename = f"{self.get_desktop()}\\{self.mode}_report.hwp"
        self.hwp.save_as(output_filename)
        self.hwp.Quit()
        self.hwp = None

    def _fill_page_data(self, page_num):
        """Fill data for a complete page (25 rows)"""
        self.hwp.goto_page(page_num)
        start_idx = (page_num - 1) * 25
        end_idx = page_num * 25

        for row_idx, data_idx in enumerate(range(start_idx, end_idx)):
            self._fill_row_data(row_idx + 1, data_idx)

    def _fill_partial_page_data(self, quotient, remainder):
        """Fill data for a partial page (less than 25 rows)"""
        start_idx = quotient * 25
        end_idx = start_idx + remainder

        for row_idx, data_idx in enumerate(range(start_idx, end_idx)):
            self._fill_row_data(row_idx + 1, data_idx)

    def _fill_row_data(self, row_num, data_idx):
        """Fill data for a single row"""
        columns = ['gong', 'address', 'simdo', 'well_diameter', 'hp', 'capa', 'q', 'purpose', 'inout']
        column_addrs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

        for col_addr, col_name in zip(column_addrs, columns):
            self.hwp.goto_addr(f"{col_addr}{row_num + 2}")
            value = str(self.df.iloc[data_idx][col_name])
            self.hwp.insert_text(value)

    def move_hwp_files_from_desktop(self, destination_path=None):
        """Move HWP files from desktop to destination path"""
        if destination_path is None:
            destination_path = self.XL_BASE

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        search_pattern = os.path.join(desktop_path, "*.hwp")
        hwp_files = glob.glob(search_pattern)

        if not hwp_files:
            print("No *.hwp files found on the Desktop.")
            return

        for file_path in hwp_files:
            try:
                shutil.move(file_path, destination_path)
                print(f"Moved: {os.path.basename(file_path)} to {destination_path}")
            except Exception as e:
                print(f"Error moving {os.path.basename(file_path)}: {e}")

    def delete_hwp_files(self, file_pattern):
        """Delete HWP files matching the pattern in XL_BASE directory"""
        os.chdir(self.XL_BASE)
        hwp_files = glob.glob(file_pattern)

        if not hwp_files:
            print(f"No files matching '{file_pattern}' found in {self.XL_BASE}.")
            return

        for file_path in hwp_files:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

    def process_aa_report(self):
        """Process AA report generation"""
        if self.load_excel_data("aa"):
            self.prepare_hwp_files()
            self.fill_report_data()
            if os.path.exists("01_취합본.hwp"):
                os.remove("01_취합본.hwp")

    def process_ss_report(self):
        """Process SS report generation"""
        if self.load_excel_data("ss"):
            self.prepare_hwp_files()
            self.fill_report_data()
            if os.path.exists("01_취합본.hwp"):
                os.remove("01_취합본.hwp")

    def process_ii_report(self):
        """Process SS report generation"""
        if self.load_excel_data("ii"):
            self.prepare_hwp_files()
            self.fill_report_data()
            if os.path.exists("01_취합본.hwp"):
                os.remove("01_취합본.hwp")


def main():
    """Main function to run the HWP report generator"""
    generator = HwpReportGenerator()

    # Clean up existing HWP files
    generator.delete_hwp_files("*.hwp*")

    # Process AA report
    generator.process_aa_report()

    # Countdown before processing SS report
    # generator.countdown(1)

    # Process SS report
    generator.process_ss_report()

    # Countdown before processing II report
    # generator.countdown(1)

    # Process II report
    generator.process_ii_report()

    # Move HWP files from desktop
    generator.move_hwp_files_from_desktop()

    # Merge HWP files for final report
    mh.merge_aassii_files("01_기사용관정.hwp")

    # Clean up temporary files
    generator.delete_hwp_files("a*.hwp")
    generator.delete_hwp_files("s*.hwp")
    generator.delete_hwp_files("i*.hwp")


if __name__ == "__main__":
    main()
