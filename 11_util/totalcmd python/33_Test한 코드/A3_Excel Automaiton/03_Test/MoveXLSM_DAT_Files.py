import os
import shutil

DIRECTORY = "d:\\05_Send\\"
DOCUMENTS = "c:\\Users\\minhwasoo\\Documents\\"
destination_folder = "d:\\06_Send2\\"


def move_file(source, destination):
    try:
        # Move the file from source to destination
        shutil.move(source, destination)
        print(f"File moved successfully from '{source}' to '{destination}'")
    except Exception as e:
        print(f"Error moving file: {e}")


def main():
    os.chdir(DOCUMENTS)
    files = os.listdir()

    xlsmfiles = [f for f in files if f.endswith('.xlsm')]
    datfiles = [f for f in files if f.endswith('.dat')]

    for file in xlsmfiles:
        move_file(DOCUMENTS + file, destination_folder + file)

    for file in datfiles:
        move_file(DOCUMENTS + file, destination_folder + file)


if __name__ == '__main__':
    main()
