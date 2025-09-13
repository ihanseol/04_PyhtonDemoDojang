import configparser
import os
import shutil
from datetime import datetime
import glob


class CorelConfigManager:
    """A class to manage CorelDRAW configuration in tcer.ini file."""

    def __init__(self, config_file='tcer.ini'):
        """Initialize with the path to the configuration file."""
        self.config_file = config_file
        self.config = configparser.ConfigParser(comment_prefixes=(';', '#'))
        self.corel_paths = {
            '2019': r'c:\Program Files\Corel\CorelDRAW Graphics Suite 2019\Programs64\CorelDRW.exe',
            '2021': r'c:\Program Files\Corel\CorelDRAW Graphics Suite 2021\Programs64\CorelDRW.exe'
        }
        self.section = 'Program_CorelDraw'

    def read_config(self):
        """Read the tcer.ini configuration file."""
        try:
            self.config.read(self.config_file, encoding='utf-8')
            return True
        except UnicodeDecodeError:
            print(f"Error: {self.config_file} encoding is not UTF-8.")
            return False
        except FileNotFoundError:
            print(f"Error: {self.config_file} file not found.")
            return False
        except configparser.Error as e:
            print(f"ConfigParser error: {e}")
            return False

    def ensure_section(self):
        """Ensure the Program_CorelDraw section exists."""
        if self.section not in self.config:
            self.config.add_section(self.section)
            print(f"Created new {self.section} section.")

    def set_config(self, version='2019'):
        """Set CorelDRAW configuration for the specified version."""
        if version not in self.corel_paths:
            print(f"Error: Unsupported version {version}. Available: {list(self.corel_paths.keys())}")
            return False

        try:
            if not self.read_config():
                return False

            self.ensure_section()
            self.config[self.section]['FullPath'] = self.corel_paths[version]
            self.config[self.section]['MDI'] = '1'
            # Store inactive path
            inactive_version = '2021' if version == '2019' else '2019'
            if inactive_version in self.corel_paths:
                self.config[self.section]['InactivePath'] = self.corel_paths[inactive_version]

            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)

            print(f"Set CorelDRAW {version} configuration.")
            self.verify_config()
            return True

        except Exception as e:
            print(f"Error setting configuration: {e}")
            return False

    def verify_config(self):
        """Verify the current configuration."""
        if not self.read_config():
            return

        if self.section in self.config:
            corel_section = self.config[self.section]
            full_path = corel_section.get('FullPath', 'Not set')
            mdi = corel_section.get('MDI', 'Not set')
            print("=== Current Settings ===")
            print(f"FullPath: {full_path}")
            print(f"MDI: {mdi}")

            if full_path != 'Not set' and os.path.exists(full_path):
                print("✓ Path is valid.")
            else:
                print("✗ Path is invalid or not set.")
        else:
            print(f"{self.section} section not found.")

    def read_version(self):
        """Read the current CorelDRAW version."""
        if not self.read_config():
            return None

        print(f"=== {self.section} Settings ===")
        if self.section in self.config:
            corel_section = self.config[self.section]
            full_path = corel_section.get('FullPath', 'Not set')
            mdi = corel_section.get('MDI', 'Not set')
            print(f"FullPath: {full_path}")
            print(f"MDI: {mdi}")

            if full_path != 'Not set':
                if '2019' in full_path:
                    print("→ CorelDRAW 2019 is active.")
                    return '2019'
                elif '2021' in full_path:
                    print("→ CorelDRAW 2021 is active.")
                    return '2021'
                else:
                    print("→ Unknown version.")
            print("\nAll settings:")
            for key, value in corel_section.items():
                print(f"  {key} = {value}")
        else:
            print(f"{self.section} section not found.")
        return None

    def switch_version(self, target_version):
        """Switch to the specified CorelDRAW version."""
        if target_version not in self.corel_paths:
            print(f"Error: Unsupported version {target_version}. Available: {list(self.corel_paths.keys())}")
            return False

        print(f"Switching to CorelDRAW {target_version}...")
        return self.set_config(version=target_version)

    def copy_config(self, dest_dir, backup_existing=True, max_backups=5):
        """Copy tcer.ini to the destination directory."""
        src_file = os.path.abspath(self.config_file)
        if not os.path.isfile(src_file):
            print(f"Error: Source file not found: {src_file}")
            return False

        os.makedirs(dest_dir, exist_ok=True)
        dest_file = os.path.join(dest_dir, os.path.basename(self.config_file))

        try:
            if os.path.exists(dest_file) and backup_existing:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(dest_dir, f"tcer_{timestamp}.bak")
                shutil.move(dest_file, backup_file)
                print(f"Backed up existing file to {backup_file}")

                # Clean up old backups
                backups = sorted(glob.glob(os.path.join(dest_dir, "tcer_*.bak")))
                if len(backups) > max_backups:
                    for old_backup in backups[:-max_backups]:
                        os.remove(old_backup)
                        print(f"Removed old backup: {old_backup}")

            shutil.copy2(src_file, dest_file)
            print(f"Copied {src_file} → {dest_file}")
            return True
        except Exception as e:
            print(f"Error copying file: {e}")
            return False


if __name__ == "__main__":
    print("=== CorelDRAW Configuration Manager ===")
    print("Manages tcer.ini to switch between CorelDRAW 2019 and 2021.")

    manager = CorelConfigManager()
    current_version = manager.read_version()
    if current_version:
        target_version = '2021' if current_version == '2019' else '2019'
        manager.switch_version(target_version)
        manager.copy_config(r"c:\Program Files\totalcmd\plugins\utils\util_tcer", backup_existing=False)
        input("Press Enter to exit...")
    else:
        print("Aborting due to configuration error.")