import pandas as pd


class WellData:
    def __init__(self):
        self.well_dict = {}

    def set_welldata(self, gong, title, address, natural, simdo, well_diameter, casing):
        # Store the basic well data
        match well_diameter:
            case 150:
                well_diameter = 6
            case 200:
                well_diameter = 8
            case 250:
                well_diameter = 10
            case _:
                well_diameter = 8

        self.well_dict = {
            "gong": gong,
            "title": title,
            "address": address,
            "natural": natural,
            "simdo": simdo,
            "casing": casing,
            "well_diameter": well_diameter
        }

    def print_well_dict(self):
        print("Well Data:")
        for key, value in self.well_dict.items():
            print(f"{key}: {value}")


class AppendixMaker:
    def __init__(self):
        self.XL_INPUT = "YanSoo_Spec.xlsx"
        self.XL_OUTPUT = "appendix_06.xlsx"
        self.XL_BASE = "d:\\05_Send"
        self.excel_in = pd.DataFrame()
        self.excel_out = pd.DataFrame()
        self.wd = WellData()

    def clear_output_data(self):
        output_columns = ['gong', 'title', 'address', 'natural', 'simdo', 'casing', 'well_diameter']
        self.excel_out = pd.DataFrame(columns=output_columns)

        try:
            self.excel_out.to_excel(f"{self.XL_BASE}\\{self.XL_OUTPUT}", index=False)
            print("Output Excel file cleared successfully.")
        except Exception as e:
            print(f"Error clearing output Excel file: {str(e)}")

    def initial_work(self):
        try:
            self.excel_in = pd.read_excel(f"{self.XL_BASE}\\{self.XL_INPUT}")
        except FileNotFoundError:
            return "Error: Input XLSX file must be located in your d:\\05_Send folder ..."

        required_columns = ['gong', 'Project Name', 'address', 'natural', 'simdo', 'well_diameter', 'casing']
        if not all(col in self.excel_in.columns for col in required_columns):
            return "Error: Input Excel file is missing required columns."

        self.clear_output_data()

        try:
            self.excel_out = pd.read_excel(f"{self.XL_BASE}\\{self.XL_OUTPUT}")
        except FileNotFoundError:
            output_columns = ['gong', 'title', 'address', 'natural', 'simdo', 'casing', 'well_diameter']
            self.excel_out = pd.DataFrame(columns=output_columns)

        # Process each row in excel_in
        output_data = []
        for i, gong in enumerate(self.excel_in['gong']):
            # Extract data from excel_in
            igong = self.excel_in.iloc[i, self.excel_in.columns.get_loc('gong')]
            ititle = self.excel_in.iloc[i, self.excel_in.columns.get_loc('Project Name')]
            iaddress = self.excel_in.iloc[i, self.excel_in.columns.get_loc('address')] + f'({igong})'
            inatural = self.excel_in.iloc[i, self.excel_in.columns.get_loc('natural')]
            isimdo = self.excel_in.iloc[i, self.excel_in.columns.get_loc('simdo')]
            iwell_diameter = self.excel_in.iloc[i, self.excel_in.columns.get_loc('well_diameter')]
            icasing = self.excel_in.iloc[i, self.excel_in.columns.get_loc('casing')]

            # Set well data and calculate derived attributes
            self.wd.set_welldata(igong, ititle, iaddress, inatural, isimdo, iwell_diameter, icasing)
            self.wd.print_well_dict()

            match iwell_diameter:
                case 150:
                    iwell_diameter = 6
                case 200:
                    iwell_diameter = 8
                case 250:
                    iwell_diameter = 10
                case _:
                    iwell_diameter = 8

            print("-" * 80)

            output_data.append({
                'gong': igong,
                'title': ititle,
                'address': iaddress,
                'natural': inatural,
                'simdo': isimdo,
                'casing': icasing,
                'well_diameter': iwell_diameter
            })

        new_data_df = pd.DataFrame(output_data)
        self.excel_out = pd.concat([self.excel_out, new_data_df], ignore_index=True)

        try:
            self.excel_out.to_excel(f"{self.XL_BASE}\\{self.XL_OUTPUT}", index=False)
            return "Processing complete. Output saved to appendix_01.xlsx."
        except Exception as e:
            return f"Error saving output Excel file: {str(e)}"

    def run(self):
        result = self.initial_work()
        print(result)


# Example usage
if __name__ == "__main__":
    appendix_maker = AppendixMaker()
    appendix_maker.run()
