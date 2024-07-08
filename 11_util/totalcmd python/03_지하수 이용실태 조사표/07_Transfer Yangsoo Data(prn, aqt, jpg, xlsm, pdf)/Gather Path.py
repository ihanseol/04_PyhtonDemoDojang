import FileProcessing_V3 as fp2c
# fp2c - file processing class v2

fp = fp2c.FileBase('')


def main_job2(folder=fp.select_folder()):
    spath = folder

    print(spath)
    print('-' * 120)
    path_list = fp.unfold_path(spath)

    print(path_list[:])
    print(path_list[:-2])
    print(path_list[:-3])

    print('-' * 120)
    print(path_list)
    print('-' * 120)
    print(fp.join_path(path_list))


if __name__ == '__main__':
    # main()
    main_job2()
