"""
Water Quality Report Generator - Refactored Version

This module extracts water quality data from PDF reports and generates
HWP (Hangul Word Processor) documents for each well tested.
"""

import re
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass, field

import pymupdf
from pyhwpx import Hwp

from merge_hwp_files import merge_hwp_files
from FileManger_V0_20250406 import FileBase

# Constants
WATER_QUALITY_PARAMS = {
    '총대장균군': 'Total_Coliform',
    '수소이온농도': 'pH',
    '염소이온': 'Chloride',
    '질산성질소': 'Nitrate_Nitrogen',
    '카드뮴': 'Cadmium',
    '비소': 'Arsenic',
    '시안': 'Cyanide',
    '수은': 'Mercury',
    '파라티온': 'Parathion',
    '다이아지논': 'Diazinon',
    '페놀': 'Phenol',
    '납': 'Lead',
    '크롬': 'Chromium',
    '1,1,1-트리클로로에탄': '1,1,1-Trichloroethane',
    '테트라클로로에틸렌': 'Tetrachloroethylene',
    '트리클로로에틸렌': 'Trichloroethylene',
    '벤젠': 'Benzene',
    '톨루엔': 'Toluene',
    '에틸벤젠': 'Ethylbenzene',
    '크실렌': 'Xylene'
}

BASE_DIR = Path("d:/05_Send")
TEMPLATE_DIR = Path("c:/Program Files/totalcmd/hwp")
HWP_TEMPLATE = "wt_domestic.hwp"


@dataclass
class WaterQualityData:
    """Data class to hold water quality test results."""
    Total_Coliform: str = ""
    pH: str = ""
    Chloride: str = ""
    Nitrate_Nitrogen: str = ""
    Cadmium: str = ""
    Arsenic: str = ""
    Cyanide: str = ""
    Mercury: str = ""
    Parathion: str = ""
    Diazinon: str = ""
    Phenol: str = ""
    Lead: str = ""
    Chromium: str = ""
    Trichloroethane: str = field(default="", metadata={'field_name': '1,1,1-Trichloroethane'})
    Tetrachloroethylene: str = ""
    Trichloroethylene: str = ""
    Benzene: str = ""
    Toluene: str = ""
    Ethylbenzene: str = ""
    Xylene: str = ""
    water_ok: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'WaterQualityData':
        """Create WaterQualityData instance from dictionary."""
        # Map the field names to handle special case
        mapped_data = {}
        for key, value in data.items():
            if key == '1,1,1-Trichloroethane':
                mapped_data['Trichloroethane'] = value
            else:
                mapped_data[key] = value
        return cls(**mapped_data)


