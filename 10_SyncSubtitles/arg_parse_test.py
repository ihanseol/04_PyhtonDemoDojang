import argparse


def main_job(mode):
    print(mode)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['sub', 'mov'], help="Select 'sub' or 'mov' mode.")
    args = parser.parse_args()

    main_job(args.mode)

if __name__ == "__main__":
    main()

    