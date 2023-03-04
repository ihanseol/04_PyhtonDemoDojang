import os

def print_tree(path, prefix=''):
    # Print the directory name
    print(f"{prefix}├── {os.path.basename(path)}")

    # Recurse into the subdirectories
    for idx, subpath in enumerate(sorted([os.path.join(path, name) for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))])):
        if idx == len(os.listdir(path)) - 1:
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
