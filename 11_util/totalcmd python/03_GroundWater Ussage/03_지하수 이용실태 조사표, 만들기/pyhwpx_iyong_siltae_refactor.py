from pyhwpx import Hwp
import os
import pandas as pd


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

    def save_and_close(self):
        """Save the document and close HWP."""
        self.line_print(' Delete All Fields .... ')
        self.hwp.delete_all_fields()
        self.hwp.save_as(f"{self.XL_BASE}/{self.HWP_OUTPUT}")
        self.hwp.quit()
        self.line_print(f"Document saved to {self.XL_BASE}/{self.HWP_OUTPUT}")

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


if __name__ == "__main__":
    main()
