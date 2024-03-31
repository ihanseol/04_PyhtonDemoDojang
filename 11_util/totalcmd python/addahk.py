import os
import argparse


def rename_file_extension(filename, extension=".ahk"):
    # Verify if extension starts with a dot
    if not extension.startswith("."):
        extension = "." + extension

    # Verify if file exists
    if not os.path.exists(filename):
        print("File not found.")
        return

    # Rename the file with the new extension
    try:
        file_name, _ = os.path.splitext(filename)
        os.rename(filename, file_name + extension)
        print("File extension successfully changed to", extension)
    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Rename file with a specified extension")

    # Add optional arguments
    parser.add_argument("filename", type=str, help="Name of the file")
    parser.add_argument("-e", "--extension", type=str, help="Desired extension", default=".ahk")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function to rename file extension
    rename_file_extension(args.filename, args.extension)
