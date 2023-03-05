import os
import sys

def tree(dir_path, prefix='|__'):
    """
    A recursive function to display the tree structure of a directory.

    Parameters:
    dir_path (str): The path to the directory to be displayed.
    prefix (str): The prefix to use for each line of the tree structure.

    """
    # Get a list of all files and directories in the current directory.
    files = os.listdir(dir_path)

    # Loop through each file or directory in the list.
    for file in files:
        # Get the full path of the file or directory.
        path = os.path.join(dir_path, file)
        # Check if the file is a directory.
        if os.path.isdir(path):
            # Print the directory name with the prefix.
            print(prefix + file)
            # Call the tree function recursively with the subdirectory path and an updated prefix.
            tree(path, prefix + '|  ')

# Check if the script is being run directly (not imported as a module).
if __name__ == '__main__':
    # Check if there is at least one command line argument (in addition to the script name).
    if len(sys.argv) > 1:
        # Get the second command line argument (the target directory path).
        target_dir = sys.argv[1]
        # Call the tree function with the target directory path.
        tree(target_dir)
    else:
        # If no target directory is specified, print an error message.
        print('Please specify a directory path as a command line argument.')


        