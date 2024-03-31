import os

def get_paths_from_user():
    paths = []
    path = input("Enter a path (leave blank to stop): ").strip()
    return path


def write_paths_to_file(paths):
    # Split the input path by semicolon
    path_list = paths.split(';')

    # Write the paths to path.out file
    with open('path.out', 'w') as file:
        for path in path_list:
            file.write(path + '\n')


def main():
    print("Please enter paths. Leave blank to stop.")
    paths = get_paths_from_user()
    write_paths_to_file(paths)
    print("Paths have been written to 'path.out'.")


if __name__ == "__main__":
    main()
