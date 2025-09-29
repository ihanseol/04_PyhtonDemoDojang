"""
YangSooInjector - A tool for automating well pumping test data processing
--------------------------------------------------------
This script automates the process of injecting data from YanSoo_Spec.xlsx
into pumping test Excel workbooks, handling both old and new versions
of the test formats.

Main functionalities:
- Reads well specifications from Excel
- Populates input forms in test workbooks
- Automates button clicking and form interactions
- Handles step tests, long-term tests, and water quality tests

Version History:
- 2024.3.25: Initial version - basic data reading and writing
- 2024.4.9: Converted to class, added error handling
- 2024.6.15: Added support for project, region names
- 2024.6.19: Added stable water level time handling
- 2024.6.26: Added support for both old and new form versions
- 2024.6.29: Refactored for improved structure and readability
"""
from typing import Dict, List, Optional, Union, Any, Tuple
import os
import re
import time
import random
from datetime import timedelta

import pandas as pd
import pyautogui
import pygetwindow as gw
import win32com.client as win32
from natsort import natsorted

# Mapping of stable time to corresponding MY_TIME values
STABLE_TIME_MAPPING = {
    60: 17, 75: 18, 90: 19, 105: 20, 120: 21, 140: 22, 160: 23, 180: 24,
    240: 25, 300: 26, 360: 27, 420: 28, 480: 29, 540: 30, 600: 31,
    660: 32, 720: 33, 780: 34, 840: 35, 900: 36, 960: 37, 1020: 38,
    1080: 39, 1140: 40, 1200: 41, 1260: 42, 1320: 43, 1380: 44,
    1440: 45, 1500: 46,
}


