import os
import subprocess
import random
import string
import argparse
import shutil
import logging


class DriveFiller:
    def __init__(self, root:str, 
                 file_min_size:int, file_max_size:int, 
                 file_prefix:str, file_suffix:str, file_extension:str,
                 file_use_progressive:bool, subdirectories:bool,
                 subdirectory_min_files:int, subdirectory_max_files:int,
                 subdirectory_prefix:str, subdirectory_suffix:str,
                 subdirectory_use_progressive:bool,
                 zero_bytes:bool,
                 dry_run:bool = True) -> None:
        self.log = self._configure_logging()

        self.root = root
        self.file_min_size = max(1, file_min_size)
        self.file_max_size = max(self.file_min_size, file_max_size)
        self.file_prefix = file_prefix
        self.file_suffix = file_suffix
        self.file_extension = file_extension.replace(" ", "")
        self.file_extension = self.file_extension if self.file_extension.startswith(".") else "." + self.file_extension
        self.file_use_progressive = file_use_progressive
        self.subdirectories = subdirectories
        self.subdirectory_min_files = max(1, subdirectory_min_files)
        self.subdirectory_max_files = max(self.subdirectory_min_files, subdirectory_max_files)
        self.subdirectory_prefix = subdirectory_prefix
        self.subdirectory_suffix = subdirectory_suffix
        self.subdirectory_use_progressive = subdirectory_use_progressive
        self.zero_bytes = zero_bytes
        self.dry_run = dry_run


    def run(self) -> None:
        """
        Run the random file generation and zero-filling process.
        """

        self._fill()
        self._zero()


    def _fill(self) -> None:
        """
        Fill the root directory specified during the class initialization with random files.

        If subdirectories are enabled, this function creates random subdirectories inside the root directory.
        For each subdirectory, a random number of files is created.

        If subdirectories are disabled, files are created directly in the root directory.
        """

        self._create_directory(self.root)

        dir_i = 0
        while True:
            path = self._create_random_subdirectory(dir_i, self.root) if self.subdirectories else self.root
            dir_i += 1

            for file_i in range(random.randint(self.subdirectory_min_files, self.subdirectory_max_files)):
                if not self._create_random_file(file_i, path):
                    return
                
            if self.dry_run and dir_i == 3: # just making sure the process stops in dry-run mode
                return
                
    
    def _zero(self) -> None:
        """
        If the functionality is enabled, this function create a directory "zero" populated with one single file
        filling the remaining free space on the disk.
        """

        if self.zero_bytes:
            zero_path = os.path.join(self.root, "zero")
            self._create_directory(zero_path)
            self._create_random_file(0, zero_path, shutil.disk_usage(zero_path).free)


    def _generate_random_string(self, length = 20) -> str:
        """
        Generate a random string of given length.

        Parameters:
        - length (int): The length of the random string. Default is 20.

        Returns:
        str: A randomly generated string.
        """

        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


    def _create_random_file(self, i:int, path:str, size:int = -1) -> bool:
        """
        Create a random file.

        Parameters:
        - i (int): An index or unique identifier for the file.
        - path (str): The path where the file will be created.
        - size (int): The size of the random file. Default -1 equals random file size.

        Returns:
        bool: True if the file creation is successful, False otherwise.
        """

        unique_name = str(i) if self.file_use_progressive else self._generate_random_string()

        file_path = os.path.join(path,  f"{self.file_prefix}{unique_name}{self.file_suffix}{self.file_extension}")
        file_size = size if size > 0 else random.randint(self.file_min_size, self.file_max_size)

        return self._create_file(file_path, file_size)
            

    def _create_file(self, file_path:str, file_size:int) -> bool:
        """
        Create a file with the specified path and size using the fsutil command.

        Parameters:
        - file_path (str): The full path, including the filename, where the new file will be created.
        - file_size (int): The size of the new file in bytes.

        Returns:
        bool: True if the file creation is successful, False otherwise.
        """

        self.log.info(f"creating file {file_path}...")

        if self.dry_run:
            return True
        
        try:
            result  = subprocess.run(["fsutil", "file", "createnew", file_path, str(file_size)])
            return True if result.returncode == 0 else False
        except subprocess.CalledProcessError as e:
            return False


    def _create_random_subdirectory(self, i:int, path:str) -> str:
        """
        Create a random subdirectory.

        Parameters:
        - i (int): An index or unique identifier for the subdirectory.
        - path (str): The path where the subdirectory will be created.

        Returns:
        str: The path of the created subdirectory.
        """

        unique_name = str(i) if self.subdirectory_use_progressive else self._generate_random_string()

        subdirectory_path = os.path.join(path, f"{self.subdirectory_prefix}{unique_name}{self.subdirectory_suffix}")
        self._create_directory(subdirectory_path)
        return subdirectory_path


    def _create_directory(self, path:str) -> None:
        """
        Create a file with the specified path.

        Parameters:
        - path (str): The full path, including the  directory name, where the new directory will be created.
        """

        self.log.info(f"creating directory {path}...")

        if not self.dry_run:
            os.makedirs(path, exist_ok=True)


    def _configure_logging(self):
        """
        Configure logging for the script.
        """

        log = logging.getLogger("DriveFiller")
        log.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s'))
        log.addHandler(console_handler)
        return log


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random files to fill the drive.")
    parser.add_argument("--root", type=str, default="C:\\fill", help="Root directory where random files will be generated.")
    parser.add_argument("--file-min-size", type=int, default=500 * 1024**2, help="Minimum size for a file in bytes (default: 500 MB).")
    parser.add_argument("--file-max-size", type=int, default=5 * 1024**3, help="Maximum size for a file in bytes (default: 5 GB).")
    parser.add_argument("--file-prefix", type=str, default="", help="Prefix for each file.")
    parser.add_argument("--file-suffix", type=str, default="", help="Suffix for each file.")
    parser.add_argument("--file-extension", type=str, default=".bin", help="Extension for each file.")
    parser.add_argument("--file-use-progressive", action="store_true", help="Use a progressive value for uniqueness in file names (default: random alphanumeric string).")
    parser.add_argument("--subdirectories", action="store_true", help="Split files into different subdirectories.")
    parser.add_argument("--subdirectory-min-files", type=int, default=10, help="Minimum number of files for each subdirectory.")
    parser.add_argument("--subdirectory-max-files", type=int, default=50, help="Maximum number of files for each subdirectory.")
    parser.add_argument("--subdirectory-prefix", type=str, default="", help="Prefix for each subdirectory.")
    parser.add_argument("--subdirectory-suffix", type=str, default="", help="Suffix for each subdirectory.")
    parser.add_argument("--subdirectory-use-progressive", action="store_true", help="Use a progressive value for uniqueness in subdirectory names (default: random alphanumeric string).")
    parser.add_argument("--zero", action="store_true", help="Generate one last file that fills the remaining space on the drive.")
    parser.add_argument("--dry-run", action="store_true", help="Print what the script would do without actually creating files or directories.")
    args = parser.parse_args()

    filler = DriveFiller(args.root, 
                         args.file_min_size, args.file_max_size,
                         args.file_prefix, args.file_suffix, args.file_extension,
                         args.file_use_progressive, args.subdirectories,
                         args.subdirectory_min_files, args.subdirectory_max_files,
                         args.subdirectory_prefix, args.subdirectory_suffix,
                         args.subdirectory_use_progressive,
                         args.zero,
                         args.dry_run)
    filler.run()
