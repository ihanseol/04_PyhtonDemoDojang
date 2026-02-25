import pymupdf
import re
from pyhwpx import Hwp
from pathlib import Path
import os
from abc import ABC, abstractmethod
from typing import Dict, Optional, List
import enum
from enum import Enum

import sys
import psutil
from typing import Optional

from merge_hwp_files import merge_hwp_files
from FileManger_V0_20250406 import FileBase

from pdf_dringking46_engine import get_data_hanwool
from pdf_dringking46_engine import get_data_malgun_hwangyung
from pdf_dringking46_engine import get_data_kiwii
from pdf_dringking46_engine import get_data_malgeunmul
from pdf_dringking46_engine import get_data_nurilife

BASE_DIR = Path("d:/05_Send")
TEMPLATE_DIR = Path("c:/Program Files/totalcmd/hwp")
HWP_TEMPLATE = "wt_dringking46.hwp"

def terminate_all_hwp():
    """
    프로세스 이름이 'hwp'로 시작하는 모든 실행 파일을 찾아 종료합니다.
    """
    killed_count = 0
    print("이름이 'hwp'로 시작하는 모든 프로세스 종료를 시작합니다...")

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_name = proc.info['name']

            # 프로세스 이름이 존재하고, 'hwp'로 시작하는지 확인 (대소문자 무시)
            if process_name and process_name.lower().startswith('hwp'):
                proc.kill()
                print(f"종료됨: {process_name} (PID: {proc.info['pid']})")
                killed_count += 1

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # 프로세스가 이미 종료되었거나 권한 문제 발생 시 무시
            pass

    if killed_count > 0:
        print(f"--- 총 {killed_count}개의 프로세스를 종료했습니다. ---")
    else:
        print("대상 프로세스를 찾지 못했습니다.")


class PDFEngineType(Enum):
    """Supported PDF parsing engines."""
    HANWOOL = "hanwool"
    MALGUN_HWANGYUNG = "malgun_hwangyung"
    KIWII = "kiwii"
    MALGEUNMUL = "malgeunmul"
    NURILIFE = "nurilife"

    # Add future engines here
    # ALTERNATIVE = "alternative"
    # CUSTOM = "custom"


class PDFEngine(ABC):
    """Abstract base class for PDF parsing engines."""

    @abstractmethod
    def extract_data(self, pdf_path: str, page_number: int) -> Dict[str, str]:
        """
        Extract water quality data from a PDF page.

        Args:
            pdf_path: Path to the PDF file
            page_number: Page number to extract (1-indexed)

        Returns:
            Dictionary containing water quality parameters
        """
        pass

    @abstractmethod
    def validate_pdf(self, pdf_path: str) -> bool:
        """
        Validate if the PDF is compatible with this engine.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            True if compatible, False otherwise
        """
        pass


class HanwoolPDFEngine(PDFEngine):
    """PDF engine for Hanwool format water quality reports."""

    def extract_data(self, pdf_path: str, page_number: int) -> Dict[str, str]:
        """Extract data using Hanwool-specific parser."""
        return get_data_hanwool(pdf_path, page_number)

    def validate_pdf(self, pdf_path: str) -> bool:
        """Validate Hanwool format PDF."""
        # Add validation logic if needed
        return True

class Malgun_HwanGyungPDFEngine(PDFEngine):
    """PDF engine for Hanwool format water quality reports."""

    def extract_data(self, pdf_path: str, page_number: int) -> Dict[str, str]:
        """Extract data using Hanwool-specific parser."""
        return get_data_malgun_hwangyung(pdf_path, page_number)

    def validate_pdf(self, pdf_path: str) -> bool:
        """Validate Hanwool format PDF."""
        # Add validation logic if needed
        return True

class KiwiiPDFEngine(PDFEngine):
    """PDF engine for Hanwool format water quality reports."""

    def extract_data(self, pdf_path: str, page_number: int) -> Dict[str, str]:
        """Extract data using Hanwool-specific parser."""
        return get_data_kiwii(pdf_path, page_number)

    def validate_pdf(self, pdf_path: str) -> bool:
        """Validate Hanwool format PDF."""
        # Add validation logic if needed
        return True


