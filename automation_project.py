"""
Python Automation Script Project
Smart File Management and Cleaning System Using Python Automation
"""

# ---------------------------------------------------------------------------
# Import required modules for file handling, moving, logging, and timestamps.
# ---------------------------------------------------------------------------
import logging
import os
import shutil
from datetime import datetime


# ---------------------------------------------------------------------------
# Function: configure_logging
# Purpose : Configure logging for both console output and file storage.
# ---------------------------------------------------------------------------
def configure_logging(log_file_path):
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )


# ---------------------------------------------------------------------------
# Function: safe_input
# Purpose : Safely collect user input and handle keyboard interruptions.
# ---------------------------------------------------------------------------
def safe_input(message):
    """Return user input safely."""
    try:
        return input(message).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nInput interrupted by user.")
        logging.warning("User interrupted the input operation.")
        return ""


# ---------------------------------------------------------------------------
# Function: get_valid_directory
# Purpose : Ask the user for a valid existing directory path.
# ---------------------------------------------------------------------------
def get_valid_directory():
    """Prompt the user until a valid directory path is entered."""
    while True:
        directory = safe_input("Enter the full directory path for automation: ")

        # Validate empty input before checking the directory path.
        if not directory:
            print("Directory path cannot be empty. Please try again.")
            continue

        # Verify that the given path points to an existing directory.
        if os.path.isdir(directory):
            return os.path.abspath(directory)

        print("Invalid directory path. Please enter a valid folder path.")


# ---------------------------------------------------------------------------
# Function: get_non_empty_prefix
# Purpose : Collect a valid prefix for file renaming.
# ---------------------------------------------------------------------------
def get_non_empty_prefix():
    """Return a non-empty prefix for file renaming."""
    while True:
        prefix = safe_input("Enter a prefix for renaming files: ")

        # The prefix should not be blank because it is used in file names.
        if prefix:
            return prefix

        print("Prefix cannot be empty. Please enter a valid prefix.")


# ---------------------------------------------------------------------------
# Function: get_yes_no_choice
# Purpose : Standard yes/no input helper for user confirmation.
# ---------------------------------------------------------------------------
def get_yes_no_choice(message):
    """Return True for yes and False for no after validation."""
    while True:
        choice = safe_input(message).lower()

        # Accept common yes responses.
        if choice in {"yes", "y"}:
            return True

        # Accept common no responses.
        if choice in {"no", "n"}:
            return False

        print("Please enter yes or no.")


# ---------------------------------------------------------------------------
# Function: print_menu
# Purpose : Display the available automation operations to the user.
# ---------------------------------------------------------------------------
def print_menu():
    """Display the main menu."""
    print("\n" + "=" * 60)
    print("PYTHON AUTOMATION SCRIPT - SMART FILE MANAGEMENT SYSTEM")
    print("=" * 60)
    print("1. Preview directory contents")
    print("2. Organize files by extension")
    print("3. Rename files with a custom prefix")
    print("4. Sort files by size")
    print("5. Clean temporary and junk files")
    print("6. Remove empty folders")
    print("7. Create backup")
    print("8. Run complete automation")
    print("9. Exit")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Class: FileAutomationProject
