# Drive Filler Tool

## Description

The Drive Filler Tool generates random files to fill up a specified drive in few seconds.

## Table of Contents:

- [Drive Filler Tool](#drive-filler-tool)
  - [Description](#description)
  - [Table of Contents:](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Options](#options)
  - [Example](#example)
  - [Expandability and customization](#expandability-and-customization)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- Generate random files with varying sizes between a specified minimum and maximum.
- Option to group files in subdirectories.
- Allow customization of files and subdirectory names with prefixes, suffixes, and progressive or random alphanumeric strings.

## Requirements
- Python 3.x
- Windows operating system (for `fsutil` command) 

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sim1angeloni/drive-filler-tool.git
   cd drive-filler-tool
	```

> This tool can be run from any location of your choice. You have the flexibility to save the files wherever you prefer.

## Usage

```bash
python drive_filler.py <OPTIONS>
```

Configure the tool with the [options](#options) that you need.

## Options

- `--root`: Root directory where random files will be generated.
- `--file-min-size`: Minimum size for a file in bytes (default: 500 MB).
- `--file-max-size`: Maximum size for a file in bytes (default: 5 GB).
- `--file-prefix`: Prefix for each file.
- `--file-suffix`: Suffix for each file.
- `--file-extension`: Extension for each file.
- `--file-use-progressive`: Use a progressive value for uniqueness in file names (default: random alphanumeric string).
- `--subdirectories`: Split files into different subdirectories.
- `--subdirectory-min-files`: Minimum number of files for each subdirectory.
- `--subdirectory-max-files`: Maximum number of files for each subdirectory.
- `--subdirectory-prefix`: Prefix for each subdirectory.
- `--subdirectory-suffix`: Suffix for each subdirectory.
- `--subdirectory-use-progressive`: Use a progressive value for uniqueness in subdirectory names (default: random alphanumeric string).
- `--zero`: Generate one last file that fills the remaining space on the drive.
- `--dry-run`: Print what the script would do without actually creating files or directories.

## Example

```python
python drive_filler.py --root "C:\\fill" --file-min-size 524288000 --file-max-size 5368709120 --file-prefix "data_" --file-extension ".txt" --file-use-progressive --subdirectories --subdirectory-min-files 10 --subdirectory-max-files 50 --subdirectory-prefix "subdir_" --subdirectory-suffix "_dir" --zero
```

- Fill the drive `C:\` and put all the files in the directory `fill`.
- The files will be called `data_<N>.txt` where N is a numeric progression starting from 0.
- They will be created inside subdirectories, each will contain a random number between 10 and 50.
- The subdirectories will be called `subdir_<RND>_dir` where RND is an alphanumeric string 20 characters long.
- The system will write a final file as big as the remaining bytes of the disk.

## Expandability and customization

The Drive Filler script is designed to be flexible and easily extendable. If you want to use it under Linux or customize the file creation process, you can create a new class that inherits from the `DriveFiller` class.

For instance, to make the tool working under linux, you just need to override the `_create_file` method.

```python
from drive_filler import DriveFiller

class CustomDriveFiller(DriveFiller):
   def _create_file(self, file_path: str, file_size: int) -> bool:
	   # Add your custom file creation logic here
	   # Example: Use Linux-specific commands or tools
```
	
## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3.  Make your changes and commit them.
4.  Push to your branch: `git push origin feature-name`.
5.  Create a pull request on GitHub.

You can [Report a bug](https://github.com/sim1angeloni/drive-filler-tool/issues/new/choose) too.

## License

This project is licensed under the MIT - see the [LICENSE](https://github.com/sim1angeloni/drive-filler-tool/blob/main/LICENSE) file for details.
