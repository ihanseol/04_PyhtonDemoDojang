import time
import os
import glob
import pandas as pd
from pyhwpx import Hwp # Assuming Hwp is correctly imported from pyhwpx
import shutil
import merge_hwp_files as mh # Keep the alias for the external merge script
from contextlib import contextmanager

# --- Utility Functions ---
def countdown(n):
    print(' Please Move the Command Window to Side ! ')
    while n > 0:
        print(n)
        time.sleep(1)
        n -= 1
    print("Time's up!")

@contextmanager
def change_cwd(path):
    old_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)

# --- Configuration Class ---
class AppConfig:
    SS_INPUT = "ss_out.xlsx"
    AA_INPUT = "aa_out.xlsx"
    XL_BASE = "d:\\05_Send"
    HWP_BASE_TEMPLATES = r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\00_UsedWell"
    
    @staticmethod
    def get_desktop_path():
        return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# --- HWP Automation Class ---
class HwpAutomator:
    def __init__(self, visible=False):
        self.hwp = Hwp(visible=visible)
        self.is_file_open = False

    def open(self, filepath):
        if self.hwp.open(filepath):
            self.is_file_open = True
            return True
        print(f"Error: Could not open HWP file {filepath}")
        return False

    def save_as(self, filepath):
        if not self.is_file_open:
            print("Error: No HWP file is open to save.")
            return False
        return self.hwp.save_as(filepath)

    def quit(self):
        if self.hwp:
            self.hwp.quit()
        self.is_file_open = False

    def goto_page(self, page_num):
        if not self.is_file_open: return
        self.hwp.goto_page(page_num)

    def goto_addr(self, addr):
        if not self.is_file_open: return
        self.hwp.goto_addr(addr)

    def insert_text(self, text):
        if not self.is_file_open: return
        self.hwp.insert_text(str(text)) # Ensure text is string

    def fill_data_row(self, data_series, hwp_table_row_index):
        """Fills a row in the HWP table using data from a Pandas Series."""
        if not self.is_file_open: return
        
        fields_map = {
            'gong': 'a', 'address': 'b', 'simdo': 'c',
            'well_diameter': 'd', 'hp': 'e', 'q': 'f',
            'purpose': 'g', 'inout': 'h'
        }
        for field_name, col_prefix in fields_map.items():
            self.goto_addr(f"{col_prefix}{hwp_table_row_index}")
            self.insert_text(data_series.get(field_name, ""))


# --- Data Handling Class ---
class DataHandler:
    def __init__(self, config):
        self.config = config

    def load_data(self, mode):
        file_name = self.config.AA_INPUT if mode == "aa" else self.config.SS_INPUT
        excel_path = os.path.join(self.config.XL_BASE, file_name)
        try:
            df = pd.read_excel(excel_path)
            # Ensure all relevant columns are treated as strings initially if needed,
            # or handle type conversion during HWP insertion.
            # For now, default pd.read_excel behavior is used.
            return df
        except FileNotFoundError:
            print(f"Error: XLSX file {excel_path} not found.")
            return None

    def print_data_summary(self, df):
        if df is None or df.empty:
            print("No data to summarize.")
            return

        length = len(df)
        format_string = "{:<6} {:<15} {:<5} {:<5} {:<5} {:<5} {:<7} {:<5}"
        print(format_string.format("gong", "address", "simdo", "well", "hp", "q", "purpose", "inout"))
        print("-" * 80)

        for i in range(length):
            print(format_string.format(
                df.iloc[i].get('gong', ''),
                df.iloc[i].get('address', ''),
                df.iloc[i].get('simdo', ''),
                df.iloc[i].get('well_diameter', ''),
                df.iloc[i].get('hp', ''),
                df.iloc[i].get('q', ''),
                df.iloc[i].get('purpose', ''),
                df.iloc[i].get('inout', '')
            ))
        print("-" * 80)
        print()

