import os
import fnmatch
import shutil
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox
from natsort import natsorted


class PathChecker:
    """Utility class for checking and validating file paths."""
    
    # Return codes for path checking
    RET_FILE = 1
    RET_DIR = 2
    RET_NOTHING = 0

    @staticmethod
    def check_path(path=""):
        """
        Check if a path exists and what type it is.
        
        Args:
            path: Path to check
            
        Returns:
            RET_FILE: If path is a file
            RET_DIR: If path is a directory
            RET_NOTHING: If path doesn't exist or is invalid
        """
        if path is None:
            return PathChecker.RET_NOTHING

        if os.path.exists(path):
            if os.path.isfile(path):
                return PathChecker.RET_FILE
            elif os.path.isdir(path):
                return PathChecker.RET_DIR
            else:
                return PathChecker.RET_NOTHING
        else:
            return PathChecker.RET_NOTHING

    def resolve_path(self, path=""):
        """
        Resolve and report what type of path is provided.
        
        Args:
            path: Path to resolve
            
        Returns:
            Path type code
        """
        if path is None:
            return PathChecker.RET_NOTHING

        result = self.check_path(path)
        if result == PathChecker.RET_FILE:
            print("Given Path is File")
        elif result == PathChecker.RET_DIR:
            print("Given Path is DIR")
        else:
            print("Given Path is NOTHING")
        
        return result


