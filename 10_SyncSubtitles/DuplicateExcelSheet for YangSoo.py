import shutil
import os

# Example usage
original_file_path = "d:/05_Send/A1_ge_OriginalSaveFile.xlsm"
destination_folder = "d:/05_Send/"
new_filename = "_ge_OriginalSaveFile.xlsm"


def duplicate_and_rename_file(original_path, destination_folder, new_filename, cnt):
    # Extract filename from original path
    filename = os.path.basename(original_path)
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    # Destination path for the duplicated file

    destination_path = os.path.join(destination_folder, f"A{cnt}"+new_filename)
    # Copy the original file to the destination folder
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
    n = get_user_input()
    print("You entered:", n)
    for i in  range(2, n+1):
        new_file_path = duplicate_and_rename_file(original_file_path, destination_folder, new_filename, i)
        print(f"File duplicated and renamed to: {new_file_path}")


if __name__ == "__main__":
    main()



