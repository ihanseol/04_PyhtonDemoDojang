import configparser
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from enum import Enum


class CorelVersion(Enum):
    """Enumeration for CorelDRAW versions"""
    V2019 = "2019"
    V2021 = "2021"

    @property
    def path(self) -> str:
        """Get the full path for this CorelDRAW version"""
        base_path = r"c:\Program Files\Corel\CorelDRAW Graphics Suite"
        return f"{base_path} {self.value}\\Programs64\\CorelDRW.exe"


class CorelConfigManager:
    """Manager for CorelDRAW configuration in tcer.ini file"""

    DEFAULT_CONFIG_FILE = "tcer.ini"
    SECTION_NAME = "Program_CorelDraw"
    DEFAULT_DEST_DIR = r"c:\Program Files\totalcmd\plugins\utils\util_tcer"

    def __init__(self, config_file: str = DEFAULT_CONFIG_FILE):
        """
        Initialize the CorelDRAW configuration manager.

        Args:
            config_file: Path to the configuration file (default: tcer.ini)
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.comment_prefixes = (';', '#')

    def _ensure_config_loaded(self) -> None:
        """Ensure configuration file is loaded"""
        try:
            self.config.read(self.config_file, encoding='utf-8')
        except Exception as e:
            raise FileNotFoundError(f"Cannot read config file '{self.config_file}': {e}")

    def _ensure_section_exists(self) -> None:
        """Ensure the CorelDRAW section exists in config"""
        if self.SECTION_NAME not in self.config:
            self.config.add_section(self.SECTION_NAME)
            print(f"Created new section: {self.SECTION_NAME}")

    def get_current_version(self) -> Optional[CorelVersion]:
        """
        Get the currently active CorelDRAW version.

        Returns:
            CorelVersion if found, None otherwise
        """
        try:
            self._ensure_config_loaded()

            if self.SECTION_NAME not in self.config:
                print(f"Section '{self.SECTION_NAME}' not found in config file.")
                return None

            section = self.config[self.SECTION_NAME]
            full_path = section.get('FullPath', '')

            if not full_path:
                print("FullPath not set in configuration.")
                return None

            for version in CorelVersion:
                if version.value in full_path:
                    return version

            print("Unknown CorelDRAW version in configuration.")
            return None

        except Exception as e:
            print(f"Error reading current version: {e}")
            return None

    def display_current_config(self) -> None:
        """Display current configuration settings"""
        try:
            self._ensure_config_loaded()

            print("=== Current Configuration ===")

            if self.SECTION_NAME in self.config:
                section = self.config[self.SECTION_NAME]
                full_path = section.get('FullPath', 'Not configured')
                mdi = section.get('MDI', 'Not configured')

                print(f"FullPath: {full_path}")
                print(f"MDI: {mdi}")

                # Display current version
                current_version = self.get_current_version()
                if current_version:
                    print(f"→ Currently using CorelDRAW {current_version.value}")

                    # Check if path exists
                    if full_path != 'Not configured' and os.path.exists(full_path):
                        print("✓ Path is valid")
                    elif full_path != 'Not configured':
                        print("✗ Path not found")

                print("\nAll configuration items:")
                for key, value in section.items():
                    print(f"  {key} = {value}")
            else:
                print(f"Section '{self.SECTION_NAME}' not found.")

        except Exception as e:
            print(f"Error displaying configuration: {e}")

    def switch_version(self, target_version: CorelVersion) -> bool:
        """
        Switch to the specified CorelDRAW version.

        Args:
            target_version: The version to switch to

        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_config_loaded()
            self._ensure_section_exists()

            current_version = self.get_current_version()

            if current_version == target_version:
                print(f"Already using CorelDRAW {target_version.value}")
                return True

            print(f"Switching to CorelDRAW {target_version.value}...")

            # Update configuration
            self.config[self.SECTION_NAME]['FullPath'] = target_version.path
            self.config[self.SECTION_NAME]['MDI'] = '1'

            # Save with comments
            self._save_config_with_comments(target_version)

            print(f"✓ Successfully switched to CorelDRAW {target_version.value}")
            return True

        except Exception as e:
            print(f"Error switching version: {e}")
            return False

    def _save_config_with_comments(self, active_version: CorelVersion) -> None:
        """
        Save configuration file with commented alternate version.

        Args:
            active_version: The version to make active
        """
        try:
            # Read existing file content
            with open(self.config_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = []
            in_corel_section = False
            comment_added = False

            for line in lines:
                line_stripped = line.strip()

                # Track if we're in the CorelDRAW section
                if line_stripped == f"[{self.SECTION_NAME}]":
                    in_corel_section = True
                    new_lines.append(line)
                    continue

                # Check if we've moved to another section
                if line_stripped.startswith("[") and line_stripped != f"[{self.SECTION_NAME}]":
                    in_corel_section = False

                # Handle FullPath lines in CorelDRAW section
                if in_corel_section and 'FullPath=' in line and not comment_added:
                    # Add active version first, then commented alternate
                    new_lines.append(f"FullPath={active_version.path}\n")

                    # Add commented alternate version
                    for version in CorelVersion:
                        if version != active_version:
                            new_lines.append(f";FullPath={version.path}\n")

                    comment_added = True
                    continue

                if (active_version.value in line_stripped) and in_corel_section:
                    continue
                else:
                    new_lines.append(line)

            # Write updated content
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

        except Exception as e:
            print(f"Error saving config with comments: {e}")
            raise

    def toggle_version(self) -> bool:
        """
        Toggle between available CorelDRAW versions.

        Returns:
            True if successful, False otherwise
        """
        current_version = self.get_current_version()

        if current_version == CorelVersion.V2019:
            return self.switch_version(CorelVersion.V2021)
        else:
            return self.switch_version(CorelVersion.V2019)

    def copy_config_to_destination(self, dest_dir: str = DEFAULT_DEST_DIR,
                                   backup_existing: bool = True) -> bool:
        """
        Copy configuration file to destination directory.

        Args:
            dest_dir: Target directory path
            backup_existing: Whether to backup existing file

        Returns:
            True if successful, False otherwise
        """
        try:
            src_file = Path(self.config_file)
            if not src_file.is_file():
                raise FileNotFoundError(f"Source file not found: {src_file}")

            # Create destination directory
            dest_path = Path(dest_dir)
            dest_path.mkdir(parents=True, exist_ok=True)

            dest_file = dest_path / self.config_file

            # Handle backup
            if dest_file.exists() and backup_existing:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = dest_path / f"tcer_{timestamp}.bak"
                shutil.move(str(dest_file), str(backup_file))
                print(f"Backed up existing file to: {backup_file}")

            # Copy file
            shutil.copy2(str(src_file), str(dest_file))
            print(f"Copied {src_file} → {dest_file}")
            return True

        except Exception as e:
            print(f"Error copying config file: {e}")
            return False

    def validate_paths(self) -> Dict[str, bool]:
        """
        Validate all CorelDRAW installation paths.

        Returns:
            Dictionary mapping version strings to validity
        """
        results = {}
        for version in CorelVersion:
            results[version.value] = os.path.exists(version.path)
        return results

    def setup_initial_config(self, default_version: CorelVersion = CorelVersion.V2019) -> bool:
        """
        Setup initial configuration with default settings.

        Args:
            default_version: Default CorelDRAW version to configure

        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_config_loaded()
            self._ensure_section_exists()

            print("=== Setting up initial configuration ===")
            self.switch_version(default_version)
            return True

        except Exception as e:
            print(f"Error setting up initial configuration: {e}")
            return False


def main():
    """Main function to demonstrate usage"""
    print("=== CorelDRAW Configuration Manager ===")
    print("Manages CorelDRAW version switching between 2019 and 2021")

    try:
        # Initialize manager
        manager = CorelConfigManager()

        # Display current configuration
        manager.display_current_config()

        # Toggle version
        print("\n" + "=" * 50)
        manager.toggle_version()

        # Copy to destination
        print("\n" + "=" * 50)
        manager.copy_config_to_destination(backup_existing=False)

        # Validate paths
        print("\n=== Path Validation ===")
        validation_results = manager.validate_paths()
        for version, is_valid in validation_results.items():
            status = "✓ Valid" if is_valid else "✗ Not found"
            print(f"CorelDRAW {version}: {status}")

        input('\nPress Enter to exit...')

    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()