class MalgeunmulPDFEngine(PDFEngine):
    """PDF engine for Hanwool format water quality reports."""

    def extract_data(self, pdf_path: str, page_number: int) -> Dict[str, str]:
        """Extract data using Hanwool-specific parser."""
        return get_data_malgeunmul(pdf_path, page_number)

    def validate_pdf(self, pdf_path: str) -> bool:
        """Validate Hanwool format PDF."""
        # Add validation logic if needed
        return True


class NurilifePDFEngine(PDFEngine):
    """PDF engine for Hanwool format water quality reports."""

    def extract_data(self, pdf_path: str, page_number: int) -> Dict[str, str]:
        """Extract data using Hanwool-specific parser."""
        return get_data_nurilife(pdf_path, page_number)

    def validate_pdf(self, pdf_path: str) -> bool:
        """Validate Hanwool format PDF."""
        # Add validation logic if needed
        return True


class PDFEngineFactory:
    """Factory for creating PDF engine instances."""

    _engines: Dict[PDFEngineType, type] = {
        PDFEngineType.HANWOOL: HanwoolPDFEngine,
        PDFEngineType.MALGUN_HWANGYUNG: Malgun_HwanGyungPDFEngine,
        PDFEngineType.KIWII: KiwiiPDFEngine,
        PDFEngineType.MALGEUNMUL: MalgeunmulPDFEngine,
        PDFEngineType.NURILIFE: NurilifePDFEngine,
        # Register future engines here
    }

    @classmethod
    def create_engine(cls, engine_type: PDFEngineType) -> PDFEngine:
        """
        Create a PDF engine instance.

        Args:
            engine_type: Type of engine to create

        Returns:
            PDFEngine instance

        Raises:
            ValueError: If engine type is not supported
        """
        engine_class = cls._engines.get(engine_type)
        if not engine_class:
            raise ValueError(f"Unsupported engine type: {engine_type}")
        return engine_class()

    @classmethod
    def register_engine(cls, engine_type: PDFEngineType, engine_class: type):
        """
        Register a new PDF engine.

        Args:
            engine_type: Type identifier for the engine
            engine_class: Engine class to register
        """
        if not issubclass(engine_class, PDFEngine):
            raise TypeError(f"{engine_class} must inherit from PDFEngine")
        cls._engines[engine_type] = engine_class