# --- File Management Class ---
class FileManager:
    def __init__(self, config):
        self.config = config

    def copy_template_files(self, mode, num_records):
        os.makedirs(self.config.XL_BASE, exist_ok=True) # Ensure XL_BASE exists
        
        general_template_name = "01_AA_General.hwpx" if mode == "aa" else "01_SS_General.hwpx"
        final_template_name = "02_AA_Final.hwpx" if mode == "aa" else "02_SS_Final.hwpx"
        
        src_general_path = os.path.join(self.config.HWP_BASE_TEMPLATES, general_template_name)
        src_final_path = os.path.join(self.config.HWP_BASE_TEMPLATES, final_template_name)

        if num_records <= 24: # Original logic was length <= 24, meaning 0 to 24 records.
            dest_path = os.path.join(self.config.XL_BASE, f"{mode}_00.hwpx")
            print(f"Copying {src_final_path} to {dest_path}")
            shutil.copy(src_final_path, dest_path)
        else:
            n_quotient, _ = divmod(num_records, 25)
            for i in range(n_quotient): # Copies general templates
                dest_path = os.path.join(self.config.XL_BASE, f"{mode}_0{i}.hwpx")
                print(f"Copying {src_general_path} to {dest_path}")
                shutil.copy(src_general_path, dest_path)
            
            # Copies the final template page
            final_dest_path = os.path.join(self.config.XL_BASE, f"{mode}_0{n_quotient}.hwpx")
            print(f"Copying {src_final_path} to {final_dest_path}")
            shutil.copy(src_final_path, final_dest_path)

    def merge_hwp_files_in_dir(self, base_path, output_filename=None, sort_option=None, pattern="*.hwpx"):
        """Wraps mh.merge_hwp_files, handling CWD and arguments."""
        with change_cwd(base_path):
            # This part needs to match how mh.merge_hwp_files is actually defined
            # Assuming: mh.merge_hwp_files(output_filename=None, sort_key=None, reverse_sort=False, pattern="*.hwpx")
            # Original calls:
            # 1. mh.merge_hwp_files() -> for templates, output "01_취합본.hwp", pattern "*.hwpx"
            # 2. mh.merge_hwp_files("01_기사용관정.hwp", "reverse") -> for reports, pattern "*.hwp" (implied)
            
            if output_filename is None and sort_option is None: # Case 1
                mh.merge_hwp_files(pattern=pattern) # Assumes default output "01_취합본.hwp"
            elif output_filename and sort_option == "reverse": # Case 2
                mh.merge_hwp_files(output_filename, sort_option, pattern=pattern) # Passes "reverse" literally
            elif output_filename:
                 mh.merge_hwp_files(output_filename, pattern=pattern)
            else:
                print(f"Warning: Unhandled merge case. Output: {output_filename}, Sort: {sort_option}, Pattern: {pattern}")
                mh.merge_hwp_files(pattern=pattern) # Default call

    def cleanup_files_by_pattern(self, directory, pattern):
        search_path = os.path.join(directory, pattern)
        files_to_delete = glob.glob(search_path)
        if not files_to_delete:
            print(f"No files matching {pattern} found in {directory} to delete.")
            return
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")
    
    def cleanup_file(self, filepath):
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            else:
                print(f"File not found for deletion: {filepath}")
        except OSError as e:
            print(f"Error deleting {filepath}: {e}")

    def move_reports_from_desktop(self, destination_dir):
        desktop_path = AppConfig.get_desktop_path()
        search_pattern = os.path.join(desktop_path, "*.hwp") # Only .hwp files
        hwp_files = glob.glob(search_pattern)

        if not hwp_files:
            print("No *.hwp files found on the Desktop to move.")
            return

        os.makedirs(destination_dir, exist_ok=True)
        for file_path in hwp_files:
            try:
                shutil.move(file_path, destination_dir)
                print(f"Moved: {os.path.basename(file_path)} to {destination_dir}")
            except Exception as e:
                print(f"Error moving {os.path.basename(file_path)}: {e}")