class FileManager(PathChecker):
    """
    Class for managing file operations with a working directory.
    """
    
    def __init__(self, directory='D:\\05_Send\\', debug_mode=True):
        """
        Initialize FileManager with a working directory.
        
        Args:
            directory: Working directory to start with
            debug_mode: Whether to print debug messages
        """
        self.default_directory = 'D:\\05_Send\\'
        self.send_directory = 'D:\\05_Send\\'
        self.send2_directory = 'D:\\06_Send2\\'
        self.documents_directory = os.path.expanduser("~\\Documents")
        
        # Application paths and file templates
        self.aqtesolv_path = 'C:\\WHPA\\AQTEver3.4(170414)\\AQTW32.EXE'
        self.tc_dir = 'C:\\Program Files\\totalcmd\\AqtSolv\\'
        
        # File template names
        self.step_file = "_01_step.aqt"
        self.long_file = "_02_long.aqt"
        self.recover_file = "_03_recover.aqt"
        
        # Excel templates
        self.yangsoo_excel = "A1_ge_OriginalSaveFile.xlsm"
        self.yangsoo_rest = "_ge_OriginalSaveFile.xlsm"
        self.yansoo_spec = "d:\\05_Send\\YanSoo_Spec.xlsx"
        
        # State flags
        self.is_aqt_open = False
        self.debug_mode = debug_mode
        self.delay = 0.2
        self.is_block = False
        
        # File list
        self.files = None
        
        # Set working directory
        if self.check_path(directory) != PathChecker.RET_NOTHING:
            self._set_directory(directory)
        else:
            self._set_directory(self.default_directory)

    def _set_directory(self, directory):
        """
        Set the working directory and refresh the file list.
        
        Args:
            directory: Directory to set as working directory
        """
        self.directory = directory
        os.chdir(self.directory)
        self.refresh_files()
        
    def refresh_files(self):
        """Refresh the list of files in the current directory."""
        if self.check_path(self.directory) == PathChecker.RET_DIR:
            self.files = os.listdir(self.directory)
        else:
            self._set_directory(self.default_directory)

    def get_files_by_extension(self, extension):
        """
        Get all files with a specific extension in the current directory.
        
        Args:
            extension: File extension to filter by (including dot)
            
        Returns:
            List of matching files
        """
        self.refresh_files()
        return [f for f in self.files if f.endswith(extension)]

    def get_files_by_pattern(self, pattern, directory=None):
        """
        Get files matching a pattern in the specified or current directory.
        
        Args:
            pattern: Pattern to match (using fnmatch)
            directory: Optional directory to search in
            
        Returns:
            Sorted list of matching files
        """
        if directory:
            self._set_directory(directory)
        self.refresh_files()
        return natsorted(fnmatch.filter(self.files, pattern))

    # Specific file type getters
    def get_xlsm_files(self):
        """Get all Excel macro-enabled workbooks."""
        return self.get_files_by_extension('.xlsm')
        
    def get_xlsx_files(self):
        """Get all Excel workbooks."""
        return self.get_files_by_extension('.xlsx')
        
    def get_aqt_files(self):
        """Get all AQT files."""
        return self.get_files_by_extension('.aqt')
        
    def get_dat_files(self):
        """Get all DAT files."""
        return self.get_files_by_extension('.dat')
        
    def get_prn_files(self):
        """Get all PRN files."""
        return self.get_files_by_extension('.prn')
        
    def get_pdf_files(self):
        """Get all PDF files."""
        return self.get_files_by_extension('.pdf')
        
    def get_jpg_files(self):
        """Get all JPG files."""
        return self.get_files_by_extension('.jpg')
        
    def get_image_files(self):
        """Get all image files (jpg, jpeg, png)."""
        return self.get_list_files(['.jpg', '.jpeg', '.png'])

    def get_list_files(self, extensions):
        """
        Get files matching any of the given extensions.
        
        Args:
            extensions: List of file extensions to match
            
        Returns:
            List of matching files
        """
        result = []
        for ext in extensions:
            result.extend(self.get_files_by_extension(ext))
        return result

    # Convenience methods for file filtering
    def get_xlsm_filter(self, path=None, pattern="*_ge_OriginalSaveFile.xlsm"):
        """Get XLSM files matching a pattern."""
        return self.get_files_by_pattern(pattern, path)
        
    def get_jpg_filter(self, path=None, pattern="*page1.jpg"):
        """Get JPG files matching a pattern."""
        if path:
            self._set_directory(path)
        return self.get_files_by_pattern(pattern)

    def get_file_filter(self, path=None, pattern="*.hwp"):
        """Get any files matching a pattern."""
        if path:
            self._set_directory(path)
        self.refresh_files()
        return natsorted(fnmatch.filter(self.files, pattern))

    # Path manipulation methods
    @staticmethod
    def separate_filename(filename):
        """
        Split a filename into name and extension.
        
        Args:
            filename: Filename to split
            
        Returns:
            Tuple of (name, extension)
        """
        return os.path.splitext(filename)

    @staticmethod
    def separate_path(file_path):
        """
        Split a path into directory and filename.
        
        Args:
            file_path: Path to split
            
        Returns:
            Tuple of (directory, filename)
        """
        return os.path.dirname(file_path), os.path.basename(file_path)

    @staticmethod
    def normalize_path(file_path):
        """
        Normalize a path by converting all slashes to forward slashes.
        
        Args:
            file_path: Path to normalize
            
        Returns:
            Normalized path
        """
        return file_path.replace("\\", "/")

    def join_path(self, *path_components):
        """
        Join path components into a single path.
        
        Args:
            *path_components: Path components to join
            
        Returns:
            Joined path
        """
        path = os.path.join(*path_components)
        return self.normalize_path(path)

    def get_dirname(self, file_path):
        """
        Get the directory part of a path.
        
        Args:
            file_path: Path to get directory from
            
        Returns:
            Directory path with trailing slash or None if invalid
        """
        if self.check_path(file_path) == PathChecker.RET_NOTHING:
            self.debug_print(f'get_dirname arg is not path ... {file_path}')
            return None
        return os.path.dirname(file_path) + os.path.sep

    def get_basename(self, file_path):
        """
        Get the filename part of a path.
        
        Args:
            file_path: Path to get filename from
            
        Returns:
            Filename or None if invalid
        """
        if self.check_path(file_path) == PathChecker.RET_NOTHING:
            self.debug_print(f'get_basename arg is not path ... {file_path}')
            return None
        return os.path.basename(file_path)

    def unfold_path(self, folder_path):
        """
        Split a path into its components.
        
        Args:
            folder_path: Path to split
            
        Returns:
            List of path components
        """
        if not self.check_path(folder_path):
            folder_path = self.default_directory

        parts = folder_path.replace('/', '\\').split('\\')
        return [part for part in parts if part]

    @staticmethod
    def join_path_reverse(folder_list, n=0):
        """
        Join path components from the beginning to n elements from the end.
        
        Args:
            folder_list: List of path components
            n: Number of elements to exclude from the end (if positive)
                or include from the end (if negative)
            
        Returns:
            Joined path
        """
        if not isinstance(folder_list, list):
            return None

        if n == 0:
            return os.path.sep.join(folder_list)
        elif n > 0:
            return os.path.sep.join(folder_list[:-n])
        else:
            return os.path.sep.join(folder_list[:n])

    @staticmethod
    def join_path_forward(folder_list, n=0):
        """
        Join first n path components.
        
        Args:
            folder_list: List of path components
            n: Number of elements to include from the beginning
            
        Returns:
            Joined path
        """
        depth = len(folder_list)
        if depth == 0:
            return None

        n = abs(n)
        if n > 0:
            return os.path.sep.join(folder_list[:min(n, depth)])
        return os.path.sep.join(folder_list)

    # File operations
    @staticmethod
    def is_hidden(filepath):
        """
        Check if a file is hidden.
        
        Args:
            filepath: Path to check
            
        Returns:
            True if file is hidden, False otherwise
        """
        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(filepath))
            assert attrs != -1
            return bool(attrs & 2)  # FILE_ATTRIBUTE_HIDDEN
        except (AssertionError, AttributeError):
            return False

    def is_exist(self, file_path):
        """
        Check if a file exists.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file exists, False otherwise
        """
        return self.check_path(file_path) != PathChecker.RET_NOTHING

    def is_valid(self, file_path):
        """Alias for is_exist for backward compatibility."""
        return self.is_exist(file_path)

    @staticmethod
    def copy_file(source, destination):
        """
        Copy a file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            shutil.copy(source, destination)
            print(f"File copied successfully from '{source}' to '{destination}'")
            return True
        except Exception as e:
            print(f"Error copying file: {e}")
            return False

    @staticmethod
    def move_file(source, destination):
        """
        Move a file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(destination):
                os.remove(destination)
                print(f'Removed existing file: {destination}')

            shutil.move(source, destination)
            print(f"File moved successfully from '{source}' to '{destination}'")
            return True
        except Exception as e:
            print(f"Error moving file: {e}")
            return False

    def delete_file(self, file_path):
        """
        Delete a file.
        
        Args:
            file_path: Path of file to delete
            
        Returns:
            True if successful, False otherwise
        """
        if self.check_path(file_path) == PathChecker.RET_FILE:
            try:
                os.remove(file_path)
                self.debug_print(f"{self.get_basename(file_path)} removed successfully.")
                return True
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        else:
            print(f"The file {file_path} does not exist or is not a file.")
        return False

    def delete_files(self, folder_path, files):
        """
        Delete multiple files from a folder.
        
        Args:
            folder_path: Folder containing files
            files: List of filenames to delete
            
        Returns:
            True if all files deleted successfully, False otherwise
        """
        if self.check_path(folder_path) == PathChecker.RET_FILE:
            folder_path = self.get_dirname(folder_path)

        success = True
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            
            if self.check_path(file_path) == PathChecker.RET_FILE:
                try:
                    os.remove(file_path)
                    self.debug_print(f"{file_name} removed successfully from {folder_path}")
                except Exception as e:
                    print(f"Error deleting {file_name}: {e}")
                    success = False
            else:
                print(f"The file {file_name} does not exist in the folder {folder_path} or is not a file")
                success = False
                
        return success

    def delete_files_in_directory(self, folder_path):
        """
        Delete all files in a directory.
        
        Args:
            folder_path: Directory to clean
            
        Returns:
            True if successful, False otherwise
        """
        if self.check_path(folder_path) == PathChecker.RET_DIR:
            files = os.listdir(folder_path)
            self.debug_print(f"Deleting files in directory: {files}")
            return self.delete_files(folder_path, files)
        else:
            print(f"Cannot delete files: {folder_path} is not a directory")
            return False

    @staticmethod
    def empty_directory(directory):
        """
        Remove all files and subdirectories from a directory.
        
        Args:
            directory: Directory to empty
        """
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove the file
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove the directory
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    # UI methods
    @staticmethod
    def ask_yes_no_question(message=''):
        """
        Show a yes/no dialog box.
        
        Args:
            message: Message to display
            
        Returns:
            True if user chose Yes, False otherwise
        """
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        try:
            response = messagebox.askyesno("Confirm", f"Do you want to proceed? {message}")
            return response
        finally:
            root.destroy()

    def select_folder(self, initial_dir=''):
        """
        Show a folder selection dialog.
        
        Args:
            initial_dir: Initial directory to show
            
        Returns:
            Selected folder path or empty string if canceled
        """
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        if not initial_dir:
            initial_dir = self.default_directory

        folder_path = filedialog.askdirectory(initialdir=initial_dir)
        
        if folder_path:
            self.debug_print(f"Selected folder: {folder_path}")
        else:
            self.debug_print("No folder selected.")

        return folder_path

    # Directory listing methods
    @staticmethod
    def list_directory_contents(path):
        """
        List all files and folders in a directory.
        
        Args:
            path: Directory to list
            
        Returns:
            List of all entries or error message
        """
        try:
            return os.listdir(path)
        except FileNotFoundError:
            return f"The directory '{path}' does not exist."
        except PermissionError:
            return f"Permission denied to access the directory '{path}'."
        except Exception as e:
            return f"An error occurred: {e}"

    @staticmethod
    def list_non_hidden_directories(path):
        """
        List non-hidden directories in a path.
        
        Args:
            path: Directory to list
            
        Returns:
            List of non-hidden directories or error message
        """
        try:
            entries = os.listdir(path)
            directories = [
                entry for entry in entries
                if os.path.isdir(os.path.join(path, entry)) and not entry.startswith('.')
            ]
            return directories
        except FileNotFoundError:
            return f"The directory '{path}' does not exist."
        except PermissionError:
            return f"Permission denied to access the directory '{path}'."
        except Exception as e:
            return f"An error occurred: {e}"

    def list_hidden_directories(self, path):
        """
        List hidden directories in a path.
        
        Args:
            path: Directory to list
            
        Returns:
            List of hidden directory names or error message
        """
        try:
            entries = os.listdir(path)
            hidden_directories = [
                entry for entry in entries
                if os.path.isdir(os.path.join(path, entry)) and 
                   self.is_hidden(os.path.join(path, entry))
            ]
            return hidden_directories
        except FileNotFoundError:
            return f"The directory '{path}' does not exist."
        except PermissionError:
            return f"Permission denied to access the directory '{path}'."
        except Exception as e:
            return f"An error occurred: {e}"

    def list_directories_only(self, path):
        """
        List non-hidden directories only.
        
        Args:
            path: Directory to list
            
        Returns:
            List of directories or error message
        """
        dir_non_hidden = self.list_non_hidden_directories(path)
        dir_hidden = self.list_hidden_directories(path)

        if isinstance(dir_non_hidden, str) or isinstance(dir_hidden, str):
            return "An error occurred while fetching directories."

        return [d for d in dir_non_hidden if d not in dir_hidden]

    @staticmethod
    def get_last_path_component(path):
        """
        Get the last component of a path.
        
        Args:
            path: Path to parse
            
        Returns:
            Last path component
        """
        return os.path.basename(os.path.normpath(path))

    # Debugging
    def debug_print(self, message):
        """
        Print debug information if debug mode is enabled.
        
        Args:
            message: Message to print
        """
        if self.debug_mode:
            if "*-@#$%&" in message:
                print(message * 180)
            else:
                print(message)

    # Input blocking control for special operations
    @staticmethod
    def block_user_input():
        """Block user input using Windows API."""
        user32 = ctypes.windll.user32
        user32.BlockInput(True)

    @staticmethod
    def unblock_user_input():
        """Unblock user input using Windows API."""
        user32 = ctypes.windll.user32
        user32.BlockInput(False)


# Example usage
if __name__ == "__main__":
    file_manager = FileManager()
    jpg_files = file_manager.get_jpg_filter(".", "a1*.jpg")
    file_count = len(jpg_files)
    
    print("Number of jpg files:", file_count)
    if file_count == 4:
        print("-- include dangye --")
    else:
        print("-- exclude dangye --")

    jpg_files = file_manager.get_jpg_filter(".", "a*.jpg")
    if jpg_files:
        last_file = jpg_files[-1]
        well = int(last_file[1])
        print("Last file indicator:", well)