class PDFParser:
    """Parser for extracting water quality data from PDF reports."""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_page_data(self, page_num: int) -> Dict[str, str]:
        """
        Extract water quality data from a specific page.

        Args:
            page_num: Page number (1-indexed)

        Returns:
            Dictionary containing water quality parameters and results
        """
        doc = pymupdf.open(self.pdf_path)

        if page_num > len(doc):
            doc.close()
            return {}

        try:
            page_obj = doc.load_page(page_num - 1)
            text = page_obj.get_text("text")
            return self._parse_page_text(text)
        finally:
            doc.close()

    def _parse_page_text(self, text: str) -> Dict[str, str]:
        """Parse text content and extract water quality data."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        if not lines:
            return {}

        print(f"Extracted {len(lines)} lines from page")

        # Determine water quality status
        water_ok = self._determine_water_status(lines)

        # Find the start of the results table
        start_idx = self._find_table_start(lines)
        if start_idx is None:
            return {}

        # Extract test results
        data = self._extract_test_results(lines, start_idx)
        data['water_ok'] = water_ok

        print('=' * 100)
        print(data)
        return data

    @staticmethod
    def _determine_water_status(lines: List[str]) -> str:
        """Determine if water quality is acceptable."""
        try:
            return '적합' if lines[-6] == '적합' else '부적합'
        except IndexError:
            return '부적합'

    @staticmethod
    def _find_table_start(lines: List[str]) -> Optional[int]:
        """Find the starting index of the results table."""
        for i, line in enumerate(lines):
            if line == '1':
                return i - 1
        return None

    def _extract_test_results(self, lines: List[str], start_idx: int) -> Dict[str, str]:
        """Extract test results from the lines starting at start_idx."""
        data = {}
        i = start_idx

        # Extract titles and results for 20 parameters
        line_results = []
        for j in range(20):
            try:
                line_results.append(lines[i + 3])
                i += 4
            except IndexError:
                break


        # print(f'line_results: {line_results}')
        # line_results: ['0', '7.2', '10.3', '1.4', '불검출', '0.009', '불검출', '불검출', '불검출', '불검출', '불검출', '불검출', '불검출',
        #                '불검출', '불검출', '불검출', '불검출', '불검출', '불검출', '불검출']
        # 이것은 그냥 결과값만을 저장하는 부분이다.


        # Map results to parameter names
        for idx, (korean_name, english_name) in enumerate(WATER_QUALITY_PARAMS.items()):
            if idx < len(line_results):
                data[english_name] = line_results[idx]
                print(f"{korean_name}: {data[english_name]}")

        return data

    def get_total_pages(self) -> int:
        """Get the total number of pages in the PDF."""
        doc = pymupdf.open(self.pdf_path)
        total_pages = len(doc)
        doc.close()
        return total_pages


class HWPDocumentGenerator:
    """Generator for HWP documents from water quality data."""

    def __init__(self, template_path: Path, output_dir: Path):
        self.template_path = template_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_document(self, well_name: str, data: WaterQualityData) -> Path:
        """
        Generate an HWP document for a specific well.

        Args:
            well_name: Name of the well (e.g., "W-1")
            data: WaterQualityData instance

        Returns:
            Path to the generated document
        """
        hwp = Hwp(visible=False)

        try:
            hwp.open(str(self.template_path))

            # Extract well index number
            well_index = self._extract_number(well_name)

            # Fill in all fields
            self._populate_document(hwp, well_name, well_index, data)

            # Save document
            output_path = self.output_dir / f"ex_domestic_{well_name}.hwp"
            hwp.save_as(str(output_path))

            return output_path
        finally:
            hwp.Quit(save=False)

    def _populate_document(self, hwp: Hwp, well_name: str,
                           well_index: Optional[int], data: WaterQualityData):
        """Populate the HWP document with data."""
        # Basic information
        self._write_field(hwp, 'index', well_index or "")
        self._write_field(hwp, 'well', well_name)
        self._write_field(hwp, 'water_ok', data.water_ok)

        # Water quality parameters
        param_mapping = {
            'ecoli': data.Total_Coliform,
            'ph': data.pH,
            'chloride': data.Chloride,
            'nitrogen': data.Nitrate_Nitrogen,
            'cadmium': data.Cadmium,
            'arsenic': data.Arsenic,
            'cyanide': data.Cyanide,
            'mercury': data.Mercury,
            'parathion': data.Parathion,
            'diazinon': data.Diazinon,
            'phenol': data.Phenol,
            'lead': data.Lead,
            'chromium': data.Chromium,
            'trichloroethane': data.Trichloroethane,
            'tetrachloroethylene': data.Tetrachloroethylene,
            'trichloroethylene': data.Trichloroethylene,
            'benzene': data.Benzene,
            'toluene': data.Toluene,
            'ethylbenzene': data.Ethylbenzene,
            'xylene': data.Xylene
        }

        for field_name, value in param_mapping.items():
            self._write_field(hwp, field_name, value)

    @staticmethod
    def _write_field(hwp: Hwp, placeholder: str, data: any):
        """Write data to a specific field in the HWP document."""
        hwp.MoveToField(placeholder)
        hwp.PutFieldText(placeholder, str(data))

    @staticmethod
    def _extract_number(text: str) -> Optional[int]:
        """Extract the first continuous sequence of digits from a string."""
        match = re.search(r'\d+', text)
        return int(match.group(0)) if match else None


class WaterQualityReportProcessor:
    """Main processor for generating water quality reports."""

    def __init__(self, pdf_path: str, template_path: Path, output_dir: Path):
        self.parser = PDFParser(pdf_path)
        self.generator = HWPDocumentGenerator(template_path, output_dir)

    def process_all_pages(self):
        """Process all pages in the PDF and generate HWP documents."""
        total_pages = self.parser.get_total_pages()
        print(f"Processing {total_pages} pages...")

        for page_num in range(1, total_pages + 1):
            print(f"\n{'=' * 100}")
            print(f"Processing page {page_num}/{total_pages}")

            # Extract data from PDF
            data_dict = self.parser.extract_page_data(page_num)

            if not data_dict:
                print(f"No data found on page {page_num}, skipping...")
                continue

            # Create data object
            water_data = WaterQualityData.from_dict(data_dict)

            # Generate well name
            well_name = f"W-{page_num}"

            # Generate HWP document
            output_path = self.generator.generate_document(well_name, water_data)
            print(f"Generated: {output_path}")

        print(f"\n{'=' * 100}")
        print("All documents generated. Merging HWP files...")
        merge_hwp_files()
        print("Process completed successfully!")


def main():
    """Main entry point for the application."""
    # Get PDF file
    fb = FileBase()
    file_list = fb.get_file_filter(".", "*.pdf")

    if not file_list:
        print("No PDF files found in the current directory.")
        return

    pdf_path = file_list[0]
    print(f"Processing PDF: {pdf_path}")

    # Set up paths
    template_path = TEMPLATE_DIR / HWP_TEMPLATE
    output_dir = BASE_DIR

    # Process the PDF
    processor = WaterQualityReportProcessor(pdf_path, template_path, output_dir)
    processor.process_all_pages()


if __name__ == "__main__":
    main()