# --- Report Processing Class ---
class ReportProcessor:
    def __init__(self, mode, config, file_manager):
        self.mode = mode
        self.config = config
        self.df = None
        self.data_handler = DataHandler(config)
        self.file_manager = file_manager
        # HwpAutomator is created and destroyed within _populate_hwp

    def _prepare_data(self):
        self.df = self.data_handler.load_data(self.mode)
        if self.df is None or self.df.empty:
            print(f"No data loaded for mode '{self.mode}'. Aborting report generation for this mode.")
            return False
        self.data_handler.print_data_summary(self.df)
        return True

    def _populate_hwp(self):
        hwp_automator = HwpAutomator(visible=False) # Create new instance
        merged_hwp_path = os.path.join(self.config.XL_BASE, "01_취합본.hwp")
        
        if not hwp_automator.open(merged_hwp_path):
            print(f"Failed to open merged HWP: {merged_hwp_path}")
            hwp_automator.quit()
            return

        num_records = len(self.df)
        n_quotient, remainder = divmod(num_records, 25)

        # Loop for full 25-item pages
        for page_idx in range(n_quotient): # page_idx from 0 to n_quotient-1
            hwp_automator.goto_page(page_idx) # HWP pages are 0-indexed in pyhwpx
            current_hwp_table_row = 3 # Data starts at 3rd row of HWP table (a3, b3, etc.)
            start_df_idx = page_idx * 25
            for i in range(25):
                df_row_idx = start_df_idx + i
                hwp_automator.fill_data_row(self.df.iloc[df_row_idx], current_hwp_table_row)
                current_hwp_table_row += 1
        
        # Loop for the remaining items on the last page
        if remainder > 0:
            hwp_automator.goto_page(n_quotient) # Go to the next page (0-indexed)
            current_hwp_table_row = 3
            start_df_idx = n_quotient * 25
            for i in range(remainder):
                df_row_idx = start_df_idx + i
                hwp_automator.fill_data_row(self.df.iloc[df_row_idx], current_hwp_table_row)
                current_hwp_table_row += 1
        
        # Fill summary fields (assuming these are on the last page processed, or a specific page)
        # The original code implies these fields are on the page after the last data-filled page,
        # or on the last page if it's a "final" template.
        # For simplicity, assuming it's the page n_quotient (0-indexed for pages).
        if num_records > 0: # Only attempt to fill summary if there's data
             hwp_automator.goto_page(n_quotient) # Go to the page where summary fields are expected

        q_sum_in = round(self.df.loc[self.df['inout'] == "O", 'q'].sum(), 2)
        q_sum_out = round(self.df.loc[self.df['inout'] == "X", 'q'].sum(), 2)
        qo_count = len(self.df.loc[self.df['inout'] == "O", 'q'])
        qx_count = len(self.df.loc[self.df['inout'] == "X", 'q'])

        hwp_automator.goto_addr("b27")
        hwp_automator.insert_text(f"{qo_count}개소(유역내)")
        hwp_automator.goto_addr("b28")
        hwp_automator.insert_text(f"{qx_count}개소(유역외)" if q_sum_out != 0 else "-")
        
        hwp_automator.goto_addr("f27")
        hwp_automator.insert_text(str(q_sum_in))
        hwp_automator.goto_addr("f28")
        hwp_automator.insert_text(str(q_sum_out) if q_sum_out != 0 else "-")

        output_filename = f"{self.mode}_report.hwp"
        desktop_save_path = os.path.join(AppConfig.get_desktop_path(), output_filename)
        hwp_automator.save_as(desktop_save_path)
        print(f"Report saved to: {desktop_save_path}")
        hwp_automator.quit()

    def run(self):
        print(f"\n--- Starting report generation for mode: {self.mode.upper()} ---")
        if not self._prepare_data():
            return

        # 1. Copy template HWPX files
        self.file_manager.copy_template_files(self.mode, len(self.df))

        # 2. Merge these template HWPX files (e.g., ss_00.hwpx, ss_01.hwpx)
        #    into "01_취합본.hwp". The pattern must select only this mode's files.
        #    Current `merge_hwp_files_in_dir` uses a generic pattern.
        #    This relies on `XL_BASE` being clean or `mh.merge_hwp_files` being smart.
        #    For safety, pattern should be specific if `mh.merge_hwp_files` supports it.
        #    Assuming `mh.merge_hwp_files()` merges all *.hwpx in CWD.
        #    Since we cleanup *.hwp* first, then copy only {mode}_*.hwpx, this should be fine.
        print(f"Merging template files for mode '{self.mode}'...")
        self.file_manager.merge_hwp_files_in_dir(
            base_path=self.config.XL_BASE,
            pattern=f"{self.mode}_*.hwpx" # Crucial: ensure only mode-specific templates are merged
        )


        # 3. Populate the merged "01_취합본.hwp" with data
        self._populate_hwp()

        # 4. Clean up the merged "01_취합본.hwp"
        merged_hwp_to_delete = os.path.join(self.config.XL_BASE, "01_취합본.hwp")
        self.file_manager.cleanup_file(merged_hwp_to_delete)
        
        # 5. Clean up the individual {mode}_*.hwpx template files
        self.file_manager.cleanup_files_by_pattern(self.config.XL_BASE, f"{self.mode}_*.hwpx")

        print(f"--- Finished report generation for mode: {self.mode.upper()} ---")