class WaterQualityData:
    """Container for water quality test results."""

    REQUIRED_FIELDS = [
        "General_bacteria", "Total_coliforms", "Fecal_coliforms", "Lead", "Fluoride",
        "Arsenic", "Selenium", "Mercury", "Cyanide", "Chromium", "Chloride_ion", "Ammonia_nitrogen",
        "Nitrate_nitrogen", "Cadmium", "Boron", "Phenol", "Diazinon", "Parathion", "Fenitrothion", "Carbaryl",
        "1,1,1-Trichloroethane", "Tetrachloroethylene", "Trichloroethylene", "Dichloromethane", "Benzene", "Toluene",
        "Ethylbenzene", "Xylene", "1,1-Dichloroethylene", "Carbon_tetrachloride", "1,2-Dibromo-3-chloropropane",
        "1,4-Dioxane", "Hardness", "Potassium_permanganate_consumption", "Odor", "Taste", "Copper", "Color",
        "Detergents", "pH", "Zinc", "Iron", "Manganese", "Turbidity", "Sulfate_ion", "Aluminum", "water_ok"
    ]

    def __init__(self, data: Dict[str, str]):
        """
        Initialize water quality data.

        Args:
            data: Dictionary containing water quality parameters
        """
        self._validate_data(data)

        self.general_bacteria = data['General_bacteria']        #일반세균
        self.total_coliform = data['Total_coliforms']            #총대장균군
        self.fecal_coliforms = data['Fecal_coliforms']          #대장균/분원성대장균군
        self.lead = data['Lead']                                #납
        self.fluoride = data['Fluoride']                        #불소
        self.arsenic = data['Arsenic']                          #비소
        self.selenium = data['Selenium']                        #세레늄
        self.mercury = data['Mercury']                          #수은
        self.cyanide = data['Cyanide']                          #시안
        self.chromium = data['Chromium']                        #크롬

        self.ammonia_nitrogen = data['Ammonia_nitrogen']        #암모니아성질소
        self.nitrate_nitrogen = data['Nitrate_nitrogen']        #질산성질소
        self.cadmium = data['Cadmium']                          #카드뮴
        self.boron = data['Boron']                              #붕소
        self.phenol = data['Phenol']                            #페놀

        self.diazinon = data['Diazinon']                        #다이아지논
        self.parathion = data['Parathion']                      #파라티논
        self.fenitrothion = data['Fenitrothion']                #페니트로티논
        self.carbaryl = data['Carbaryl']                        #카바릴

        self.trichloroethane = data['1,1,1-Trichloroethane']    #1,1,1-트리클로로에탄
        self.tetrachloroethylene = data['Tetrachloroethylene']  #테트라클로로에틸렌
        self.trichloroethylene = data['Trichloroethylene']      #트리클로로에틸렌
        self.dichloromethane = data['Dichloromethane']          #디클로로메탄

        self.benzene = data['Benzene']                          #벤젠
        self.toluene = data['Toluene']                          #톨루엔
        self.ethylbenzene = data['Ethylbenzene']                #에틸벤젠
        self.xylene = data['Xylene']                            #크실렌

        self.dichloroethylene = data['1,1-Dichloroethylene']                #1.1-디클로로에틸렌
        self.carbon_tetrachloride = data['Carbon_tetrachloride']            #사염화탄소
        self.dibromo_3_chloropropane = data['1,2-Dibromo-3-chloropropane']  #1.2-디브로모-3-클로로프로판
        self.dioxane = data['1,4-Dioxane']                                  #1.4-다이옥산

        self.hardness = data['Hardness']        #경도
        self.potassium_permanganate_consumption = data['Potassium_permanganate_consumption']  #과망간산칼륨소비량

        self.odor = data['Odor']                    #냄새
        self.taste = data['Taste']                  #맛
        self.copper = data['Copper']                #동
        self.color = data['Color']                  #색도

        self.detergents = data['Detergents']        #세제
        self.ph = data['pH']                        #수소이온농도

        self.zinc = data['Zinc']                    #아연
        self.chloride = data['Chloride_ion']        #염소이온
        self.iron = data['Iron']                    #철
        self.manganese = data['Manganese']          #망간
        self.turbidity = data['Turbidity']          #탁도
        self.sulfate_ion = data['Sulfate_ion']      #황산이온
        self.aluminum = data['Aluminum']            #알루미늄

        # Overall Result
        self.water_ok = data['water_ok']            #수질 적합, 부적합

    @classmethod
    def _validate_data(cls, data: Dict[str, str]):
        """Validate that all required fields are present."""
        missing = [field for field in cls.REQUIRED_FIELDS if field not in data]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")


