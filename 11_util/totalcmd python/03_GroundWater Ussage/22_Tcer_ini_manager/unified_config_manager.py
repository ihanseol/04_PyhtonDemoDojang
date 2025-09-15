import configparser
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Type
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

    @property
    def display_name(self) -> str:
        return f"CorelDRAW {self.value}"


class HwpVersion(Enum):
    """Enumeration for HWP versions"""
    V2022 = "2022"
    V2024 = "2024"

    @property
    def path(self) -> str:
        """Get the full path for this HWP version"""
        office_version = 'Hoffice120' if self.value == '2022' else 'Hoffice130'
        base_path = r"C:\Program Files (x86)\Hnc\Office"
        return f"{base_path} {self.value}\\{office_version}\\Bin\\Hwp.exe"

    @property
    def display_name(self) -> str:
        return f"HWP {self.value}"


class ProgramType(Enum):
    """Supported program types"""
    COREL = ("Program_CorelDraw", CorelVersion)
    HWP = ("Program_HWP", HwpVersion)

    def __init__(self, section_name: str, version_enum: Type[Enum]):
        self.section_name = section_name
        self.version_enum = version_enum

    @property
    def versions(self) -> List[Enum]:
        """Get all available versions for this program type"""
        return list(self.version_enum)


class UnifiedConfigManager:
    """Unified manager for program configurations in tcer.ini file"""

    DEFAULT_CONFIG_FILE = "tcer.ini"
    DEFAULT_DEST_DIR = r"c:\Program Files\totalcmd\plugins\utils\util_tcer"

    def __init__(self, config_file: str = DEFAULT_CONFIG_FILE):
        """
        Initialize the unified configuration manager.

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

    def _ensure_section_exists(self, program_type: ProgramType) -> None:
        """Ensure the program section exists in config"""
        if program_type.section_name not in self.config:
            self.config.add_section(program_type.section_name)
            print(f"Created new section: {program_type.section_name}")

    def get_current_version(self, program_type: ProgramType) -> Optional[Enum]:
        """
        Get the currently active version for a program type.

        Args:
            program_type: The program type to check

        Returns:
            Version enum if found, None otherwise
        """
        try:
            self._ensure_config_loaded()

            if program_type.section_name not in self.config:
                print(f"Section '{program_type.section_name}' not found in config file.")
                return None

            section = self.config[program_type.section_name]
            full_path = section.get('FullPath', '')

            if not full_path:
                print(f"FullPath not set in {program_type.section_name} configuration.")
                return None

            for version in program_type.versions:
                if version.value in full_path:
                    return version

            print(f"Unknown {program_type.name} version in configuration.")
            return None

        except Exception as e:
            print(f"Error reading current version for {program_type.name}: {e}")
            return None

    def display_current_config(self, program_type: ProgramType = None) -> None:
        """
        Display current configuration settings

        Args:
            program_type: Specific program type to display, or None for all
        """
        try:
            self._ensure_config_loaded()

            program_types = [program_type] if program_type else list(ProgramType)

            for pt in program_types:
                print(f"=== {pt.name} Configuration ===")

                if pt.section_name in self.config:
                    section = self.config[pt.section_name]
                    full_path = section.get('FullPath', 'Not configured')
                    mdi = section.get('MDI', 'Not configured')

                    print(f"FullPath: {full_path}")
                    print(f"MDI: {mdi}")

                    # Display current version
                    current_version = self.get_current_version(pt)
                    if current_version:
                        print(f"→ Currently using {current_version.display_name}")

                        # Check if path exists
                        if full_path != 'Not configured' and os.path.exists(full_path):
                            print("✓ Path is valid")
                        elif full_path != 'Not configured':
                            print("✗ Path not found")

                    print("\nAll configuration items:")
                    for key, value in section.items():
                        print(f"  {key} = {value}")
                else:
                    print(f"Section '{pt.section_name}' not found.")

                print()  # Add spacing between sections

        except Exception as e:
            print(f"Error displaying configuration: {e}")

    def switch_version(self, program_type: ProgramType, target_version: Enum) -> bool:
        """
        Switch to the specified program version.

        Args:
            program_type: The program type to configure
            target_version: The version to switch to

        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate target version belongs to program type
            if target_version not in program_type.versions:
                print(f"Version {target_version.value} is not valid for {program_type.name}")
                return False

            self._ensure_config_loaded()
            self._ensure_section_exists(program_type)

            current_version = self.get_current_version(program_type)

            if current_version == target_version:
                print(f"Already using {target_version.display_name}")
                return True

            print(f"Switching to {target_version.display_name}...")

            # Update configuration
            self.config[program_type.section_name]['FullPath'] = target_version.path
            self.config[program_type.section_name]['MDI'] = '1'

            # Save with comments
            self._save_config_with_comments(program_type, target_version)

            print(f"✓ Successfully switched to {target_version.display_name}")
            return True

        except Exception as e:
            print(f"Error switching version: {e}")
            return False

    def _save_config_with_comments(self, program_type: ProgramType, active_version: Enum) -> None:
        """
        Save configuration file with commented alternate versions.

        Args:
            program_type: The program type being configured
            active_version: The version to make active
        """
        try:
            # Read existing file content
            with open(self.config_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = []
            in_target_section = False
            comment_added = False

            for line in lines:
                line_stripped = line.strip()

                # Track if we're in the target section
                if line_stripped == f"[{program_type.section_name}]":
                    in_target_section = True
                    new_lines.append(line)
                    continue

                # Check if we've moved to another section
                if line_stripped.startswith("[") and line_stripped != f"[{program_type.section_name}]":
                    in_target_section = False

                # Handle FullPath lines in target section
                if in_target_section and 'FullPath=' in line and not comment_added:
                    # Add active version first, then commented alternates
                    new_lines.append(f"FullPath={active_version.path}\n")

                    # Add commented alternate versions
                    for version in program_type.versions:
                        if version != active_version:
                            new_lines.append(f";FullPath={version.path}\n")

                    comment_added = True
                    continue

                # Skip existing FullPath lines for this program in the section
                if in_target_section and 'FullPath=' in line_stripped:
                    continue

                new_lines.append(line)

            # Write updated content
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

        except Exception as e:
            print(f"Error saving config with comments: {e}")
            raise

    def toggle_version(self, program_type: ProgramType) -> bool:
        """
        Toggle between available versions for a program type.

        Args:
            program_type: The program type to toggle

        Returns:
            True if successful, False otherwise
        """
        current_version = self.get_current_version(program_type)
        versions = program_type.versions

        if len(versions) < 2:
            print(f"Cannot toggle - only {len(versions)} version(s) available for {program_type.name}")
            return False

        if current_version is None:
            # If no current version, switch to first available
            return self.switch_version(program_type, versions[0])

        # Find current version index and switch to next
        try:
            current_index = versions.index(current_version)
            next_index = (current_index + 1) % len(versions)
            return self.switch_version(program_type, versions[next_index])
        except ValueError:
            # Current version not found in list, switch to first
            return self.switch_version(program_type, versions[0])

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

    def validate_paths(self, program_type: ProgramType = None) -> Dict[str, Dict[str, bool]]:
        """
        Validate installation paths for program types.

        Args:
            program_type: Specific program type to validate, or None for all

        Returns:
            Dictionary mapping program names to version validation results
        """
        results = {}
        program_types = [program_type] if program_type else list(ProgramType)

        for pt in program_types:
            results[pt.name] = {}
            for version in pt.versions:
                results[pt.name][version.value] = os.path.exists(version.path)

        return results

    def setup_initial_config(self, program_configs: Dict[ProgramType, Enum] = None) -> bool:
        """
        Setup initial configuration with default settings.

        Args:
            program_configs: Dictionary mapping program types to default versions

        Returns:
            True if successful, False otherwise
        """
        try:
            if program_configs is None:
                # Use first available version for each program type
                program_configs = {pt: pt.versions[0] for pt in ProgramType}

            self._ensure_config_loaded()

            print("=== Setting up initial configuration ===")

            success = True
            for program_type, default_version in program_configs.items():
                print(f"Setting up {program_type.name}...")
                if not self.switch_version(program_type, default_version):
                    success = False

            return success

        except Exception as e:
            print(f"Error setting up initial configuration: {e}")
            return False

    def list_available_programs(self) -> None:
        """List all available program types and their versions"""
        print("=== Available Programs ===")
        for pt in ProgramType:
            print(f"{pt.name}:")
            for version in pt.versions:
                status = "✓" if os.path.exists(version.path) else "✗"
                print(f"  {status} {version.display_name} -> {version.path}")
            print()


def main():
    """Main function to demonstrate usage"""
    print("=== Unified Program Configuration Manager ===")
    print("Manages version switching for multiple programs")

    try:
        # Initialize manager
        manager = UnifiedConfigManager()

        # List available programs
        manager.list_available_programs()

        # Display current configuration for all programs
        manager.display_current_config()

        # Example: Toggle CorelDRAW version
        print("\n" + "=" * 50)
        print("Toggling CorelDRAW version...")
        manager.toggle_version(ProgramType.COREL)

        # Example: Toggle HWP version
        print("\n" + "=" * 50)
        print("Toggling HWP version...")
        manager.toggle_version(ProgramType.HWP)

        # Copy to destination
        # print("\n" + "=" * 50)
        # manager.copy_config_to_destination(backup_existing=False)

        # Validate all paths
        print("\n=== Path Validation ===")
        validation_results = manager.validate_paths()
        for program_name, versions in validation_results.items():
            print(f"{program_name}:")
            for version, is_valid in versions.items():
                status = "✓ Valid" if is_valid else "✗ Not found"
                print(f"  Version {version}: {status}")

        input('\nPress Enter to exit...')

    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
