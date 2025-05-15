import time
import os
import glob
import pandas as pd
from pyhwpx import Hwp
import shutil
import merge_hwp_files as mh

SS_INPUT = "ss_out.xlsx"
AA_INPUT = "aa_out.xlsx"
XL_BASE = "d:\\05_Send"

HWP_BASE = r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\00_UsedWell"


def get_desktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop


def countdown(n):
    print(' Please Move the Command Window to Side ! ')
    while n > 0:
        print(n)
        time.sleep(1)
        n -= 1
    print("Time's up!")


def initial_work(mode):
    if mode == "aa":
        file_name = AA_INPUT
    else:
        file_name = SS_INPUT

    try:
        df = pd.read_excel(f"{XL_BASE}\\{file_name}")
    except FileNotFoundError:
        print("Error: XLSX file must located your d:/05_Send/ folder.")
        return False

    length = len(df)
    format_string = "{:<6} {:<15} {:<5} {:<5} {:<5} {:<5} {:<7} {:<5}"

    # Print header
    print(format_string.format("gong", "address", "simdo", "well", "hp", "q", "purpose", "inout"))
    print("-" * 80)  # Separator line

    # Print each row with aligned columns
    for i in range(length):
        print(format_string.format(
            df.iloc[i]['gong'],
            df.iloc[i]['address'],
            df.iloc[i]['simdo'],
            df.iloc[i]['well_diameter'],
            df.iloc[i]['hp'],
            df.iloc[i]['q'],
            df.iloc[i]['purpose'],
            df.iloc[i]['inout']
        ))

    print("-" * 80)  # Separator line
    print()
    return df


def initial_opencopy(df, mode):
    """
        :param df: datafrom of excel, ss_out.xlsx & aa_out.xlsx
        :param mode: selection mode ss or aa
        :return:
    """

    def loop25(n):
        """
            :param n: number of loop 25times
            :return:
        """
        hwp.goto_page(n)
        j = 1
        for ii in range((n - 1) * 25 + 1, n * 25 + 1):
            n_a: str = df.iloc[ii - 1]['gong']
            hwp.goto_addr("a" + str(j + 2))
            hwp.insert_text(n_a)

            hwp.goto_addr("b" + str(j + 2))
            n_b: str = df.iloc[ii - 1]['address']
            hwp.insert_text(n_b)

            hwp.goto_addr("c" + str(j + 2))
            n_c: str = df.iloc[ii - 1]['simdo']
            hwp.insert_text(n_c)

            hwp.goto_addr("d" + str(j + 2))
            n_d: str = df.iloc[ii - 1]['well_diameter']
            hwp.insert_text(n_d)

            hwp.goto_addr("e" + str(j + 2))
            n_e: str = df.iloc[ii - 1]['hp']
            hwp.insert_text(n_e)

            hwp.goto_addr("f" + str(j + 2))
            n_f: str = df.iloc[ii - 1]['q']
            hwp.insert_text(n_f)

            hwp.goto_addr("g" + str(j + 2))
            n_g: str = df.iloc[ii - 1]['purpose']
            hwp.insert_text(n_g)

            hwp.goto_addr("h" + str(j + 2))
            n_h: str = df.iloc[ii - 1]['inout']
            hwp.insert_text(n_h)

            j += 1

    def loop_rest(start, remainder_j):
        """
            :param start: quotient
            :param remainder_j: rest
            :return:
        """
        j = 1
        for ii in range((start * 25) + 1, (start * 25) + remainder_j + 1):
            n_a: str = df.iloc[ii - 1]['gong']
            hwp.goto_addr("a" + str(j + 2))
            hwp.insert_text(n_a)

            hwp.goto_addr("b" + str(j + 2))
            n_b: str= df.iloc[ii - 1]['address']
            hwp.insert_text(n_b)

            hwp.goto_addr("c" + str(j + 2))
            n_c: str = df.iloc[ii - 1]['simdo']
            hwp.insert_text(n_c)

            hwp.goto_addr("d" + str(j + 2))
            n_d: str = df.iloc[ii - 1]['well_diameter']
            hwp.insert_text(n_d)

            hwp.goto_addr("e" + str(j + 2))
            n_e: str = df.iloc[ii - 1]['hp']
            hwp.insert_text(n_e)

            hwp.goto_addr("f" + str(j + 2))
            n_f: str = df.iloc[ii - 1]['q']
            hwp.insert_text(n_f)

            hwp.goto_addr("g" + str(j + 2))
            n_g: str = df.iloc[ii - 1]['purpose']
            hwp.insert_text(n_g)

            hwp.goto_addr("h" + str(j + 2))
            n_h: str = df.iloc[ii - 1]['inout']
            hwp.insert_text(n_h)
            j += 1

    os.chdir(XL_BASE)
    q_sum_in = round(df.loc[df['inout'] == "O", 'q'].sum(), 2)
    q_sum_out = round(df.loc[df['inout'] == "X", 'q'].sum(), 2)
    qo_count = len(df.loc[df['inout'] == "O", 'q'])
    qx_count = len(df.loc[df['inout'] == "X", 'q'])

    hwp = Hwp(visible=False)
    hwp.open("01_취합본.hwp")

    length = len(df)
    nquo, remainder = divmod(length, 25)

    i = 0

    for i in range(1, nquo + 1):
        loop25(i)
        print("-" * 80)

    hwp.goto_page(nquo + 1)
    loop_rest(nquo, remainder)

    hwp.goto_addr("b27")
    hwp.insert_text(str(qo_count) + "개소(유역내)")
    hwp.goto_addr("b28")
    if q_sum_out == 0:
        hwp.insert_text("-")
    else:
        hwp.insert_text(str(qx_count) + "개소(유역외)")

    hwp.goto_addr("f27")
    hwp.insert_text(str(q_sum_in))

    hwp.goto_addr("f28")
    if q_sum_out == 0:
        hwp.insert_text("-")
    else:
        hwp.insert_text(str(q_sum_out))

    if mode == "ss":
        hwp.save_as(get_desktop() + "\\ss_report.hwp")
    else:
        hwp.save_as(get_desktop() + "\\aa_report.hwp")

    hwp.Quit()