class HWPDocumentWriter:
    """Handles HWP document creation and manipulation."""

    def __init__(self, template_path: str):
        """
        Initialize the HWP writer.

        Args:
            template_path: Path to the HWP template file
        """
        self.template_path = Path(template_path)
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

    def write_field(self, hwp: Hwp, field_name: str, value: str):
        """
        Write data to a field in the HWP document.

        Args:
            hwp: Hwp instance
            field_name: Name of the field placeholder
            value: Value to write
        """
        hwp.MoveToField(field_name)
        hwp.PutFieldText(field_name, str(value))

    def create_document(self, well_id: str, water_data: WaterQualityData,
                        output_path: str) -> Path:
        """
        Create a water quality report document.

        Args:
            well_id: Well identifier (e.g., 'W-1')
            water_data: Water quality test data
            output_path: Path to save the output file

        Returns:
            Path to the created document
        """
        hwp = Hwp(visible=False)
        hwp.open(str(self.template_path))

        try:
            # Extract well index number
            well_index = self._extract_number(well_id)

            # Write well information
            self.write_field(hwp, 'index', str(well_index) if well_index else '')
            self.write_field(hwp, 'well', well_id)

            # Write microbiological data
            self.write_field(hwp, 'general_bacteria', water_data.general_bacteria)
            self.write_field(hwp, 'total_coliform', water_data.total_coliform)
            self.write_field(hwp, 'fecal_coliforms', water_data.fecal_coliforms)

            self.write_field(hwp, 'lead', water_data.lead)
            self.write_field(hwp, 'fluoride', water_data.fluoride)
            self.write_field(hwp, 'arsenic', water_data.arsenic)
            self.write_field(hwp, 'selenium', water_data.selenium)
            self.write_field(hwp, 'mercury', water_data.mercury)
            self.write_field(hwp, 'cyanide', water_data.cyanide)
            self.write_field(hwp, 'chromium', water_data.chromium)

            self.write_field(hwp, 'ammonia_nitrogen', water_data.ammonia_nitrogen)
            self.write_field(hwp, 'nitrate_nitrogen', water_data.nitrate_nitrogen)
            self.write_field(hwp, 'cadmium', water_data.cadmium)


            self.write_field(hwp, 'boron', water_data.boron)
            self.write_field(hwp, 'phenol', water_data.phenol)
            self.write_field(hwp, 'diazinon', water_data.diazinon)
            self.write_field(hwp, 'parathion', water_data.parathion)
            self.write_field(hwp, 'fenitrothion', water_data.fenitrothion)
            self.write_field(hwp, 'carbaryl', water_data.carbaryl)


            self.write_field(hwp, 'trichloroethane', water_data.trichloroethane)
            self.write_field(hwp, 'tetrachloroethylene', water_data.tetrachloroethylene)
            self.write_field(hwp, 'trichloroethylene', water_data.trichloroethylene)
            self.write_field(hwp, 'dichloromethane', water_data.dichloromethane)

            self.write_field(hwp, 'benzene', water_data.benzene)
            self.write_field(hwp, 'toluene', water_data.toluene)
            self.write_field(hwp, 'ethylbenzene', water_data.ethylbenzene)
            self.write_field(hwp, 'xylene', water_data.xylene)


            self.write_field(hwp, 'dichloroethylene', water_data.dichloroethylene)
            self.write_field(hwp, 'carbon_tetrachloride', water_data.carbon_tetrachloride)
            self.write_field(hwp, 'dibromo_3_chloropropane', water_data.dibromo_3_chloropropane)
            self.write_field(hwp, 'dioxane', water_data.dioxane)

            self.write_field(hwp, 'hardness', water_data.hardness)
            self.write_field(hwp, 'potassium_permanganate_consumption', water_data.potassium_permanganate_consumption)
            self.write_field(hwp, 'odor', water_data.odor)
            self.write_field(hwp, 'taste', water_data.taste)
            self.write_field(hwp, 'copper', water_data.copper)
            self.write_field(hwp, 'color', water_data.color)
            self.write_field(hwp, 'detergents', water_data.detergents)
            self.write_field(hwp, 'color', water_data.color)


            # Write physical/chemical data
            self.write_field(hwp, 'ph', water_data.ph)
            self.write_field(hwp, 'zinc', water_data.zinc)
            self.write_field(hwp, 'chloride', water_data.chloride)
            self.write_field(hwp, 'iron', water_data.iron)
            self.write_field(hwp, 'manganese', water_data.manganese)
            self.write_field(hwp, 'turbidity', water_data.turbidity)
            self.write_field(hwp, 'sulfate_ion', water_data.sulfate_ion)
            self.write_field(hwp, 'aluminum', water_data.aluminum)

            # Write overall result
            self.write_field(hwp, 'water_ok', water_data.water_ok)

            # Save document
            output_file = Path(output_path)
            hwp.save_as(str(output_file))

            return output_file

        finally:
            hwp.Quit(save=False)

    @staticmethod
    def _extract_number(text: str) -> Optional[int]:
        """
        Extract the first continuous sequence of digits from text.

        Args:
            text: String to search (e.g., 'W-20', 'item_34b')

        Returns:
            Extracted number as integer, or None if no digits found
        """
        match = re.search(r'\d+', text)
        return int(match.group(0)) if match else None


