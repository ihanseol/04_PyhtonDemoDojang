import configparser
import os
import sys
import shutil
from datetime import datetime
import glob


def detect_coreldraw_paths():
    """Detect installed CorelDRAW paths."""
    possible_paths = {
        '2019': r'c:\Program Files\Corel\CorelDRAW Graphics Suite 2019\Programs64\CorelDRW.exe',
        '2021': r'c:\Program Files\Corel\CorelDRAW Graphics Suite 2021\Programs64\CorelDRW.exe'
    }
    valid_paths = {}
    for version, path in possible_paths.items():
        if os.path.exists(path):
            valid_paths[version] = path
    return valid_paths


def set_coreldraw_config(version='2019'):
    """Set CorelDRAW configuration in tcer.ini."""
    config = configparser.ConfigParser(comment_prefixes=(';', '#'))

    try:
        config.read('tcer.ini', encoding='utf-8')
    except UnicodeDecodeError:
        print("Error: tcer.ini encoding is not UTF-8. Please check the file.")
        return

    if 'Program_CorelDraw' not in config:
        config.add_section('Program_CorelDraw')
        print("Created new Program_CorelDraw section.")

    corel_paths = detect_coreldraw_paths()
    if version not in corel_paths:
        print(f"Error: CorelDRAW {version} not found at expected path.")
        return

    config['Program_CorelDraw']['FullPath'] = corel_paths[version]
    config['Program_CorelDraw']['MDI'] = '1'

    # Store inactive path as a separate key
    inactive_version = '2021' if version == '2019' else '2019'
    if inactive_version in corel_paths:
        config['Program_CorelDraw']['InactivePath'] = corel_paths[inactive_version]

    with open('tcer.ini', 'w', encoding='utf-8') as f:
        config.write(f)

    print(f"Set CorelDRAW {version} configuration.")
    verify_config()


def verify_config():
    """Verify the current configuration."""
    config = configparser.ConfigParser(comment_prefixes=(';', '#'))
    try:
        config.read('tcer.ini', encoding='utf-8')
    except UnicodeDecodeError:
        print("Error: Unable to read tcer.ini due to encoding issues.")
        return

    if 'Program_CorelDraw' in config:
        corel_section = config['Program_CorelDraw']
        full_path = corel_section.get('FullPath', 'Not set')
        mdi = corel_section.get('MDI', 'Not set')
        print(f"FullPath: {full_path}")
        print(f"MDI: {mdi}")
        if full_path != 'Not set' and os.path.exists(full_path):
            print("✓ Path is valid.")
        else:
            print("✗ Path is invalid or not set.")
    else:
        print("Program_CorelDraw section not found.")


def switch_version(target_version):
    """Switch to the specified CorelDRAW version."""
    set_coreldraw_config(version=target_version)
    print(f"Switched to CorelDRAW {target_version}.")


def read_corel_version():
    """Read the current CorelDRAW version."""
    config = configparser.ConfigParser(comment_prefixes=(';', '#'))
    try:
        config.read('tcer.ini', encoding='utf-8')
    except FileNotFoundError:
        print("Error: tcer.ini file not found.")
        return None
    except UnicodeDecodeError:
        print("Error: tcer.ini encoding is not UTF-8.")
        return None

    if 'Program_CorelDraw' in config:
        full_path = config['Program_CorelDraw'].get('FullPath', 'Not set')
        print("=== Program_CorelDraw Settings ===")
        print(f"FullPath: {full_path}")
        print(f"MDI: {config['Program_CorelDraw'].get('MDI', 'Not set')}")

        if '2019' in full_path:
            print("→ CorelDRAW 2019 is active.")
            return '2019'
        elif '2021' in full_path:
            print("→ CorelDRAW 2021 is active.")
            return '2021'
        else:
            print("→ Unknown version.")
            return None
    else:
        print("Program_CorelDraw section not found.")
        return None


def copy_tcer_ini(dest_dir, backup_existing=True, max_backups=5):
    """Copy tcer.ini to the destination directory."""
    src_file = os.path.join(os.getcwd(), "tcer.ini")
    if not os.path.isfile(src_file):
        print(f"Error: Source file not found: {src_file}")
        return

    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, "tcer.ini")

    # Manage backups
    if os.path.exists(dest_file) and backup_existing:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(dest_dir, f"tcer_{timestamp}.bak")
        shutil.move(dest_file, backup_file)
        print(f"Backed up existing file to {backup_file}")

        # Clean up old backups if exceeding max_backups
        backups = sorted(glob.glob(os.path.join(dest_dir, "tcer_*.bak")))
        if len(backups) > max_backups:
            for old_backup in backups[:-max_backups]:
                os.remove(old_backup)
                print(f"Removed old backup: {old_backup}")

    shutil.copy2(src_file, dest_file)
    print(f"Copied {src_file} → {dest_file}")


if __name__ == "__main__":
    print("=== CorelDRAW Configuration Manager ===")
    print("Switches between CorelDRAW 2019 and 2021 in tcer.ini.")

    current_version = read_corel_version()
    if current_version:
        target_version = '2021' if current_version == '2019' else '2019'
        switch_version(target_version)
        copy_tcer_ini(r"c:\Program Files\totalcmd\plugins\utils\util_tcer", backup_existing=False)

        # Pause for user confirmation (optional)
        input("Press Enter to exit...")
    else:
        print("Aborting due to configuration error.")

    input("Press Enter to exit...")