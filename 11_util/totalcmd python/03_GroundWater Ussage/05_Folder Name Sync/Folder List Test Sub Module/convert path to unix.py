import os


# def convert_dos_to_unix_path(dos_path):
#     # Convert backslashes to forward slashes
#     unix_path = dos_path.replace('\\', '/')
#     # Remove the drive letter (e.g., C:) and replace with root slash
#     if ':' in unix_path:
#         unix_path = '/' + unix_path.split(':', 1)[1]
#     return unix_path
def convert_dos_to_unix_path(dos_path):
    # Convert backslashes to forward slashes
    unix_path = dos_path.replace('\\', '/')
    # Remove the drive letter (e.g., C:) and replace with root slash
    return unix_path


# Example usage:
# dos_path = r'C:\Users\Example\Documents\file.txt'

dos_path = r'd:\09_hardRain\04_ihanseol - 2019\00_Data'

unix_path = convert_dos_to_unix_path(dos_path)
print(f"Converted path: {unix_path}")
