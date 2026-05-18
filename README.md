# Python Automation Script Project Report

## Project Title
**Smart File Management and Cleaning System Using Python Automation**

## Introduction
Python automation is widely used to reduce repetitive manual work in computer systems. In day-to-day file handling, users often face problems such as scattered files, inconsistent file names, temporary junk files, and unorganized folders. This mini project presents a professional Python automation script that can automatically organize files, rename them, sort them, clean unwanted items, and generate logs for easy tracking.

This report is written in English and formatted in a professional structure so it can be directly adapted into a DOCX or PDF college project submission.

## Objective
The main objective of this project is to develop a detailed Python automation script that:

- accepts user input,
- organizes files into folders,
- renames files systematically,
- sorts files based on extension and size,
- removes temporary and unnecessary files,
- logs all actions performed by the system, and
- handles errors using exception handling.

## Problem Statement
Managing large numbers of files manually is time-consuming and error-prone. Students, office staff, and computer users often store files in one location without proper naming or folder structure. As a result, files become difficult to find, duplicate files remain unnoticed, and temporary files occupy unnecessary storage space.

This project solves the problem by building a Python-based automation system that can intelligently manage file operations in a user-selected directory with minimal human effort.

## Features
- User-friendly menu-driven program
- Accepts directory path and operation choices from the user
- Uses the **OS module** for file and folder handling
- Uses the **shutil module** for moving and copying files
- Uses **logging** for activity tracking
- Uses **exception handling** for reliability
- Renames files with a custom prefix
- Sorts files into categories such as documents, images, videos, audio, archives, and scripts
- Organizes files into dedicated folders automatically
- Cleans temporary and junk files
- Removes empty folders
- Creates a backup of the selected directory
- Displays a final automation summary report

## Technologies Used
- **Programming Language:** Python 3
- **Libraries/Modules:** `os`, `shutil`, `logging`, `datetime`
- **Concepts Used:** automation, file handling, user input, exception handling, logging, menu-driven programming

## System Requirements
### Hardware Requirements
- Computer or laptop
- Minimum 2 GB RAM
- Minimum 100 MB free disk space

### Software Requirements
- Python 3.8 or above
- Any code editor (VS Code, PyCharm, IDLE, or similar)
- Windows, Linux, or macOS operating system

## Step-by-step Working Process
1. The user runs the Python script.
2. The program asks the user to enter the directory path.
3. The program validates whether the directory exists.
4. Logging is configured so all automation steps are saved in a log file.
5. The user chooses operations from a menu.
6. The script scans all files in the selected directory.
7. Files are organized into folders based on their type.
8. Files can be renamed using a custom prefix.
9. Files can be sorted into size-based folders.
10. Temporary and junk files are deleted.
11. Empty folders are removed.
12. A backup copy of the selected directory can be created.
13. A final summary is displayed showing the work completed.

## Complete Python Source Code
The complete, detailed, commented source code for this project is provided in:

**`automation_project.py`**

The source file contains more than 300 lines of Python code and includes:
- full comments for every major section,
- user input functionality,
- file renaming,
- sorting,
- organizing,
- cleaning,
- logging,
- exception handling,
- and a menu-driven workflow suitable for a college mini project.

## Explanation of Every Function
### 1. `configure_logging(log_file_path)`
Configures the logging system and stores all automation events in a log file as well as on the console.

### 2. `safe_input(message)`
Takes input from the user safely and handles unexpected keyboard interruption or end-of-file errors.

### 3. `get_valid_directory()`
Asks the user for a folder path and checks whether it is a valid directory before proceeding.

### 4. `get_non_empty_prefix()`
Collects a prefix value from the user for the file renaming feature.

### 5. `get_yes_no_choice(message)`
Collects yes/no responses from the user in a validated format.

### 6. `print_menu()`
Displays the main project menu and shows all automation options available to the user.

### 7. `unique_destination_path(destination_directory, file_name)`
Creates a unique destination path so that files are not overwritten if another file with the same name already exists.

### 8. `classify_file(extension)`
Determines the category of a file by checking its extension and assigning it to the correct folder.

### 9. `classify_size(file_path)`
Checks the file size and returns whether the file belongs in the small, medium, or large category.

### 10. `preview_directory_contents()`
Shows a preview of files and folders in the selected directory before automation tasks are executed.

### 11. `create_category_directories()`
Creates standard folders such as Documents, Images, Videos, and Others where files can be moved.

### 12. `organize_files_by_extension()`
Moves files into category folders based on their extension and keeps the directory more organized.

### 13. `rename_files_with_prefix(prefix)`
Renames all eligible files using the custom prefix entered by the user.

### 14. `sort_files_by_size()`
Copies files into size-based folders such as Small_Files, Medium_Files, and Large_Files so the original organized files remain available in their category folders.

### 15. `clean_temporary_files()`
Deletes temporary and junk files that match the exact rules used in the script: extensions `.tmp`, `.temp`, `.bak`, `.old`, `.dmp` and file names `thumbs.db`, `.ds_store`, and `desktop.ini`.

### 16. `remove_empty_folders()`
Deletes folders that no longer contain files after the organization and cleaning process.

### 17. `create_backup()`
Creates a full backup copy of the selected directory in a separate backup location.

### 18. `display_summary()`
Shows the total number of files organized, renamed, sorted, cleaned, and folders removed.

### 19. `run_complete_automation(prefix, run_backup, run_size_sort)`
Runs the complete automation workflow in one sequence for convenience.

### 20. `main()`
Acts as the entry point of the program, coordinating user input, menu display, and task execution.

## Sample Input and Output
### Sample Input
```text
Enter the full directory path for automation: /home/student/demo_folder
Choose an option: 8
Enter a prefix for renaming files: college_project
Do you want to create a backup before automation? (yes/no): yes
Do you want to sort files by size too? (yes/no): yes
```

### Sample Output
```text
============================================================
PYTHON AUTOMATION SCRIPT - SMART FILE MANAGEMENT SYSTEM
============================================================
Selected directory: /home/student/demo_folder
Backup created successfully.
Files organized by extension successfully.
Files renamed successfully.
Files sorted by size successfully.
Temporary files cleaned successfully.
Empty folders removed successfully.

---------------- AUTOMATION SUMMARY ----------------
Files organized : 12
Files renamed   : 12
Files size-sorted: 12
Files cleaned   : 4
Folders removed : 3
Backup created  : Yes
---------------------------------------------------
```

## Advantages
- Saves time and manual effort
- Improves file organization
- Reduces clutter in storage locations
- Helps users quickly locate files
- Provides automatic logging for transparency
- Demonstrates practical use of Python modules in a real-world project

## Disadvantages
- Incorrect folder selection by the user may affect unintended files
- File organization rules are based mainly on extensions
- Some users may require customization for special file categories
- Backup creation can take extra time for very large directories

## Future Improvements
- Add a graphical user interface (GUI) using Tkinter or PyQt
- Add duplicate file detection
- Add scheduling using task automation tools
- Export automation summaries to PDF or Excel
- Add checksum-based verification before deleting files
- Add configuration support through JSON or YAML files

## Conclusion
This Python Automation Script project demonstrates how Python can be used to solve practical file management problems in a simple and effective way. The project combines user input, file organization, renaming, sorting, cleaning, logging, and exception handling into one complete mini project. Because of its structured design and detailed code, it is highly suitable for college-level academic submission and can also serve as a base for future advanced automation systems.
