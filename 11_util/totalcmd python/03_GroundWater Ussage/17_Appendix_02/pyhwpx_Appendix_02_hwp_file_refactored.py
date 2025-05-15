import os
import time
import pandas as pd
from pyhwpx import Hwp
from pathlib import Path
import shutil
from make_appendix_02_refactored import AppendixMaker


class HwpDocumentGenerator:
    """Class to generate HWP documents from Excel data."""

    def __init__(self):
        """Initialize the document generator with default paths."""
        self.base_dir = Path("d:/05_Send")
        self.excel_file = "appendix_02.xlsx"
        self.hwp_template = "appendix_02(field).hwpx"
        self.hwp_output = "appendix_02(result).hwpx"
        self.template_source = Path("c:/Program Files/totalcmd/ini/02_python") / self.hwp_template
        self.desktop = self.get_desktop_path()
        self.hwp = None
        self.excel_data = None
        self.field_list = []

    @staticmethod
    def get_desktop_path():
        """Get the path to the user's desktop."""
        return Path(os.environ['USERPROFILE']) / 'Desktop'

    @staticmethod
    def display_countdown(seconds):
        """Display a countdown timer."""
        print(' Please Move the Command Window to Side ! ')
        for i in range(seconds, 0, -1):
            print(i)
            time.sleep(1)
        print("Time's up!")

    @staticmethod
    def prepare_excel_data():
        """Generate Excel data file using AppendixMaker."""
        try:
            appendix_maker = AppendixMaker()
            appendix_maker.run()
            return True
        except Exception as e:
            print(f"Error generating Excel data: {str(e)}")
            return False

    def copy_template_to_desktop(self):
        """Copy the HWP template file to the desktop."""
        try:
            desktop_template = self.desktop / self.hwp_template
            shutil.copy(self.template_source, desktop_template)
            return True
        except Exception as e:
            print(f"Error copying template to desktop: {str(e)}")
            return False

    def load_excel_data(self):
        """Load data from the Excel file."""
        try:
            excel_path = self.base_dir / self.excel_file
            self.excel_data = pd.read_excel(excel_path)
            print(f"Loaded {len(self.excel_data)} rows from Excel file.")
            return True
        except FileNotFoundError:
            print(f"Error: Excel file not found at {excel_path}")
            print("Make sure the Excel file is in the d:/05_Send/ folder.")
            return False
        except Exception as e:
            print(f"Error loading Excel data: {str(e)}")
            return False

    def initialize_hwp(self):
        """Initialize the HWP application."""
        try:
            self.hwp = Hwp(visible=False)
            return True
        except Exception as e:
            print(f"Error initializing HWP: {str(e)}")
            return False

    def open_template(self):
        """Open the HWP template file and extract field list."""
        try:
            template_path = self.desktop / self.hwp_template

            if not template_path.exists():
                print(f"Error: Template file not found at {template_path}")
                return False

            if not self.hwp.open(str(template_path)):
                print("Error: Failed to open HWP template file.")
                return False

            # Extract field list
            raw_field_list = self.hwp.get_field_list(0, 0x02).split("\x02")
            self.field_list = [field for field in raw_field_list if field]

            print(f"Found {len(self.field_list)} fields in template.")
            return True
        except Exception as e:
            print(f"Error opening template: {str(e)}")
            return False

    def duplicate_template(self):
        """Duplicate the template page for each row in Excel data."""
        try:
            # Select all content
            self.hwp.Run('SelectAll')
            self.hwp.Run('Copy')
            self.hwp.MovePos(3)  # Move to end of document

            print('------------------------------------------------------')
            print('Page duplication started...')

            # Number of pages needed (minus 1 for the original page)
            pages_to_create = len(self.excel_data) - 1

            for i in range(pages_to_create):
                self.hwp.Run('Paste')
                self.hwp.MovePos(3)

            print(f'{len(self.excel_data)} pages created successfully.')
            print('------------------------------------------------------')
            return True
        except Exception as e:
            print(f"Error duplicating template: {str(e)}")
            return False

    def fill_fields(self):
        """Fill all fields with data from Excel."""
        try:
            for page, address in enumerate(self.excel_data.address):
                for field in self.field_list:
                    # Skip fields that don't exist in Excel
                    if field not in self.excel_data.columns:
                        continue

                    # Get data from Excel
                    data = self.excel_data[field].iloc[page]
                    # Handle NaN values
                    write_data = " " if pd.isna(data) else data

                    field_tag = f'{field}{{{{{page}}}}}'
                    self.hwp.MoveToField(field_tag)
                    self.hwp.PutFieldText(field_tag, write_data)

                print(f'Page {page + 1}: {address}')
            return True
        except Exception as e:
            print(f"Error filling fields: {str(e)}")
            return False

    def save_and_cleanup(self):
        """Save the document and clean up resources."""
        try:
            # self.hwp.delete_all_fields()
            output_path = self.base_dir / self.hwp_output
            self.hwp.save_as(str(output_path))
            print(f"Document saved successfully to {output_path}")

            self.hwp.quit()

            template_path = self.desktop / self.hwp_template
            if template_path.exists():
                os.remove(template_path)

            return True
        except Exception as e:
            print(f"Error during save and cleanup: {str(e)}")
            return False

    def run(self):
        """Run the complete document generation process."""
        print("Starting HWP document generation...")

        if not self.prepare_excel_data():
            return "Failed to generate Excel data."

        # self.display_countdown(1)

        if not self.copy_template_to_desktop():
            return "Failed to copy template to desktop."

        if not self.load_excel_data():
            return "Failed to load Excel data."

        if not self.initialize_hwp():
            return "Failed to initialize HWP."

        if not self.open_template():
            return "Failed to open template."

        if not self.duplicate_template():
            return "Failed to duplicate template pages."

        if not self.fill_fields():
            return "Failed to fill fields with data."

        if not self.save_and_cleanup():
            return "Failed during save and cleanup."

        print('------------------------------------------------------')
        return "HWP document generation completed successfully."


def main():
    """Main function to run the document generator."""
    generator = HwpDocumentGenerator()
    result = generator.run()
    print(result)


if __name__ == "__main__":
    main()
