import os
import time

def open_aqt() -> int:
    return 1


def determine_runningstep(file_name):
    if os.path.exists(file_name):
        if "step" in file_name:
            return 1
        elif "janggi_01" in file_name:
            return 2
        elif "janggi_02" in file_name:
            return 3
        else:
            return 4
    else:
        return 1

def AqtesolverMain(file_name) -> int:
    dat_files = {
        1: f"A{open_aqt()}_ge_step_01.dat",
        2: f"A{open_aqt()}_ge_janggi_01.dat",
        3: f"A{open_aqt()}_ge_janggi_02.dat",
        4: f"A{open_aqt()}_ge_recover_01.dat"
    }
    running_step = determine_runningstep(file_name)

    dat_file = dat_files.get(running_step, None)
    if dat_file is None:
        print('Invalid running step. Match case exception...')
        return []



AqtesolverMain("test")