def main_ss():
    df = initial_work("ss")

    length = len(df)
    nquo, remainder = divmod(length, 25)

    if length <= 24:
        shutil.copy(HWP_BASE + "\\02_SS_Final.hwpx", XL_BASE + '\\ss_00.hwpx')
    else:
        i = 0
        if remainder != 0:
            for i in range(nquo):
                source_file = HWP_BASE + "\\01_SS_General.hwpx"
                print(source_file)
                # print('ss_0' + str(i) + '.hwpx')
                shutil.copy(source_file, XL_BASE + f"\\ss_0{i}.hwpx")
            shutil.copy(HWP_BASE + "\\02_SS_Final.hwpx", XL_BASE + f"\\ss_0{i + 1}.hwpx")
        else:
            for i in range(nquo):
                shutil.copy(HWP_BASE + "\\01_SS_General.hwpx", XL_BASE + f"\\ss_0{i}.hwpx")
            shutil.copy(HWP_BASE + "\\02_SS_Final.hwpx", XL_BASE + f"\\ss_0{i + 1}.hwpx")

    mh.merge_hwp_files()
    initial_opencopy(df, "ss")
    os.remove("01_취합본.hwp")
    hwp = None
    df = None


def main_aa():
    df = initial_work("aa")

    length = len(df)
    nquo, remainder = divmod(length, 25)

    if length <= 24:
        shutil.copy(HWP_BASE + "\\02_AA_Final.hwpx", XL_BASE + '\\aa_00.hwpx')
    else:
        i = 0
        if remainder != 0:
            for i in range(nquo):
                source_file = HWP_BASE + "\\01_AA_General.hwpx"
                print(source_file)
                # print('aa_0' + str(i) + '.hwpx')
                shutil.copy(source_file, XL_BASE + f"\\aa_0{i}.hwpx")
            shutil.copy(HWP_BASE + "\\02_AA_Final.hwpx", XL_BASE + f"\\aa_0{i + 1}.hwpx")
        else:
            for i in range(nquo):
                shutil.copy(HWP_BASE + "\\01_AA_General.hwpx", XL_BASE + f"\\aa_0{i}.hwpx")
            shutil.copy(HWP_BASE + "\\02_AA_Final.hwpx", XL_BASE + f"\\aa_0{i + 1}.hwpx")

    mh.merge_hwp_files()
    initial_opencopy(df, "aa")
    os.remove("01_취합본.hwp")
    hwp = None
    df = None


def move_hwp_files_from_desktop(destination_path):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    search_pattern = os.path.join(desktop_path, "*.hwp")
    hwp_files = glob.glob(search_pattern)

    if not hwp_files:
        print(f"No *.hwp files found on the Desktop.")
        return

    # os.makedirs(destination_path, exist_ok=True)

    for file_path in hwp_files:
        try:
            shutil.move(file_path, destination_path)
            print(f"Moved: {os.path.basename(file_path)} to {destination_path}")
        except Exception as e:
            print(f"Error moving {os.path.basename(file_path)}: {e}")


def delete_hwp_files_in_current_directory(file_path='*.hwpx'):
    """Deletes all *.hwp files in the current directory."""
    # Use glob to find all *.hwp files in the current directory
    os.chdir(XL_BASE)
    hwp_files = glob.glob(file_path)

    if not hwp_files:
        print("No *.hwp files found in the current directory.")
        return  # Exit the function if no matching files are found

    # Iterate through the list of found files and delete each one
    for file_path in hwp_files:
        try:
            os.remove(file_path)  # Use os.remove to delete the file
            print(f"Deleted: {file_path}")
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")  # catch errors


if __name__ == "__main__":
    delete_hwp_files_in_current_directory("*.hwp*")
    main_aa()
    countdown(2)
    main_ss()
    move_hwp_files_from_desktop(XL_BASE)
    mh.merge_hwp_files("01_기사용관정.hwp","reverse")
    delete_hwp_files_in_current_directory("a*.hwp")
    delete_hwp_files_in_current_directory("s*.hwp")
