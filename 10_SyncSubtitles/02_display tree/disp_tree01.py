import os

def print_tree(path, prefix=''):
    # Get the contents of the directory
    dir_list = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    file_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    # Print the directory name
    print(f"{prefix}├── {os.path.basename(path)}")

    # Print the files in the directory
    for file in file_list:
        print(f"{prefix}│   ├── {file}")

    # Recurse into the subdirectories
    for idx, dir in enumerate(dir_list):
        subpath = os.path.join(path, dir)
        if idx == len(dir_list) - 1:
            print_tree(subpath, f"{prefix}    ")
        else:
            print_tree(subpath, f"{prefix}│   ")

if __name__ == '__main__':
    import sys

    # Use the current directory if no arguments given
    if len(sys.argv) == 1:
        path = '.'
    else:
        path = sys.argv[1]

    print_tree(path)