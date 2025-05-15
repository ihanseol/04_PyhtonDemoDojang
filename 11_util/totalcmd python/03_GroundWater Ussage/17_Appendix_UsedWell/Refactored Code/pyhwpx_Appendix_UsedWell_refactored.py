import time
import os
import glob
import pandas as pd
from pyhwpx import Hwp
import shutil
import merge_hwp_files as mh


class WellReportGenerator:
    """Class to handle well report generation from Excel data"""
    
    SS_INPUT = "ss_out.xlsx"
    AA_INPUT = "aa_out.xlsx"
    XL_BASE = "d:\\05_Send"
    HWP_BASE = r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\00_UsedWell"
    
    def __init__(self, mode="ss"):
        """Initialize with mode ('ss' or 'aa')"""
        self.mode = mode
        self.df = None
        self.hwp = None
    
    @staticmethod
    def get_desktop():
        """Get path to desktop directory"""
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        return desktop
    
    @staticmethod
    def countdown(n):
        """Countdown timer for n seconds"""
        print(' Please Move the Command Window to Side ! ')
        while n > 0:
            print(n)
            time.sleep(1)
            n -= 1
        print("Time's up!")
    
    def load_data(self):
        """Load and display well data from Excel file"""
        if self.mode == "aa":
            file_name = self.AA_INPUT
        else:
            file_name = self.SS_INPUT

        try:
            self.df = pd.read_excel(f"{self.XL_BASE}\\{file_name}")
        except FileNotFoundError:
            print(f"Error: XLSX file must be located in your {self.XL_BASE} folder.")
            return False

        self._display_data()
        return True
    
    def _display_data(self):
        """Display the data in formatted table"""
        if self.df is None:
            return
            
        length = len(self.df)
        format_string = "{:<6} {:<15} {:<5} {:<5} {:<5} {:<5} {:<7} {:<5}"

        # Print header
        print(format_string.format("gong", "address", "simdo", "well", "hp", "q", "purpose", "inout"))
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
                self.df.iloc[i]['inout']
            ))

        print("-" * 80)  # Separator line
        print()
    
    def _copy_hwp_templates(self):
        """Copy HWP template files according to data size"""
        if self.df is None:
            return False
            
        length = len(self.df)
        nquo, remainder = divmod(length, 25)
        template_prefix = "SS" if self.mode == "ss" else "AA"
        output_prefix = "ss" if self.mode == "ss" else "aa"

        if length <= 23:
            # For small datasets, just use the final template
            shutil.copy(f"{self.HWP_BASE}\\02_{template_prefix}_Final.hwpx", f"{self.XL_BASE}\\{output_prefix}_00.hwpx")
        else:
            # For larger datasets, use multiple templates
            i = 0
            if remainder != 0:
                for i in range(nquo):
                    source_file = f"{self.HWP_BASE}\\01_{template_prefix}_General.hwpx"
                    shutil.copy(source_file, f"{self.XL_BASE}\\{output_prefix}_0{i}.hwpx")
                shutil.copy(f"{self.HWP_BASE}\\02_{template_prefix}_Final.hwpx", f"{self.XL_BASE}\\{output_prefix}_0{i + 1}.hwpx")
            else:
                for i in range(nquo - 1):
                    shutil.copy(f"{self.HWP_BASE}\\01_{template_prefix}_General.hwpx", f"{self.XL_BASE}\\{output_prefix}_0{i}.hwpx")
                shutil.copy(f"{self.HWP_BASE}\\02_{template_prefix}_Final.hwpx", f"{self.XL_BASE}\\{output_prefix}_0{i + 1}.hwpx")
                
        return True
    
    def _fill_hwp_document(self):
        """Fill HWP document with data from Excel"""
        if self.df is None:
            return False
            
        os.chdir(self.XL_BASE)
        
        # Calculate summaries
        q_sum_in = self.df.loc[self.df['inout'] == "O", 'q'].sum()
        q_sum_out = self.df.loc[self.df['inout'] == "X", 'q'].sum()
        qo_count = len(self.df.loc[self.df['inout'] == "O", 'q'])
        qx_count = len(self.df.loc[self.df['inout'] == "X", 'q'])

        # Open HWP
        self.hwp = Hwp(visible=True)
        self.hwp.open("01_취합본.hwp")

        length = len(self.df)
        nquo, remainder = divmod(length, 25)

        # Fill main data pages
        for i in range(1, nquo + 1):
            self._fill_page_data(i)
            print("-" * 80)

        # Fill remainder data
        self.hwp.goto_page(nquo + 1)
        self._fill_remainder_data(nquo, remainder)

        # Fill summary fields
        self.hwp.goto_addr("b27")
        self.hwp.insert_text(f"{qo_count}개소(유역내)")
        
        self.hwp.goto_addr("b28")
        if q_sum_out == 0:
            self.hwp.insert_text("-")
        else:
            self.hwp.insert_text(f"{qx_count}개소(유역외)")

        self.hwp.goto_addr("f27")
        self.hwp.insert_text(str(q_sum_in))

        self.hwp.goto_addr("f28")
        if q_sum_out == 0:
            self.hwp.insert_text("-")
        else:
            self.hwp.insert_text(str(q_sum_out))

        # Save the document
        output_file = f"{self.get_desktop()}\\{self.mode}_report.hwp"
        self.hwp.save_as(output_file)
        self.hwp.Quit()
        self.hwp = None
        
        return True
        
    def _fill_page_data(self, page_number):
        """Fill data for a full page (25 rows)"""
        self.hwp.goto_page(page_number)
        j = 1
        for i in range((page_number - 1) * 25 + 1, page_number * 25 + 1):
            self._fill_row_data(i, j)
            j += 1
    
    def _fill_remainder_data(self, start_page, remainder):
        """Fill data for the remainder rows"""
        i = 1
        for j in range((start_page * 25) + 1, (start_page * 25) + remainder + 1):
            self._fill_row_data(j, i)
            i += 1
    
    def _fill_row_data(self, data_index, row_number):
        """Fill data for a single row"""
        row = self.df.iloc[data_index - 1]
        
        # Map of columns to addresses
        columns = {
            'gong': 'a', 
            'address': 'b', 
            'simdo': 'c',
            'well_diameter': 'd', 
            'hp': 'e', 
            'q': 'f',
            'purpose': 'g', 
            'inout': 'h'
        }
        
        # Fill each cell
        for col, addr_prefix in columns.items():
            self.hwp.goto_addr(f"{addr_prefix}{row_number + 2}")
            self.hwp.insert_text(str(row[col]))
    
    def generate_report(self):
        """Main method to generate the report"""
        # Load data from Excel
        if not self.load_data():
            return False
            
        # Copy HWP templates
        self._copy_hwp_templates()
        
        # Merge HWP files
        mh.merge_hwp_files()
        
        # Fill the merged document with data
        self._fill_hwp_document()
        
        # Clean up
        if os.path.exists("01_취합본.hwp"):
            os.remove("01_취합본.hwp")
            
        return True
    
    @staticmethod
    def move_hwp_files_from_desktop(destination_path):
        """Move HWP files from desktop to destination path"""
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        search_pattern = os.path.join(desktop_path, "*.hwp")
        hwp_files = glob.glob(search_pattern)

        if not hwp_files:
            print(f"No *.hwp files found on the Desktop.")
            return

        for file_path in hwp_files:
            try:
                shutil.move(file_path, destination_path)
                print(f"Moved: {os.path.basename(file_path)} to {destination_path}")
            except Exception as e:
                print(f"Error moving {os.path.basename(file_path)}: {e}")


def main():
    """Main function to run the application"""
    # Generate AA report
    aa_generator = WellReportGenerator(mode="aa")
    aa_generator.generate_report()
    
    # Countdown between reports
    WellReportGenerator.countdown(2)
    
    # Generate SS report
    ss_generator = WellReportGenerator(mode="ss")
    ss_generator.generate_report()
    
    # Move generated files from desktop
    WellReportGenerator.move_hwp_files_from_desktop(WellReportGenerator.XL_BASE)


if __name__ == "__main__":
    main()
