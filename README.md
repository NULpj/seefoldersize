# Folder Size Viewer

This Python script allows you to view the size of folders, subfolders, and files within a specified directory. It provides detailed information about the size of each file and folder, as well as the total size of the directory.

## Features

- View the size of files and directories
- Filter files based on their size and extension
- Option to show detailed information about files and folders
- Option to exclude hidden files/folders
- Customizable size units (bytes, KB, MB, GB)
- Limit the depth of directory scanning

## Requirements

- Python 3.x
- `tabulate` library (for formatting the output)

You can install the required libraries by running:

```bash
pip install -r requirements.txt
```

## Usage

To use the script, run the following command in your terminal:

```bash
python main.py <path> [options]
```

### Options

- `path`: The path to the folder you want to scan.
- `-u`, `--unit`: Specify the size unit (`auto`, `bytes`, `kb`, `mb`, `gb`). Default is `auto`.
- `-d`, `--details`: Show detailed information for all files, not just folders.
- `-t`, `--total-only`: Show only the total size of the folder.
- `--max-depth`: Limit the folder depth to a specified level.
- `--min-size`: Specify the minimum file size (in bytes) to be included in the scan.
- `--exclude-ext`: Exclude files with specified extensions (e.g., `.tmp`, `.log`).
- `--hidden`: Include hidden files and folders.

### License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).