class WaterQualityProcessor:
    """Main processor for water quality reports."""

    def __init__(self,
                 engine_type: PDFEngineType = PDFEngineType.HANWOOL,
                 template_path: str = r"c:\Program Files\totalcmd\hwp\wt_dringking46.hwp",
                 output_dir: str = r"d:\05_Send"):
        """
        Initialize the processor.

        Args:
            engine_type: PDF parsing engine to use
            template_path: Path to HWP template
            output_dir: Directory for output files
        """
        self.engine = PDFEngineFactory.create_engine(engine_type)
        self.writer = HWPDocumentWriter(template_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process_pdf(self, pdf_path: str) -> List[Path]:
        """
        Process a water quality PDF and generate HWP reports.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            List of paths to generated HWP documents
        """
        # Validate PDF
        if not self.engine.validate_pdf(pdf_path):
            raise ValueError(f"PDF is not compatible with selected engine: {pdf_path}")

        # Get page count
        doc = pymupdf.open(pdf_path)
        page_count = len(doc)
        doc.close()

        # Process each page
        generated_files = []
        for page_num in range(1, page_count + 1):
            print(f"Processing page {page_num}/{page_count}...")

            # Extract data
            raw_data = self.engine.extract_data(pdf_path, page_num)
            water_data = WaterQualityData(raw_data)

            # Generate well ID
            well_id = f"W-{page_num}"

            # Create document
            output_path = self.output_dir / f"ex_dringking_{well_id}.hwp"
            created_file = self.writer.create_document(well_id, water_data, str(output_path))
            generated_files.append(created_file)

            print(f"  Well {well_id}: Water Status = {water_data.water_ok}")
            print("=" * 100)

        return generated_files

    def process_and_merge(self, pdf_path: str) -> Path:
        """
        Process PDF and merge all generated HWP files.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Path to the merged document
        """
        # Generate individual documents
        self.process_pdf(pdf_path)

        # Merge documents
        print("\nMerging HWP files...")
        merged_path = merge_hwp_files()
        print(f"Merged document created: {merged_path}")

        return merged_path


def main(engine):
    """Main entry point."""
    # Find PDF files
    fb = FileBase()
    pdf_files = fb.get_file_filter(".", "*.pdf")

    if not pdf_files:
        print("No PDF files found in current directory")
        return

    pdf_path = pdf_files[0]
    print(f"Processing PDF: {pdf_path}\n")

    template_path = TEMPLATE_DIR / HWP_TEMPLATE
    output_dir = BASE_DIR

    # processor = WaterQualityProcessor(
    #     # engine_type=PDFEngineType.HANWOOL
    #     # engine_type=PDFEngineType.KIWII
    #     # engine_type=PDFEngineType.MALGEUNMUL
    #     # engine_type=PDFEngineType.NURILIFE
    # )

    processor = WaterQualityProcessor(engine_type=engine)

    # Process and merge
    processor.process_and_merge(pdf_path)

    print("\nProcessing completed successfully!")


def display_menu(engine_enum: type[enum.Enum]) -> None:
    """Displays the console menu options based on the Enum."""
    print("\n--- PDF Engine Selection Menu ---")

    # Iterate through the enum members to display options
    for i, member in enumerate(engine_enum):
        # We use i+1 as the menu number
        # We use member.value to show the user-friendly string
        print(f"[{i + 1}] Select: {member.value.upper()}")

    # Add the exit option
    print("[0] Exit")
    print("-" * 35)


def get_user_choice(max_options: int) -> Optional[int]:
    """Prompts the user for a choice and validates the input."""
    while True:
        try:
            choice_str = input("Enter your choice (0 to {}): ".format(max_options))

            # Check for empty input (e.g., just pressing Enter)
            if not choice_str.strip():
                print("Input cannot be empty. Please enter a number.")
                continue

            choice = int(choice_str)

            # Validate the choice range
            if 0 <= choice <= max_options:
                return choice
            else:
                print(f"Invalid choice. Please enter a number between 0 and {max_options}.")

        except ValueError:
            print("Invalid input. Please enter a number.")


def run_menu():
    """Main function to run the interactive menu."""

    # Get all members of the enum
    engine_members = list(PDFEngineType)
    num_options = len(engine_members)

    while True:
        display_menu(PDFEngineType)
        choice = get_user_choice(num_options)

        if choice is None:
            # Should not happen if get_user_choice is robust, but kept for safety
            continue

        if choice == 0:
            print("\nExiting PDF Engine Selector. Goodbye!")
            # Exit the program gracefully
            sys.exit(0)
        else:
            # Map the numerical choice back to the Enum member
            # Choice 1 maps to index 0, 2 maps to index 1, etc.
            try:
                selected_engine = engine_members[choice - 1]

                # --- Simulated Action ---
                print(f"\n--- ACTION ---")
                print(f"You selected engine: {selected_engine.name} ({selected_engine.value})")

                main(selected_engine)
                # Here is where you would call the function to initialize the parser
                # Example: initialize_parser(selected_engine)

                print("Engine parser initialized successfully!")
                print("--------------\n")

            except IndexError:
                # This block should ideally not be reached if validation in get_user_choice is correct
                print("An internal error occurred: Invalid option index.")


if __name__ == "__main__":
    # main()
    run_menu()
    terminate_all_hwp()


