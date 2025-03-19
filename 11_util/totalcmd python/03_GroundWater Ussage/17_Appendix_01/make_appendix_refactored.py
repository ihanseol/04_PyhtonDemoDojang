import pandas as pd
import os
from pathlib import Path


class WellData:
    """Class to handle well data storage and calculations."""
    
    def __init__(self):
        """Initialize well data attributes."""
        self.data = {}
        self.derived_values = {
            "well_d3": 0,
            "migogyul": 0,
            "migogyul_1": 0,
            "migogyul_2": 0,
            "rest_height": 0
        }
        
    def set_data(self, gong, title, address, q, natural, stable, simdo, well_diameter, casing, bedrock):
        """Store well data and calculate derived values."""
        # Store base data
        self.data = {
            "gong": gong,
            "title": title,
            "address": address,
            "q": q,
            "natural": natural,
            "stable": stable,
            "simdo": simdo,
            "simdo1": simdo,  # Duplicate for output format
            "casing": casing,
            "well_diameter": well_diameter,
            "bedrock": bedrock
        }
        
        # Calculate derived values
        self._calculate_derived_values(well_diameter, casing, simdo)
        
    def _calculate_derived_values(self, well_diameter, casing, simdo):
        """Calculate derived values based on well specifications."""
        self.derived_values["well_d3"] = well_diameter + 100
        self.derived_values["migogyul"] = casing - 1
        self.derived_values["migogyul_1"] = casing - 1
        self.derived_values["migogyul_2"] = casing - 1
        self.derived_values["rest_height"] = simdo - casing
        
    def get_all_data(self):
        """Return combined dictionary of base and derived data."""
        return {**self.data, **self.derived_values}
        
    def print_data(self):
        """Print all well data for debugging."""
        print("Well Data:")
        
        # Print base data
        for key, value in self.data.items():
            print(f"{key}: {value}")
            
        # Print derived values
        for key, value in self.derived_values.items():
            print(f"{key}: {value}")


class AppendixMaker:
    """Class to process well data and generate appendix output."""
    
    # Define column names as class constants
    INPUT_COLUMNS = [
        'gong', 'Project Name', 'address', 'q', 'natural', 
        'stable', 'simdo', 'well_diameter', 'casing', 'bedrock'
    ]
    
    OUTPUT_COLUMNS = [
        'gong', 'title', 'address', 'q', 'natural', 'stable', 
        'simdo', 'simdo1', 'casing', 'welld1', 'welld2', 'welld3', 
        'migogyul', 'migogyul_1', 'migogyul_2', 'rest_height', 'bedrock'
    ]
    
    def __init__(self, base_dir=None):
        """Initialize the AppendixMaker with file paths and data structures."""
        self.base_dir = Path(base_dir) if base_dir else Path("d:/05_Send")
        self.input_file = "YanSoo_Spec.xlsx"
        self.output_file = "appendix_01.xlsx"
        self.input_data = None
        self.output_data = None
        self.well_processor = WellData()
        
    def get_input_path(self):
        """Get the full path to the input file."""
        return self.base_dir / self.input_file
        
    def get_output_path(self):
        """Get the full path to the output file."""
        return self.base_dir / self.output_file
    
    def validate_input_data(self):
        """Validate that input data has all required columns."""
        if self.input_data is None:
            return False
            
        missing_columns = [col for col in self.INPUT_COLUMNS if col not in self.input_data.columns]
        if missing_columns:
            print(f"Error: Input file is missing required columns: {', '.join(missing_columns)}")
            return False
            
        return True
    
    def initialize_output_data(self):
        """Initialize or load existing output data."""
        try:
            output_path = self.get_output_path()
            if output_path.exists():
                self.output_data = pd.read_excel(output_path)
                return True
        except Exception as e:
            print(f"Could not load existing output file: {str(e)}")
        
        # If loading fails or file doesn't exist, create new DataFrame
        self.output_data = pd.DataFrame(columns=self.OUTPUT_COLUMNS)
        return True
    
    def clear_output_data(self):
        """Clear existing output data and create empty output file."""
        self.output_data = pd.DataFrame(columns=self.OUTPUT_COLUMNS)
        
        try:
            self.output_data.to_excel(self.get_output_path(), index=False)
            print("Output Excel file cleared successfully.")
            return True
        except Exception as e:
            print(f"Error clearing output Excel file: {str(e)}")
            return False
    
    def load_input_data(self):
        """Load data from input Excel file."""
        try:
            self.input_data = pd.read_excel(self.get_input_path())
            return self.validate_input_data()
        except FileNotFoundError:
            print(f"Error: Input XLSX file not found at {self.get_input_path()}")
            return False
        except Exception as e:
            print(f"Error loading input data: {str(e)}")
            return False
    
    def process_row(self, row):
        """Process a single row of input data and return output row."""
        # Format address with gong number
        address = f"{row['address']}({row['gong']})"
        
        # Set well data and calculate derived attributes
        self.well_processor.set_data(
            row['gong'], 
            row['Project Name'], 
            address,
            row['q'], 
            row['natural'], 
            row['stable'], 
            row['simdo'], 
            row['well_diameter'], 
            row['casing'],
            row['bedrock']
        )
        
        # Print debug information
        self.well_processor.print_data()
        print("-" * 80)
        
        # Prepare output row
        derived_data = self.well_processor.derived_values
        
        return {
            'gong': row['gong'],
            'title': row['Project Name'],
            'address': address,
            'q': row['q'],
            'natural': row['natural'],
            'stable': row['stable'],
            'simdo': row['simdo'],
            'simdo1': row['simdo'],
            'casing': row['casing'],
            'welld1': row['well_diameter'],
            'welld2': row['well_diameter'],
            'welld3': derived_data["well_d3"],
            'migogyul': derived_data["migogyul"],
            'migogyul_1': derived_data["migogyul_1"],
            'migogyul_2': derived_data["migogyul_2"],
            'rest_height': derived_data["rest_height"],
            'bedrock': row['bedrock']
        }
    
    def process_data(self):
        """Process all rows in the input data."""
        if self.input_data is None:
            return False
        
        output_rows = []
        
        # Process each row using pandas iterrows for better performance
        for _, row in self.input_data.iterrows():
            output_row = self.process_row(row)
            output_rows.append(output_row)
        
        # Add new data to output
        new_data_df = pd.DataFrame(output_rows)
        self.output_data = pd.concat([self.output_data, new_data_df], ignore_index=True)
        return True
    
    def save_output_data(self):
        """Save output data to Excel file."""
        try:
            self.output_data.to_excel(self.get_output_path(), index=False)
            print(f"Processing complete. Output saved to {self.output_file}.")
            return True
        except Exception as e:
            print(f"Error saving output Excel file: {str(e)}")
            return False
    
    def run(self):
        """Execute the complete data processing workflow."""
        # Step 1: Load input data
        if not self.load_input_data():
            return "Failed to load input data."
        
        # Step 2: Clear and initialize output data
        if not self.clear_output_data():
            return "Failed to clear output data."
        
        if not self.initialize_output_data():
            return "Failed to initialize output data."
        
        # Step 3: Process data
        if not self.process_data():
            return "Failed to process data."
        
        # Step 4: Save output data
        if not self.save_output_data():
            return "Failed to save output data."
        
        return "Processing completed successfully."


# Example usage
if __name__ == "__main__":
    appendix_maker = AppendixMaker()
    result = appendix_maker.run()
    print(result)
