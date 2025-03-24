import shutil
import os
from FileProcessing_V4_refactored import FileManager

# Example usage
original_file_path = "d:/05_Send/A1_ge_OriginalSaveFile.xlsm"
destination_folder = "d:/05_Send/"


def duplicate_and_rename_file(original_path, destination_folder, cnt):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    destination_path = os.path.join(destination_folder, f"A{cnt}_ge_OriginalSaveFile.xlsm")
    shutil.copy(original_path, destination_path)
    return destination_path


def get_user_input():
    while True:
        try:
            n = int(input("Enter the number of times to loop: "))
            if n <= 0:
                print("Please enter a positive integer.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    return n


def main():
    fm = FileManager()
    source = fm.get_file_filter('.', 'A1*.xlsm')[-1:]

    my_source = ''.join(source)
    print(my_source)
    if source:
        fm.copy_file(my_source, original_file_path)

    n = get_user_input()
    print("You entered:", n)
    for i in range(2, n + 1):
        new_file_path = duplicate_and_rename_file(original_file_path, destination_folder, i)
        print(f"File duplicated and renamed to: {new_file_path}")


if __name__ == "__main__":
    main()
