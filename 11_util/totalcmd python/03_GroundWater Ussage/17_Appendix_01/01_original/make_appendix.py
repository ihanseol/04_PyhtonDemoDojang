import pandas as pd


class WellData:
    def __init__(self):
        self.well_dict = {}
        self.well_d3 = 0
        self.migogyul = 0
        self.migogyul_1 = 0
        self.migogyul_2 = 0
        self.rest_height = 0
        self.bedrock = ''

    def set_welldata(self, gong, title, address, q, natural, stable, simdo, well_d, casing, bedrock):
        # Store the basic well data
        self.well_dict = {
            "gong": gong,
            "title": title,
            "address": address,
            "q": q,
            "natural": natural,
            "stable": stable,
            "simdo": simdo,
            "simdo1": simdo,
            "casing": casing,
            "well_diameter": well_d,
            "bedrock": bedrock
        }

        self.well_d3 = well_d + 100
        self.migogyul = casing - 1
        self.migogyul_1 = casing - 1
        self.migogyul_2 = casing - 1
        self.rest_height = simdo - casing

    def print_well_dict(self):
        print("Well Data:")
        for key, value in self.well_dict.items():
            print(f"{key}: {value}")
        print(f"well_d3: {self.well_d3}")
        print(f"migogyul: {self.migogyul}")
        print(f"migogyul1: {self.migogyul_1}")
        print(f"migogyul2: {self.migogyul_2}")
        print(f"rest_height: {self.rest_height}")


class AppendixMaker:
    def __init__(self):
        self.XL_INPUT = "YanSoo_Spec.xlsx"
        self.XL_OUTPUT = "appendix_01.xlsx"
        self.XL_BASE = "d:\\05_Send"
        self.excel_in = pd.DataFrame()
        self.excel_out = pd.DataFrame()
        self.wd = WellData()

    def clear_output_data(self):
        output_columns = ['gong', 'title', 'address', 'q', 'natural', 'stable', 'simdo', 'simdo1', 'casing', 'welld1',
                          'welld2', 'welld3', 'migogyul', 'migogyul_1', 'migogyul_2', 'rest_height', 'bedrock']
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

        required_columns = ['gong', 'Project Name', 'address', 'q', 'natural', 'stable', 'simdo', 'well_diameter',
                            'casing']
        if not all(col in self.excel_in.columns for col in required_columns):
            return "Error: Input Excel file is missing required columns."

        self.clear_output_data()

        try:
            self.excel_out = pd.read_excel(f"{self.XL_BASE}\\{self.XL_OUTPUT}")
        except FileNotFoundError:
            output_columns = ['gong', 'title', 'address', 'q', 'natural', 'stable', 'simdo', 'simdo1', 'casing',
                              'welld1', 'welld2', 'welld3', 'migogyul', 'migogyul_1', 'migogyul_2', 'rest_height',
                              'bedrock']
            self.excel_out = pd.DataFrame(columns=output_columns)

        # Process each row in excel_in
        output_data = []
        for i, gong in enumerate(self.excel_in['gong']):
            # Extract data from excel_in
            igong = self.excel_in.iloc[i, self.excel_in.columns.get_loc('gong')]
            ititle = self.excel_in.iloc[i, self.excel_in.columns.get_loc('Project Name')]
            iaddress = self.excel_in.iloc[i, self.excel_in.columns.get_loc('address')] + f'({igong})'
            iq = self.excel_in.iloc[i, self.excel_in.columns.get_loc('q')]
            inatural = self.excel_in.iloc[i, self.excel_in.columns.get_loc('natural')]
            istable = self.excel_in.iloc[i, self.excel_in.columns.get_loc('stable')]
            isimdo = self.excel_in.iloc[i, self.excel_in.columns.get_loc('simdo')]
            iwelld = self.excel_in.iloc[i, self.excel_in.columns.get_loc('well_diameter')]
            icasing = self.excel_in.iloc[i, self.excel_in.columns.get_loc('casing')]
            ibedrock = self.excel_in.iloc[i, self.excel_in.columns.get_loc('bedrock')]

            # Set well data and calculate derived attributes
            self.wd.set_welldata(igong, ititle, iaddress, iq, inatural, istable, isimdo, iwelld, icasing, ibedrock)
            self.wd.print_well_dict()
            print("-" * 80)

            output_data.append({
                'gong': igong,
                'title': ititle,
                'address': iaddress,
                'q': iq,
                'natural': inatural,
                'stable': istable,
                'simdo': isimdo,
                'simdo1': isimdo,
                'casing': icasing,
                'welld1': iwelld,
                'welld2': iwelld,
                'welld3': self.wd.well_d3,
                'migogyul': self.wd.migogyul,
                'migogyul_1': self.wd.migogyul_1,
                'migogyul_2': self.wd.migogyul_2,
                'rest_height': self.wd.rest_height,
                'bedrock': ibedrock
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
