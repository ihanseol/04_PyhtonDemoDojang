import pandas as pd
import os
from pathlib import Path


class WellData:
    """
     Class to handle well data storage and processing.
     2025/07/03
     집수정 우물직경 1700미리 추가해줌 ....
    """
    
    DIAMETER_MAPPING = {
        150: '6″',
        200: '8″',
        250: '10″'
    }
    
    def __init__(self):
        self.data = {}
        
    def set_data(self, gong, title, address, natural, simdo, well_diameter, casing):
        """Store well data with normalized diameter value."""
        self.data = {
            "gong": gong,
            "title": title,
            "address": address,
            "natural": natural,
            "simdo": simdo,
            "casing": casing,
            "well_diameter": self.normalize_diameter(well_diameter)
        }
        
    def normalize_diameter(self, diameter):
        """Convert diameter to standard value."""
        return self.DIAMETER_MAPPING.get(diameter, str(diameter) + 'mm')
        
    def print_data(self):
        """Print all well data."""
        print("Well Data:")
        for key, value in self.data.items():
            print(f"{key}: {value}")
            
    def to_dict(self):
        """Return well data as dictionary."""
        return self.data


class AppendixMaker:
    """Class to process input Excel files and generate appendix output."""
    
    def __init__(self, base_dir=None):
        self.base_dir = base_dir or Path("d:/05_Send")
        self.input_file = "YanSoo_Spec.xlsx"
        self.output_file = "appendix_06.xlsx"
        self.input_data = None
        self.output_data = None
        self.required_columns = [
            'gong', 'Project Name', 'address', 'natural', 
            'simdo', 'well_diameter', 'casing'
        ]
        self.output_columns = [
            'gong', 'title', 'address', 'natural', 
            'simdo', 'casing', 'well_diameter'
        ]
        
    def get_input_path(self):
        """Get the full path to the input file."""
        return self.base_dir / self.input_file
        
    def get_output_path(self):
        """Get the full path to the output file."""
        return self.base_dir / self.output_file
        
    def load_input_data(self):
        """Load data from input Excel file."""
        try:
            input_path = self.get_input_path()
            self.input_data = pd.read_excel(input_path)
            return True
        except FileNotFoundError:
            print(f"Error: Input file '{input_path}' not found.")
            return False
        except Exception as e:
            print(f"Error loading input data: {str(e)}")
            return False
            
    def validate_input_data(self):
        """Validate that input data has required columns."""
        if self.input_data is None:
            return False
            
        missing_columns = [col for col in self.required_columns if col not in self.input_data.columns]
        if missing_columns:
            print(f"Error: Input file is missing required columns: {', '.join(missing_columns)}")
            return False
            
        return True
        
    def initialize_output_data(self):
        """Initialize output DataFrame with required columns."""
        self.output_data = pd.DataFrame(columns=self.output_columns)
        
    def load_existing_output(self):
        """Load existing output file if it exists."""
        try:
            output_path = self.get_output_path()
            if output_path.exists():
                self.output_data = pd.read_excel(output_path)
                return True
        except Exception as e:
            print(f"Error loading existing output file: {str(e)}")
        
        # If output file doesn't exist or there was an error, initialize a new DataFrame
        self.initialize_output_data()
        return False
        
    def save_output_data(self):
        """Save output data to Excel file."""
        try:
            output_path = self.get_output_path()
            self.output_data.to_excel(output_path, index=False)
            print(f"Output saved to {output_path}")
            return True
        except Exception as e:
            print(f"Error saving output: {str(e)}")
            return False
            
    @staticmethod
    def process_row(row):
        """Process a single row of input data."""
        well_data = WellData()
        
        # Extract data from row
        gong = row['gong']
        title = row['Project Name']
        address = f"{row['address']}({gong})"
        natural = row['natural']
        simdo = row['simdo']
        well_diameter = row['well_diameter']
        casing = row['casing']
        
        # Set well data and normalize values
        well_data.set_data(gong, title, address, natural, simdo, well_diameter, casing)
        well_data.print_data()
        print("-" * 80)
        
        return well_data.to_dict()
        
    def process_data(self):
        """Process all rows in the input data."""
        if self.input_data is None or self.output_data is None:
            return False
            
        output_rows = []
        for _, row in self.input_data.iterrows():
            processed_row = self.process_row(row)
            output_rows.append(processed_row)
            
        # Add new rows to output data
        new_data = pd.DataFrame(output_rows)
        # self.output_data = pd.concat([self.output_data, new_data], ignore_index=True)
        self.output_data = pd.concat([new_data], ignore_index=True)
        return True
        
    def run(self):
        """Execute the full process."""
        # Load and validate input data
        if not self.load_input_data() or not self.validate_input_data():
            return "Error: Could not load or validate input data."
            
        # Initialize output data
        self.load_existing_output()
        
        # Process data
        if not self.process_data():
            return "Error: Failed to process data."
            
        # Save output
        if not self.save_output_data():
            return "Error: Failed to save output data."
            
        return "Processing complete. Output saved successfully."


# Example usage
if __name__ == "__main__":
    appendix_maker = AppendixMaker()
    result = appendix_maker.run()
    print(result)
