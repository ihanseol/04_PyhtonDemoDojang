import os
import sys

from FileProcessing_V4_20240708 import FileBase

def main(start_dir):
    if start_dir is None:
        return None

    print(start_dir)
    fb = FileBase(start_dir)

    del_list = ['.bak', '.dwl', '.log']
    print(del_list)

    rlist = fb.get_list_files(del_list)
    print(rlist)
    fb.delete_files(start_dir, rlist)


if __name__ == "__main__":
    args = sys.argv
    arg1 = args[1] if len(args) > 1 else None
    path = arg1.strip('"')

    print('start', path)
    main(path)
    # input('press enter to go')

