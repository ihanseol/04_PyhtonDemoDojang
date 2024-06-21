import os


def list_directories_in_current_path(path=r"d:/09_hardRain/"):
    if os.path.isdir(path):
        os.chdir(path)

    current_path = os.getcwd()
    directories = [d for d in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, d))]
    return directories


# Example usage:
directories = list_directories_in_current_path()
print("Directories in the current path:")
for directory in directories:
    print(directory)

print(directories)