class YangSooInjector:
    """
    Automates the process of injecting data into YangSoo pumping test Excel workbooks
    and handling necessary button clicks and form interactions.
    """

    def __init__(self, directory: str, debug: bool = True):
        """
        Initialize the injector with directory and debug settings.

        Args:
            directory: Directory containing the source files
            debug: Whether to print debug information
        """
        self.directory = directory
        self.debug_yes = debug
        self.is_old_version = True
        self.stable_time = 0
        self.long_term_test_time = pd.Timestamp('2024-06-29 15:45:09')

        try:
            self.df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
            if self.debug_yes:
                print("Successfully loaded specification file")
        except Exception as e:
            print(f"Error loading YanSoo_Spec.xlsx: {e}")
            self.df = None

    @staticmethod
    def countdown(seconds: int) -> None:
        """Display a countdown timer."""
        print(' Please Move the Command Window to Side! ')
        for n in range(seconds, 0, -1):
            print(n)
            time.sleep(1)
        print("Time's up!")

    @staticmethod
    def extract_number(filename: str) -> int:
        """Extract a number from a string using regex."""
        return int(re.findall(r'\d+', filename)[0])

    @staticmethod
    def change_window(name_title: str) -> None:
        """Activate and maximize a window with the given title."""
        windows = gw.getWindowsWithTitle(name_title)
        if windows:
            window = windows[0]
            window.activate()
            if not window.isMaximized:
                window.maximize()
        else:
            print(f"No window with title '{name_title}' found.")

    def click_excel_button(self, worksheet, button_name: str) -> bool:
        """
        Click a button in an Excel worksheet with error handling.

        Args:
            worksheet: Excel worksheet object
            button_name: Name of the button to click

        Returns:
            bool: True if button was clicked successfully
        """

        def try_click_button():
            for obj in worksheet.OLEObjects():
                if obj.Name == button_name:
                    obj.Object.Value = True
                    return True
            return False

        while True:
            try:
                if not try_click_button():
                    return False
                break  # Exit the loop if no exception is raised
            except Exception as e:
                print(f"Error clicking button {button_name}: {e}")
                time.sleep(1)  # Wait before retrying
            finally:
                self.change_window('EXCEL')
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)

        return True

    def click_excel_buttons(self, worksheet, button_names: List[str]) -> bool:
        """
        Click multiple buttons in sequence.

        Args:
            worksheet: Excel worksheet object
            button_names: List of button names to click

        Returns:
            bool: True if all buttons were clicked successfully
        """
        success = True
        for button_name in button_names:
            result = self.click_excel_button(worksheet, button_name)
            if not result:
                print(f"Button '{button_name}' not found")
                success = False
            else:
                print(f"Successfully clicked button '{button_name}'")
        return success

    @staticmethod
    def is_old_version(worksheet, new_button_name: str) -> bool:
        """
        Check if the worksheet is using the old version based on button presence.

        Args:
            worksheet: Excel worksheet object
            new_button_name: Name of a button that exists only in the new version

        Returns:
            bool: True if old version (button not found), False if new version
        """
        for obj in worksheet.OLEObjects():
            if obj.Name == new_button_name:
                return False
        return True

    def get_excel_row(self, row_index: int) -> Optional[List]:
        """
        Get a row of data from the specification dataframe.

        Args:
            row_index: Index of the row to retrieve

        Returns:
            List of values from the row or None if index is out of bounds
        """
        try:
            return self.df.iloc[row_index, :].tolist()
        except (IndexError, AttributeError):
            return None

    def localize_and_adjust_timestamp(self, timestamp) -> pd.Timestamp:
        """
        Localize timestamp to UTC and add 10 seconds.

        Args:
            timestamp: Timestamp to adjust

        Returns:
            Adjusted and localized timestamp
        """
        try:
            # Ensure we have a pandas Timestamp
            if not isinstance(timestamp, pd.Timestamp):
                timestamp = pd.Timestamp(timestamp)

            # Localize to UTC if naive (no timezone)
            if timestamp.tzinfo is None:
                timestamp = timestamp.tz_localize('UTC')

            # Add 10 seconds
            timestamp += timedelta(seconds=10)

            return timestamp
        except Exception as e:
            print(f"Error processing timestamp: {e}")
            # Return original if failed
            return timestamp if isinstance(timestamp, pd.Timestamp) else pd.Timestamp.now()

    def prepare_cell_values(self, row_index: int) -> Dict[str, Any]:
        """
        Prepare a dictionary of cell values from the specification data.

        Args:
            row_index: Index of the row in the specification data

        Returns:
            Dictionary mapping cell references to values
        """
        row_data = self.get_excel_row(row_index)
        if not row_data:
            print(f"No data found for row index {row_index}")
            return {}

        if self.debug_yes:
            print(f'Number of columns in row data: {len(row_data)}')

        # Extract basic well data
        address, hp, casing, well_rad, simdo, q, natural, stable = row_data[1:9]

        # Default values for optional fields
        project_name = jigu_name = company_name = ''
        ph = 7.0

        # Extract stable time if available
        self.stable_time = row_data[12] if len(row_data) > 12 else 0

        # Handle long term test time if available
        if len(row_data) > 13 and pd.notna(row_data[13]):
            self.long_term_test_time = row_data[13].tz_localize('UTC')
            if self.debug_yes:
                print(f'Long test time: {self.long_term_test_time}')

        # Extract additional fields if available
        if len(row_data) > 9:
            project_name, jigu_name, company_name = row_data[9:12]
            if len(row_data) > 15 and pd.notna(row_data[15]):
                ph = row_data[15]

        # Swap natural and stable if stable is less than natural (to prevent errors)
        if stable < natural:
            natural, stable = stable, natural
            if self.debug_yes:
                print("Swapped natural and stable levels (stable was less than natural)")

        # Format well number
        gong = self.extract_number(row_data[0])
        str_gong = f"공  번 : W - {gong}"

        # Create the dictionary of cell values
        cell_values = {
            "J48": str_gong,
            "I46": address,
            "I52": casing,
            "I48": hp,
            "M44": well_rad,
            "M45": simdo,
            "M48": natural,
            "M49": stable,
            "M51": q
        }

        # Add optional fields if available
        if len(row_data) > 9:
            cell_values.update({
                "I44": project_name,
                "I45": jigu_name,
                "I47": company_name,
                "c9": ph
            })

        return cell_values

    def inject_values_to_cells(self, workbook) -> None:
        """
        Inject values from specification data into the Excel workbook.

        Args:
            workbook: Excel workbook object
        """
        input_sheet = workbook.Worksheets("Input")
        w1_sheet = workbook.Worksheets("w1")

        # Extract file number to determine row index
        filename = os.path.basename(workbook.Name)
        row_index = self.extract_number(filename) - 1

        if self.debug_yes:
            print('Preparing cell values...')

        cell_values = self.prepare_cell_values(row_index)

        # Set a default stable level to prevent errors
        input_sheet.Range("M49").Value = 300

        # Inject each value
        for cell, value in cell_values.items():
            print(f'Injecting {value} into cell {cell}')

            # Handle special case for pH value in w1 sheet
            if cell != "c9":
                input_sheet.Range(cell).Value = value
            else:
                w1_sheet.Range(cell).Value = value

            time.sleep(0.5)  # Small delay to prevent overwhelming Excel

        if self.debug_yes:
            print('Cell value injection complete')

    def process_workbook(self, workbook, excel_app) -> None:
        """
        Process an Excel workbook by injecting values and automating tests.

        Args:
            workbook: Excel workbook object
            excel_app: Excel application object
        """
        if self.debug_yes:
            print('Starting input injection process...')

        # Process each test section
        self.process_input_section(workbook, excel_app)

        print('')
        if self.debug_yes:
            print('Processing step test...')
        self.process_step_test(workbook)

        print('')
        if self.debug_yes:
            print('Processing long term test...')
        self.process_long_term_test(workbook, excel_app)

        print('')
        if self.debug_yes:
            print('Processing water quality check...')
        self.process_water_quality_test(workbook)

    def process_input_section(self, workbook, excel_app) -> None:
        """
        Process the Input worksheet in the workbook.

        Args:
            workbook: Excel workbook object
            excel_app: Excel application object
        """
        worksheet = workbook.Worksheets("Input")
        worksheet.Activate()
        time.sleep(1)

        # Inject cell values
        self.inject_values_to_cells(workbook)
        time.sleep(1)

        # Ensure Excel is the active window and scroll to top
        self.change_window('EXCEL')
        excel_app.Application.SendKeys("{PGUP}")

        # Define button sets for old and new versions
        button_mapping = {
            "old": {
                "buttons": ["CommandButton2", "CommandButton3", "CommandButton6", "CommandButton1"],
                "labels": ['SetCB1', 'SetCB2', 'Chart', 'PumpingTest']
            },
            "new": {
                "buttons": ["CommandButton_CB1", "CommandButton_CB2", "CommandButton_Chart"],
                "labels": ['SetCB1', 'SetCB2', 'SetChart']
            }
        }

        # Determine version and select appropriate button set
        if self.is_old_version(worksheet, button_mapping["new"]["buttons"][0]):
            self.is_old_version = True
            print("Detected old version of YangSoo")
            buttons = button_mapping["old"]["buttons"]
            labels = button_mapping["old"]["labels"]
        else:
            self.is_old_version = False
            print("Detected new version of YangSoo")
            buttons = button_mapping["new"]["buttons"]
            labels = button_mapping["new"]["labels"]

        # Click each button in sequence
        for button, label in zip(buttons, labels):
            self.click_excel_button(worksheet, button)
            print(f'Processed {label}')
            time.sleep(1)

    def process_step_test(self, workbook) -> None:
        """
        Process the stepTest worksheet in the workbook.

        Args:
            workbook: Excel workbook object
        """
        worksheet = workbook.Worksheets("stepTest")
        worksheet.Activate()
        time.sleep(1)

        # Click the FindAnswer button
        print('Step Test: Clicking FindAnswer button')
        self.click_excel_button(worksheet, "CommandButton1")
        time.sleep(2)

        # Click the Check button
        print('Step Test: Clicking Check button')
        self.click_excel_button(worksheet, "CommandButton2")

    def process_long_term_test(self, workbook, excel_app) -> None:
        """
        Process the LongTest worksheet in the workbook.

        Args:
            workbook: Excel workbook object
            excel_app: Excel application object
        """
        worksheet = workbook.Worksheets("LongTest")
        skin_worksheet = workbook.Worksheets("SkinFactor")
        worksheet.Activate()

        # Clear GoalSeekTarget
        worksheet.Range("GoalSeekTarget").Value = 0

        # Select stable time value (either from spec or random)
        possible_times = [540, 600, 660, 720, 780, 840]
        selected_time = random.choice(possible_times) if self.stable_time == 0 else self.stable_time
        skin_worksheet.Range("G16").Value = selected_time

        if self.debug_yes:
            print(f'Selected stable time: {selected_time}')

        # Define sequence of actions to perform
        actions = [
            {"type": "button", "name": "CommandButton5", "label": "Reset 0.1", "delay": 1},
            {"type": "combobox", "name": "ComboBox1", "value": selected_time, "delay": 1},
            {"type": "module", "modules": ["mod_W1LongtermTEST", "mod_W1_LongtermTEST"], "delay": 1},
            {"type": "button", "name": "CommandButton5", "label": "Reset 0.1", "delay": 1},
            {"type": "button", "name": "CommandButton4", "label": "FindAnswer", "delay": 2},
            {"type": "button", "name": "CommandButton7", "label": "Check", "delay": 0}
        ]

        # Set timestamp for test
        try:
            if self.long_term_test_time is not None:
                worksheet.Range("C10").Value = self.long_term_test_time
        except Exception as e:
            print(f"Error setting timestamp: {e}")

        # Execute each action in sequence
        for action in actions:
            if action["type"] == "button":
                print(f'Long Term Test: Clicking {action["label"]} button')
                self.click_excel_button(worksheet, action["name"])
            elif action["type"] == "combobox":
                worksheet.OLEObjects(action["name"]).Object.Value = action["value"]
                print(f'Long Term Test: Set ComboBox value to {action["value"]}')
            elif action["type"] == "module":
                print('Long Term Test: Running Excel macros')
                self.run_excel_modules(excel_app, action["modules"])

            time.sleep(action["delay"])

    def run_excel_modules(self, excel_app, module_names: List[str]) -> None:
        """
        Run Excel VBA modules.

        Args:
            excel_app: Excel application object
            module_names: List of module names (for old and new versions)
        """
        # Select module name based on version
        module_name = module_names[0] if self.is_old_version else module_names[1]

        # Run the macros
        excel_app.Application.Run(f"{module_name}.SetMY_TIME")
        excel_app.Application.Run(f"{module_name}.TimeSetting")

        time.sleep(1)
        print(f"Successfully ran Excel module {module_name}")

    def process_water_quality_test(self, workbook) -> None:
        """
        Process the w1 (water quality) worksheet in the workbook.

        Args:
            workbook: Excel workbook object
        """
        worksheet = workbook.Worksheets("w1")
        worksheet.Activate()
        print("Processing water quality test (w1 sheet)")

        # Random temperature and electrical conductivity values
        temp_values = [14.8, 14.9, 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7]
        ec_values = [200, 201, 202, 219, 203, 204, 218, 205, 206, 213, 207,
                     208, 209, 210, 211, 215, 217]

        temp = random.choice(temp_values)
        ec = random.choice(ec_values)

        if self.debug_yes:
            print(f'Setting water temperature to {temp}°C')
        worksheet.Range("C7").Value = temp

        if self.debug_yes:
            print(f'Setting electrical conductivity to {ec}')
        worksheet.Range("C8").Value = ec

        # Click the adjustment button
        print('Water Quality: Clicking Make adjust Value button')
        self.click_excel_button(worksheet, "CommandButton2")
        time.sleep(1)

    def validate_data(self) -> Optional[List[str]]:
        """
        Validate data and collect files to process.

        Returns:
            List of filenames to process or None if validation fails
        """

        def collect_target_files():
            files = natsorted([f for f in os.listdir() if f.endswith('.xlsm')])
            return [f for f in files if "ge_OriginalSaveFile" in f]

        # Change to target directory
        os.chdir(self.directory)
        target_files = collect_target_files()

        if not target_files:
            print("No YangSoo .xlsm files found in directory.")
            return None

        # Validate data for the last file
        last_file = target_files[-1]
        row_index = self.extract_number(last_file) - 1
        if self.get_excel_row(row_index) is None:
            print(f"No data found for file {last_file} (row index {row_index}).")
            return None

        return target_files

    def process_files(self) -> None:
        """
        Main method to process all files in the directory.
        """
        self.countdown(5)

        # Validate and get list of files
        files = self.validate_data()
        if files is None:
            print("Validation failed - cannot proceed.")
            return

        # Initialize Excel application
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.ScreenUpdating = False
        excel.Visible = True
        excel.WindowState = -4137  # xlMaximizedWindow
        self.change_window('EXCEL')

        # Process each file
        for file in files:
            if self.debug_yes:
                print(f'Processing file: {file}')

            file_path = os.path.join(self.directory, file)
            wb = excel.Workbooks.Open(file_path)

            print('\n\n')
            print('-' * 80)
            print(f'Processing file: {file}')
            print('-' * 80)

            # Process the workbook
            self.process_workbook(wb, excel)

            # Save and close
            wb.Close(SaveChanges=True)

        # Clean up Excel
        excel.ScreenUpdating = True
        excel.Quit()

        if self.debug_yes:
            print('All files processed successfully.')

    @staticmethod
    def clean_output_directory(folder_path: str) -> None:
        """
        Remove existing .xlsm files from the output directory.

        Args:
            folder_path: Path to the output directory
        """
        if not os.path.exists(folder_path):
            print(f"Output directory {folder_path} does not exist.")
            return

        files = os.listdir(folder_path)
        xlsm_files = [f for f in files if f.endswith('.xlsm')]

        for file in xlsm_files:
            file_path = os.path.join(folder_path, file)
            try:
                os.remove(file_path)
                print(f"Removed {file} from output directory.")
            except Exception as e:
                print(f"Error removing {file}: {e}")


def main():
    """Entry point for the script."""
    # Initialize injector with source directory
    injector = YangSooInjector("d:\\05_Send\\")

    # Clean output directory before processing
    output_dir = r"c:/Users/minhwasoo/Documents/"
    injector.clean_output_directory(output_dir)

    # Process the files
    injector.process_files()


if __name__ == "__main__":
    main()