import os
import time
import pandas as pd
from pyhwpx import Hwp
from pathlib import Path
import shutil
from make_appendix_06_refactored import AppendixMaker


class HwpProcessor:
    """Class to handle HWP document processing with Excel data."""

    def __init__(self):
        self.base_dir = Path("d:/05_Send")
        self.desktop = self.get_desktop()
        self.excel_file = "appendix_06.xlsx"
        self.hwp_template = "appendix_06(field).hwpx"
        self.hwp_output = "appendix_06(result).hwpx"
        self.hwp = None
        self.excel_data = None
        self.field_list = []

    @staticmethod
    def get_desktop():
        """Get the path to the user's desktop."""
        return Path(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    @staticmethod
    def countdown(seconds):
        """Display a countdown timer."""
        print(' Please Move the Command Window to Side ! ')
        for i in range(seconds, 0, -1):
            print(i)
            time.sleep(1)
        print("Time's up!")

    def prepare_environment(self):
        """Prepare the environment for processing."""
        # Create appendix data
        appendix_maker = AppendixMaker()
        appendix_maker.run()

        # Copy template file to desktop
        template_source = Path("c:/Program Files/totalcmd/ini/02_python") / self.hwp_template
        template_destination = self.desktop / self.hwp_template
        shutil.copy(template_source, template_destination)

        return True

    def load_excel_data(self):
        """Load data from Excel file."""
        try:
            excel_path = self.base_dir / self.excel_file
            self.excel_data = pd.read_excel(excel_path)
            return True
        except FileNotFoundError:
            print(f"Error: Excel file not found at {excel_path}")
            return False
        except Exception as e:
            print(f"Error loading Excel data: {str(e)}")
            return False

    def initialize_hwp(self):
        """Initialize HWP application."""
        try:
            self.hwp = Hwp(visible=False)
            return True
        except Exception as e:
            print(f"Error initializing HWP: {str(e)}")
            return False

    def open_hwp_template(self):
        """Open HWP template file."""
        template_path = self.desktop / self.hwp_template

        if not template_path.exists():
            print(f"Error: Template file not found at {template_path}")
            return False

        try:
            if not self.hwp.open(str(template_path)):
                print("Error: Failed to open HWP template file.")
                return False

            # Get field list
            fields = self.hwp.get_field_list(0, 0x02).split("\x02")
            self.field_list = [field for field in fields if field]
            print(f"Found {len(self.field_list)} fields: {self.field_list}")

            return True
        except Exception as e:
            print(f"Error opening HWP template: {str(e)}")
            return False

    def duplicate_pages(self):
        """Duplicate the template page for each data row."""
        try:
            # Select all content and copy
            self.hwp.Run('SelectAll')
            self.hwp.Run('Copy')
            self.hwp.MovePos(3)  # Move to end of document

            print('------------------------------------------------------')
            print('Page duplication started...')

            # Paste for each row in excel (minus 1 since we already have the template)
            row_count = len(self.excel_data)
            for i in range(row_count - 1):
                self.hwp.Run('Paste')
                self.hwp.MovePos(3)

            print(f'{row_count} pages created successfully.')
            print('------------------------------------------------------')
            return True
        except Exception as e:
            print(f"Error duplicating pages: {str(e)}")
            return False

    def fill_fields(self):
        """Fill fields with data from Excel."""
        try:
            for page, address in enumerate(self.excel_data.address):
                for field in self.field_list:
                    if field in self.excel_data.columns:
                        # Get data from Excel
                        data = self.excel_data[field].iloc[page]
                        # Handle NaN values
                        write_data = " " if pd.isna(data) else data

                        # Create field tag and insert data
                        field_tag = f'{field}{{{{{page}}}}}'
                        self.hwp.MoveToField(field_tag)
                        self.hwp.PutFieldText(field_tag, write_data)

                print(f'Page {page + 1}: {address}')
            return True
        except Exception as e:
            print(f"Error filling fields: {str(e)}")
            return False


    def delete_insert_field(self):
        """
            # functionOnScriptMacro_누름틀지우기()
            # {
            #     HAction.GetDefault("DeleteCtrls", HParameterSet.HDeleteCtrls.HSet);
            #     with (HParameterSet.HDeleteCtrls)
            #     {
            #     CreateItemArray("DeleteCtrlType", 1);
            #     DeleteCtrlType.Item(0) = 17;
            #     }
            #     HAction.Execute("DeleteCtrls", HParameterSet.HDeleteCtrls.HSet);
            #     }
            # }
        """

        pset = self.hwp.HParameterSet.HDeleteCtrls
        self.hwp.HAction.GetDefault("DeleteCtrls", pset.HSet)
        pset.CreateItemArray("DeleteCtrlType", 1)
        pset.DeleteCtrlType.SetItem(0, 17)
        self.hwp.HAction.Execute("DeleteCtrls", pset.HSet)


    def save_and_cleanup(self):
        """Save the document and clean up resources."""
        try:
            # Save the document
            # self.hwp.delete_all_fields()

            self.delete_insert_field()
            output_path = self.base_dir / self.hwp_output
            self.hwp.save_as(str(output_path))
            print(f"Document saved successfully to {output_path}")

            # Close HWP
            self.hwp.quit()

            # Remove template from desktop
            template_path = self.desktop / self.hwp_template
            if template_path.exists():
                os.remove(template_path)

            return True
        except Exception as e:
            print(f"Error during save and cleanup: {str(e)}")
            return False

    def run(self):
        """Run the complete HWP processing workflow."""
        print("Starting HWP document processing...")

        if not self.prepare_environment():
            return "Failed to prepare environment."

        # self.countdown(1)

        if not self.initialize_hwp():
            return "Failed to initialize HWP."

        if not self.load_excel_data():
            return "Failed to load Excel data."

        if not self.open_hwp_template():
            return "Failed to open HWP template."

        if not self.duplicate_pages():
            return "Failed to duplicate pages."

        if not self.fill_fields():
            return "Failed to fill fields with data."

        if not self.save_and_cleanup():
            return "Failed during save and cleanup."

        print('------------------------------------------------------')
        print("HWP document processing completed successfully.")
        return "Success"


def main():
    processor = HwpProcessor()
    result = processor.run()
    print(result)


if __name__ == "__main__":
    main()
