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
from typing import Optional

from merge_hwp_files import merge_hwp_files
from FileManger_V0_20250406 import FileBase

from pdf_dringking60_engine import get_data_hanwool
from pdf_dringking60_engine import get_data_kiwii
from pdf_dringking60_engine import get_data_malgeunmul
from pdf_dringking60_engine import get_data_nurilife

BASE_DIR = Path("d:/05_Send")
TEMPLATE_DIR = Path("c:/Program Files/totalcmd/hwp")
HWP_TEMPLATE = "wt_dringking60.hwp"


class PDFEngineType(Enum):
    """Supported PDF parsing engines."""
    HANWOOL = "hanwool"
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
        "General_Bacteria",
        "Total_Coliforms",
        "Fecal_Coliform",
        "Lead",
        "Fluoride",
        "Arsenic",
        "Selenium",
        "Mercury",
        "Cyanide",
        "Chromium",
        "Chloride_Ion",
        "Ammonia_Nitrogen",
        "Nitrate_Nitrogen",
        "Cadmium",
        "Boron",
        "Phenol",
        "Diazinon",
        "Fenitrothion",
        "Parathion",
        "Carbaryl",
        "1,1,1-Trichloroethane",
        "Tetrachloroethylene",
        "Trichloroethylene",
        "Dichloromethane",
        "Benzene",
        "Toluene",
        "Ethylbenzene",
        "Xylene",
        "1,1-Dichloroethylene",
        "Carbon_Tetrachloride",
        "1,2-Dibromo-3-chloropropane",
        "Free_Residual_Chlorine",
        "Dibromochloromethane",
        "Bromodichloromethane",
        "Total_Trihalomethanes",
        "Chloroform",
        "Trichloroacetonitrile",
        "Chloral_Hydrate",
        "Dichloroacetonitrile",
        "Dibromoacetonitrile",
        "Haloacetic_Acids",
        "Hardness",
        "Potassium_Permanganate_Consumption",
        "Odor",
        "Taste",
        "Copper",
        "Color",
        "Detergents",
        "pH",
        "Zinc",
        "Evaporation_Residue",
        "Iron",
        "Manganese",
        "Turbidity",
        "Sulfate_Ion",
        "Aluminum",
        "1,4-Dioxane",
        "Formaldehyde",
        "Bromate",
        "Uranium",
        "water_ok"
    ]

    def __init__(self, data: Dict[str, str]):
        """
        Initialize water quality data.

        Args:
            data: Dictionary containing water quality parameters
        """
        self._validate_data(data)

        self.General_Bacteria = data['General_Bacteria']        #일반세균
        self.Total_Coliforms = data['Total_Coliforms']            #총대장균군
        self.Fecal_Coliform = data['Fecal_Coliform']          #대장균/분원성대장균군
        self.Lead = data['Lead']                                #납
        self.Fluoride = data['Fluoride']                        #불소
        self.Arsenic = data['Arsenic']                          #비소
        self.Selenium = data['Selenium']                        #세레늄
        self.Mercury = data['Mercury']                          #수은
        self.Cyanide = data['Cyanide']                          #시안
        self.Chromium = data['Chromium']                        #크롬
        self.Chloride_Ion = data['Chloride_Ion']                        #크롬

        self.Ammonia_Nitrogen = data['Ammonia_Nitrogen']        #암모니아성질소
        self.Nitrate_Nitrogen = data['Nitrate_Nitrogen']        #질산성질소
        self.Cadmium = data['Cadmium']                          #카드뮴
        self.Boron = data['Boron']                              #붕소
        self.Phenol = data['Phenol']                            #페놀

        self.Diazinon = data['Diazinon']                        #다이아지논
        self.Parathion = data['Parathion']                      #파라티논
        self.Fenitrothion = data['Fenitrothion']                #페니트로티논
        self.Carbaryl = data['Carbaryl']                        #카바릴

        self.Trichloroethane = data['1,1,1-Trichloroethane']    #1,1,1-트리클로로에탄
        self.Tetrachloroethylene = data['Tetrachloroethylene']  #테트라클로로에틸렌
        self.Trichloroethylene = data['Trichloroethylene']      #트리클로로에틸렌
        self.Dichloromethane = data['Dichloromethane']          #디클로로메탄

        self.Benzene = data['Benzene']                          #벤젠
        self.Toluene = data['Toluene']                          #톨루엔
        self.Ethylbenzene = data['Ethylbenzene']                #에틸벤젠
        self.Xylene = data['Xylene']                            #크실렌

        self.Dichloroethylene = data['1,1-Dichloroethylene']                #1.1-디클로로에틸렌
        self.Carbon_Tetrachloride = data['Carbon_Tetrachloride']            #사염화탄소
        self.Dibromo_3_chloropropane = data['1,2-Dibromo-3-chloropropane']  #1.2-디브로모-3-클로로프로판



        self.Free_Residual_Chlorine = data['Free_Residual_Chlorine']    #유리잔류염소
        self.Dibromochloromethane = data['Dibromochloromethane']    # 디브로모클로로메탄
        self.Bromodichloromethane = data['Bromodichloromethane']    #브로로디클로로메탄
        self.Total_Trihalomethanes = data['Total_Trihalomethanes']  #총트리할로메탄
        self.Chloroform = data['Chloroform']    #클로로포름


        self.Trichloroacetonitrile = data['Trichloroacetonitrile']      #트리클로로아세토니트릴
        self.Chloral_Hydrate = data['Chloral_Hydrate']                  #클로랄하이드레이트
        self.Dichloroacetonitrile = data['Dichloroacetonitrile']        #디클로로아세토니트릴
        self.Dibromoacetonitrile = data['Dibromoacetonitrile']        #디클로로아세토니트릴


        self.Haloacetic_Acids = data['Haloacetic_Acids']                #할로아세틱에시드
        self.Hardness = data['Hardness']                                #경도
        self.Potassium_Permanganate_Consumption = data['Potassium_Permanganate_Consumption']        #과망간산칼륨소비량


        self.Odor = data['Odor']                #냄새
        self.Taste = data['Taste']              #맛
        self.Copper = data['Copper']                  #색도
        self.Color = data['Color']                  #색도
        self.Detergents = data['Detergents']        #세제
        self.pH = data['pH']                        #수소이온농도
        self.Zinc = data['Zinc']                    #아연
        self.Evaporation_Residue = data['Evaporation_Residue']
        self.Iron = data['Iron']                    #철
        self.Manganese = data['Manganese']          #망간
        self.Turbidity = data['Turbidity']          #탁도

        self.Sulfate_Ion = data['Sulfate_Ion']      #황산이온
        self.Aluminum = data['Aluminum']            #알루미늄
        self.Dioxane = data['1,4-Dioxane']          #1,4다이옥신
        self.Formaldehyde = data['Formaldehyde']

        self.Bromate = data['Bromate']
        self.Uranium = data['Uranium']

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
            self.write_field(hwp, 'General_Bacteria', water_data.General_Bacteria)
            self.write_field(hwp, 'Total_Coliforms', water_data.Total_Coliforms)
            self.write_field(hwp, 'Fecal_Coliform', water_data.Fecal_Coliform)

            self.write_field(hwp, 'Lead', water_data.Lead)
            self.write_field(hwp, 'Fluoride', water_data.Fluoride)
            self.write_field(hwp, 'Arsenic', water_data.Arsenic)
            self.write_field(hwp, 'Selenium', water_data.Selenium)
            self.write_field(hwp, 'Mercury', water_data.Mercury)
            self.write_field(hwp, 'Cyanide', water_data.Cyanide)
            self.write_field(hwp, 'Chromium', water_data.Chromium)
            self.write_field(hwp, 'Chloride_Ion', water_data.Chloride_Ion)

            self.write_field(hwp, 'Ammonia_Nitrogen', water_data.Ammonia_Nitrogen)
            self.write_field(hwp, 'Nitrate_Nitrogen', water_data.Nitrate_Nitrogen)
            self.write_field(hwp, 'Cadmium', water_data.Cadmium)


            self.write_field(hwp, 'Boron', water_data.Boron)
            self.write_field(hwp, 'Phenol', water_data.Phenol)
            self.write_field(hwp, 'Diazinon', water_data.Diazinon)
            self.write_field(hwp, 'Fenitrothion', water_data.Fenitrothion)


            self.write_field(hwp, 'Parathion', water_data.Parathion)
            self.write_field(hwp, 'Carbaryl', water_data.Carbaryl)


            self.write_field(hwp, 'Trichloroethane', water_data.Trichloroethane)
            self.write_field(hwp, 'Tetrachloroethylene', water_data.Tetrachloroethylene)
            self.write_field(hwp, 'Trichloroethylene', water_data.Trichloroethylene)
            self.write_field(hwp, 'Dichloromethane', water_data.Dichloromethane)

            self.write_field(hwp, 'Benzene', water_data.Benzene)
            self.write_field(hwp, 'Toluene', water_data.Toluene)
            self.write_field(hwp, 'Ethylbenzene', water_data.Ethylbenzene)
            self.write_field(hwp, 'Xylene', water_data.Xylene)


            self.write_field(hwp, 'Dichloroethylene', water_data.Dichloroethylene)
            self.write_field(hwp, 'Carbon_Tetrachloride', water_data.Carbon_Tetrachloride)
            self.write_field(hwp, 'Dibromo_3_chloropropane', water_data.Dibromo_3_chloropropane)


            self.write_field(hwp, 'Free_Residual_Chlorine', water_data.Free_Residual_Chlorine)
            self.write_field(hwp, 'Dibromochloromethane', water_data.Dibromochloromethane)
            self.write_field(hwp, 'Bromodichloromethane', water_data.Bromodichloromethane)
            self.write_field(hwp, 'Total_Trihalomethanes', water_data.Total_Trihalomethanes)
            self.write_field(hwp, 'Chloroform', water_data.Chloroform)
            self.write_field(hwp, 'Trichloroacetonitrile', water_data.Trichloroacetonitrile)
            self.write_field(hwp, 'Chloral_Hydrate', water_data.Chloral_Hydrate)
            self.write_field(hwp, 'Dichloroacetonitrile', water_data.Dichloroacetonitrile)
            self.write_field(hwp, 'Dibromoacetonitrile', water_data.Dibromoacetonitrile)
            self.write_field(hwp, 'Haloacetic_Acids', water_data.Haloacetic_Acids)
            self.write_field(hwp, 'Dioxane', water_data.Dioxane)
            self.write_field(hwp, 'Hardness', water_data.Hardness)
            self.write_field(hwp, 'Potassium_Permanganate_Consumption', water_data.Potassium_Permanganate_Consumption)

            self.write_field(hwp, 'Odor', water_data.Odor)
            self.write_field(hwp, 'Taste', water_data.Taste)
            self.write_field(hwp, 'Copper', water_data.Copper)
            self.write_field(hwp, 'Color', water_data.Color)
            self.write_field(hwp, 'Detergents', water_data.Detergents)
            self.write_field(hwp, 'pH', water_data.pH)


            # Write physical/chemical data
            self.write_field(hwp, 'Zinc', water_data.Zinc)
            self.write_field(hwp, 'Evaporation_Residue', water_data.Evaporation_Residue)
            self.write_field(hwp, 'Iron', water_data.Iron)
            self.write_field(hwp, 'Manganese', water_data.Manganese)
            self.write_field(hwp, 'Turbidity', water_data.Turbidity)
            self.write_field(hwp, 'Sulfate_Ion', water_data.Sulfate_Ion)
            self.write_field(hwp, 'Aluminum', water_data.Aluminum)
            self.write_field(hwp, 'Formaldehyde', water_data.Formaldehyde)
            self.write_field(hwp, 'Bromate', water_data.Bromate)
            self.write_field(hwp, 'Uranium', water_data.Uranium)

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
                 template_path: str = r"c:\Program Files\totalcmd\hwp\wt_dringking60.hwp",
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
            output_path = self.output_dir / f"ex_dringking60_{well_id}.hwp"
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