# --- Main Application Class ---
class MainApplication:
    def __init__(self, config_class):
        self.config = config_class() # Instantiate config
        self.file_manager = FileManager(self.config)

    def run_full_process(self):
        # Initial cleanup of any HWP/HWPX files in the target directory
        print("Performing initial cleanup in target directory...")
        self.file_manager.cleanup_files_by_pattern(self.config.XL_BASE, "*.hwp*")

        # Process AA mode
        aa_processor = ReportProcessor("aa", self.config, self.file_manager)
        aa_processor.run()
        
        countdown(2)

        # Process SS mode
        ss_processor = ReportProcessor("ss", self.config, self.file_manager)
        ss_processor.run()

        # Move generated reports (aa_report.hwp, ss_report.hwp) from Desktop to XL_BASE
        print("Moving generated reports from Desktop...")
        self.file_manager.move_reports_from_desktop(self.config.XL_BASE)
        
        # Final merge of the two reports (aa_report.hwp, ss_report.hwp)
        print("Performing final merge of reports...")
        self.file_manager.merge_hwp_files_in_dir(
            base_path=self.config.XL_BASE,
            output_filename="01_기사용관정.hwp",
            sort_option="reverse", # This will be passed as the second argument to mh.merge_hwp_files
            pattern="*.hwp" # Merge .hwp files now
        )
        
        # Final cleanup of individual aa_report.hwp and ss_report.hwp
        print("Performing final cleanup of individual reports...")
        self.file_manager.cleanup_files_by_pattern(self.config.XL_BASE, "aa_report.hwp")
        self.file_manager.cleanup_files_by_pattern(self.config.XL_BASE, "ss_report.hwp")
        # The original script used "a*.hwp" and "s*.hwp" which is broader.
        # If specific names are known, it's safer. If other a* or s* files could exist,
        # then the original pattern is better. I'll stick to specific for now.
        # Reverting to original broader cleanup:
        # self.file_manager.cleanup_files_by_pattern(self.config.XL_BASE, "a*.hwp")
        # self.file_manager.cleanup_files_by_pattern(self.config.XL_BASE, "s*.hwp")
        # For this refactor, let's assume the exact names are what we want to delete.
        # If broader deletion is needed, uncomment above and comment out specific ones.

        print("\n>>> All processes completed. <<<")

if __name__ == "__main__":
    # Ensure the merge_hwp_files.py (aliased as mh) is in PYTHONPATH or same directory
    # and its merge_hwp_files function matches the assumed signature in FileManager.
    
    # Example of how `mh.merge_hwp_files` might be structured for compatibility:
    # File: merge_hwp_files.py
    # def merge_hwp_files(output_filename_param=None, sort_option_param=None, pattern="*.hwpx"):
    #     actual_output_filename = output_filename_param if output_filename_param else "01_취합본.hwp"
    #     files_to_merge = glob.glob(pattern)
    #     if not files_to_merge:
    #         print(f"No files found for pattern {pattern} in {os.getcwd()}")
    #         return
    #     print(f"Merging files: {files_to_merge} into {actual_output_filename}")
    #     if sort_option_param == "reverse":
    #         files_to_merge.sort(reverse=True) # Example sort
    #     else:
    #         files_to_merge.sort() # Default sort
    #     # ... actual HWP merging logic using pyhwpx or similar ...
    #     print(f"Files merged into {actual_output_filename}")

    app = MainApplication(AppConfig)
    app.run_full_process()