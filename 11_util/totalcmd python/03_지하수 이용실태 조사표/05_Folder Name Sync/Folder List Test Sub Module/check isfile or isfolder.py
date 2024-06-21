import os
from enum import Enum


class CheckDir(Enum):
    DIRECTORY = 1
    FILE = 2
    NOTHING = 3


def check_path(path):
    if os.path.isdir(path):
        # return "Directory"
        return CheckDir.DIRECTORY
    elif os.path.isfile(path):
        # return "File"
        return CheckDir.FILE
    else:
        # return "Neither a file nor a directory"
        return CheckDir.NOTHING


def one_level_up_if_directory(path):
    if os.path.isdir(path):
        parent_directory = os.path.dirname(path)
        return parent_directory
    else:
        return "The given path is not a directory."


# Example usage:
path = r'd:\09_hardRain\04_ihanseol - 2019\00_Data'
result = check_path(path)
print(f"The path '{path}' is: {result}")


result = one_level_up_if_directory(path)
print(f"Result: {result}")







'''

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

Example usage:
print(Color.RED)
print(Color.GREEN.name)
print(Color.BLUE.value)

'''