# Purpose: Encapsulate all file automation features for the project.
# ---------------------------------------------------------------------------
class FileAutomationProject:
    """A menu-driven automation system for file management."""

    # -----------------------------------------------------------------------
    # Method: __init__
    # Purpose: Initialize project configuration and counters.
    # -----------------------------------------------------------------------
    def __init__(self, base_directory):
        """Initialize project settings."""
        self.base_directory = os.path.abspath(base_directory)
        self.generated_directory_names = {
            "Documents",
            "Images",
            "Videos",
            "Audio",
            "Archives",
            "Scripts",
            "Others",
            "Size_Sorted",
        }
        self.category_extensions = {
            "Documents": {".pdf", ".doc", ".docx", ".txt", ".csv", ".xlsx", ".ppt", ".pptx"},
            "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"},
            "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv"},
            "Audio": {".mp3", ".wav", ".aac", ".flac"},
            "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
            "Scripts": {".py", ".js", ".java", ".c", ".cpp", ".html", ".css"},
        }
        self.summary = {
            "organized": 0,
            "renamed": 0,
            "size_sorted": 0,
            "cleaned": 0,
            "removed_folders": 0,
            "backup_created": False,
        }

    # -----------------------------------------------------------------------
    # Method: unique_destination_path
    # Purpose: Prevent overwriting by creating unique file names.
    # -----------------------------------------------------------------------
    def unique_destination_path(self, destination_directory, file_name):
        """Return a unique file path inside the destination directory."""
        base_name, extension = os.path.splitext(file_name)
        candidate_path = os.path.join(destination_directory, file_name)
        counter = 1

        # Keep generating new names until a free destination is found.
        while os.path.exists(candidate_path):
            candidate_path = os.path.join(
                destination_directory,
                f"{base_name}_{counter}{extension}",
            )
            counter += 1

        return candidate_path

    # -----------------------------------------------------------------------
    # Method: classify_file
    # Purpose: Decide the target category based on file extension.
    # -----------------------------------------------------------------------
    def classify_file(self, extension):
        """Return the folder category for the given file extension."""
        lower_extension = extension.lower()

        # Search through known extension groups first.
        for category, extensions in self.category_extensions.items():
            if lower_extension in extensions:
                return category

        # Unknown file extensions are grouped into Others.
        return "Others"

    # -----------------------------------------------------------------------
    # Method: classify_size
    # Purpose: Classify files into size categories for sorting.
    # -----------------------------------------------------------------------
    def classify_size(self, file_path):
        """Return the size folder name for a file."""
        file_size = os.path.getsize(file_path)

        # Files smaller than 1 MB are labeled small.
        if file_size < 1 * 1024 * 1024:
            return "Small_Files"

        # Files between 1 MB and 10 MB are labeled medium.
        if file_size < 10 * 1024 * 1024:
            return "Medium_Files"

        # Files above 10 MB are labeled large.
        return "Large_Files"

    # -----------------------------------------------------------------------
    # Method: iter_candidate_files
    # Purpose: Yield files while skipping selected automation folders.
    # -----------------------------------------------------------------------
    def iter_candidate_files(self, excluded_directories=None):
        """Yield file paths that are eligible for automation."""
        excluded_directories = set(excluded_directories or [])

        for root, dirs, files in os.walk(self.base_directory):
            # Exclude only the folders requested by the caller.
            dirs[:] = [
                directory
                for directory in dirs
                if directory not in excluded_directories
            ]

            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Skip the project log file to avoid moving active logs.
                if os.path.basename(file_path) == "automation.log":
                    continue

                yield file_path

    # -----------------------------------------------------------------------
    # Method: preview_directory_contents
    # Purpose: Display a quick summary of files and folders before execution.
    # -----------------------------------------------------------------------
    def preview_directory_contents(self):
        """Print a short directory preview for the user."""
        file_count = 0
        folder_count = 0

        # Walk through the directory tree and count files and folders.
        for _, dirs, files in os.walk(self.base_directory):
            folder_count += len(dirs)
            file_count += len(files)

        print(f"\nSelected directory: {self.base_directory}")
        print(f"Total folders found: {folder_count}")
        print(f"Total files found  : {file_count}")
        logging.info("Preview completed for directory: %s", self.base_directory)

    # -----------------------------------------------------------------------
    # Method: create_category_directories
    # Purpose: Create target folders used for file organization.
    # -----------------------------------------------------------------------
    def create_category_directories(self):
        """Create standard category directories if they do not exist."""
        for category in list(self.category_extensions.keys()) + ["Others"]:
            category_path = os.path.join(self.base_directory, category)
            os.makedirs(category_path, exist_ok=True)

        logging.info("Category folders are ready.")

    # -----------------------------------------------------------------------
    # Method: organize_files_by_extension
    # Purpose: Move files into category folders based on their extension.
    # -----------------------------------------------------------------------
    def organize_files_by_extension(self):
        """Organize files by their extension categories."""
        self.create_category_directories()

        for file_path in list(self.iter_candidate_files(self.generated_directory_names)):
            try:
                # Determine the correct target category for the file.
                _, extension = os.path.splitext(file_path)
                category = self.classify_file(extension)
                destination_directory = os.path.join(self.base_directory, category)
                destination_path = self.unique_destination_path(
                    destination_directory,
                    os.path.basename(file_path),
                )

                # Skip files that already exist at the same destination path.
                if os.path.abspath(file_path) == os.path.abspath(destination_path):
                    continue

                shutil.move(file_path, destination_path)
                self.summary["organized"] += 1
                logging.info("Moved file: %s -> %s", file_path, destination_path)
            except Exception as error:
                logging.error("Failed to organize file %s: %s", file_path, error)

        print("Files organized by extension successfully.")

    # -----------------------------------------------------------------------
    # Method: rename_files_with_prefix
    # Purpose: Rename files systematically using a user-provided prefix.
    # -----------------------------------------------------------------------
    def rename_files_with_prefix(self, prefix):
        """Rename files using the provided prefix."""
        serial_number = 1

        for root, _, files in os.walk(self.base_directory):
            for file_name in files:
                try:
                    # Skip the log file so logging remains stable.
                    if file_name == "automation.log":
                        continue

                    old_path = os.path.join(root, file_name)
                    _, extension = os.path.splitext(file_name)
                    new_name = f"{prefix}_{serial_number:03d}{extension}"
                    new_path = self.unique_destination_path(root, new_name)

                    # Avoid renaming a file to the same path.
                    if os.path.abspath(old_path) == os.path.abspath(new_path):
                        serial_number += 1
                        continue

                    os.rename(old_path, new_path)
                    self.summary["renamed"] += 1
                    serial_number += 1
                    logging.info("Renamed file: %s -> %s", old_path, new_path)
                except Exception as error:
                    logging.error("Failed to rename file %s: %s", file_name, error)

        print("Files renamed successfully.")

    # -----------------------------------------------------------------------
    # Method: sort_files_by_size
    # Purpose: Move files into size-based folders.
    # -----------------------------------------------------------------------
    def sort_files_by_size(self):
        """Copy files into small, medium, and large size folders."""
        size_root = os.path.join(self.base_directory, "Size_Sorted")
        os.makedirs(size_root, exist_ok=True)

        for folder_name in ["Small_Files", "Medium_Files", "Large_Files"]:
            os.makedirs(os.path.join(size_root, folder_name), exist_ok=True)

        for file_path in list(self.iter_candidate_files({"Size_Sorted"})):
            try:
                # Determine the target size folder for the current file.
                size_folder = self.classify_size(file_path)
                destination_directory = os.path.join(size_root, size_folder)
                destination_path = self.unique_destination_path(
                    destination_directory,
                    os.path.basename(file_path),
                )

                shutil.copy2(file_path, destination_path)
                self.summary["size_sorted"] += 1
                logging.info("Copied file to size folder: %s -> %s", file_path, destination_path)
            except Exception as error:
                logging.error("Failed to sort file by size %s: %s", file_path, error)

        print("Files sorted by size successfully.")

    # -----------------------------------------------------------------------
    # Method: clean_temporary_files
    # Purpose: Delete temporary and junk files from the directory tree.
    # -----------------------------------------------------------------------
    def clean_temporary_files(self):
        """Delete temporary files from the project directory."""
        temporary_extensions = {".tmp", ".temp", ".bak", ".old", ".dmp"}
        temporary_names = {"thumbs.db", ".ds_store", "desktop.ini"}

        for file_path in list(self.iter_candidate_files()):
            try:
                file_name = os.path.basename(file_path)
                _, extension = os.path.splitext(file_name)

                # Delete files that match temporary patterns.
                if extension.lower() in temporary_extensions or file_name.lower() in temporary_names:
                    os.remove(file_path)
                    self.summary["cleaned"] += 1
                    logging.info("Deleted temporary file: %s", file_path)
            except Exception as error:
                logging.error("Failed to delete temporary file %s: %s", file_path, error)

        print("Temporary files cleaned successfully.")

    # -----------------------------------------------------------------------
    # Method: remove_empty_folders
    # Purpose: Remove folders that no longer contain any files or folders.
    # -----------------------------------------------------------------------
    def remove_empty_folders(self):
        """Remove empty folders from the directory tree."""
        for root, dirs, _ in os.walk(self.base_directory, topdown=False):
            for directory in dirs:
                folder_path = os.path.join(root, directory)

                try:
                    # Only delete folders that are completely empty.
                    if not os.listdir(folder_path):
                        os.rmdir(folder_path)
                        self.summary["removed_folders"] += 1
                        logging.info("Removed empty folder: %s", folder_path)
                except Exception as error:
                    logging.error("Failed to remove folder %s: %s", folder_path, error)

        print("Empty folders removed successfully.")

    # -----------------------------------------------------------------------
    # Method: create_backup
    # Purpose: Create a full backup of the selected directory.
    # -----------------------------------------------------------------------
    def create_backup(self):
        """Create a timestamped backup copy of the base directory."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            parent_directory = os.path.dirname(self.base_directory)
            base_name = os.path.basename(self.base_directory)
            backup_directory = os.path.join(
                parent_directory,
                f"{base_name}_BACKUP_{timestamp}",
            )

            # Copy the entire directory to a safe backup location.
            shutil.copytree(self.base_directory, backup_directory)
            self.summary["backup_created"] = True
            logging.info("Backup created at: %s", backup_directory)
            print("Backup created successfully.")
        except Exception as error:
            logging.error("Failed to create backup: %s", error)
            print("Backup could not be created.")

    # -----------------------------------------------------------------------
    # Method: display_summary
    # Purpose: Print a final summary of all automation operations.
    # -----------------------------------------------------------------------
    def display_summary(self):
        """Display the summary of all completed operations."""
        print("\n" + "-" * 22 + " AUTOMATION SUMMARY " + "-" * 22)
        print(f"Files organized   : {self.summary['organized']}")
        print(f"Files renamed     : {self.summary['renamed']}")
        print(f"Files size-sorted : {self.summary['size_sorted']}")
        print(f"Files cleaned     : {self.summary['cleaned']}")
        print(f"Folders removed   : {self.summary['removed_folders']}")
        print(f"Backup created    : {'Yes' if self.summary['backup_created'] else 'No'}")
        print("-" * 64)

    # -----------------------------------------------------------------------
    # Method: run_complete_automation
    # Purpose: Execute the full workflow in a single operation.
    # -----------------------------------------------------------------------
    def run_complete_automation(self, prefix, run_backup, run_size_sort):
        """Run the main automation steps in a complete workflow."""
        if run_backup:
            self.create_backup()

        self.organize_files_by_extension()
        self.rename_files_with_prefix(prefix)

        if run_size_sort:
            self.sort_files_by_size()

        self.clean_temporary_files()
        self.remove_empty_folders()
        self.display_summary()


# ---------------------------------------------------------------------------
# Function: main
# Purpose : Entry point for the menu-driven automation project.
# ---------------------------------------------------------------------------
def main():
    """Run the complete interactive automation project."""
    print("\n" + "=" * 60)
    print("WELCOME TO THE PYTHON AUTOMATION SCRIPT PROJECT")
    print("=" * 60)

    # Ask the user for the working directory before configuring the project.
    base_directory = get_valid_directory()
    log_file_path = os.path.join(base_directory, "automation.log")
    configure_logging(log_file_path)
    logging.info("Application started for base directory: %s", base_directory)

    project = FileAutomationProject(base_directory)

    while True:
        print_menu()
        choice = safe_input("Choose an option: ")

        try:
            # Option 1 previews the folder contents.
            if choice == "1":
                project.preview_directory_contents()

            # Option 2 organizes files by extension category.
            elif choice == "2":
                project.organize_files_by_extension()
                project.display_summary()

            # Option 3 renames files using a user-defined prefix.
            elif choice == "3":
                prefix = get_non_empty_prefix()
                project.rename_files_with_prefix(prefix)
                project.display_summary()

            # Option 4 creates a size-based sorted copy of files.
            elif choice == "4":
                project.sort_files_by_size()
                project.display_summary()

            # Option 5 removes temporary files from the directory.
            elif choice == "5":
                project.clean_temporary_files()
                project.display_summary()

            # Option 6 removes empty folders after cleanup.
            elif choice == "6":
                project.remove_empty_folders()
                project.display_summary()

            # Option 7 creates a backup of the selected folder.
            elif choice == "7":
                project.create_backup()
                project.display_summary()

            # Option 8 runs the entire project workflow.
            elif choice == "8":
                prefix = get_non_empty_prefix()
                run_backup = get_yes_no_choice(
                    "Do you want to create a backup before automation? (yes/no): "
                )
                run_size_sort = get_yes_no_choice(
                    "Do you want to sort files by size too? (yes/no): "
                )
                project.run_complete_automation(prefix, run_backup, run_size_sort)

            # Option 9 exits the application cleanly.
            elif choice == "9":
                logging.info("Application closed by user.")
                print("Exiting the Python Automation Script Project. Thank you.")
                break

            # Handle invalid menu choices politely.
            else:
                print("Invalid choice. Please select a valid menu option.")
        except Exception as error:
            logging.exception("Unexpected error while handling choice %s", choice)
            print(f"An unexpected error occurred: {error}")


# ---------------------------------------------------------------------------
# Standard Python entry point for running the project as a script.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
