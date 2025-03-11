import os
import sys
import platform
import zipfile
import subprocess
import importlib
import re
from datetime import datetime

source_dir = ''
dist_dir = ''
acc = 0
exclude_dirs = ["node_modules", "vendor", ".git"]
perm_error = f"Permission denied by {sys.platform} {platform.platform()} {platform.release()}. Recheck your permission."

def prepare(package: str) -> bool:
    """
    Check if 'package' is importable. If not, prompt the user to install.
    Returns True if the package is importable (or installed successfully),
    otherwise False.
    """
    try:
        importlib.import_module(package)
        return True
    except ImportError:
        y = input(f'{package} is necessary and not installed in the system. Prompt "Y" if you want to install it, else the script execution will be aborted: ').strip().lower()
        if y != 'y':
            return False
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            return True
        except PermissionError:
            print(perm_error)
            sys.exit(1)
        except Exception as e:
            print('Error log:\n', e)
            print(f"Failed to install {package}. Exiting.")
            sys.exit(2)

def should_exclude(filepath: str) -> bool:
    """
    Evaluate if the given path should be excluded from compression.
    Returns True if any excluded folder name appears as a full segment in the path,
    or if the path starts with '.git'.
    """
    return any(re.search(rf'(^|[\\/]){re.escape(ex)}([\\/]|$)', filepath) for ex in exclude_dirs) or filepath.startswith('.git')

def zip_dir(src: str, dist: str) -> None:
    start = datetime.now()
    print(Fore.GREEN + "Starting compression...")
    with zipfile.ZipFile(dist, mode='w', compression=zipfile.ZIP_DEFLATED) as z:
        for d, _, fs in os.walk(src):
            print(Fore.BLUE + f'Walking in {d}')
            if should_exclude(d):
                continue
            for f in fs:
                f_path = os.path.join(d, f)
                if should_exclude(f_path):
                    continue
                print(Fore.BLUE + f'Joining {f}')
                z.write(f_path, os.path.relpath(f_path, start=src))
    end = datetime.now()
    print(Fore.GREEN + f'Finished compressing at {end.strftime("%Y-%m-%d %H:%M:%S")} in {(end - start).total_seconds()} seconds')

if __name__ == '__main__':
    for package in ["colorama"]:
        if not prepare(package):
            print("Could not proceed with execution due to missing dependencies. Exiting.")
            sys.exit(1)
    from colorama import Fore, init
    init(autoreset=True)
    while not os.path.exists(source_dir):
        acc += 1
        if acc > 10:
            print(Fore.RED + "You reached the limit of tries. Exiting...")
            sys.exit(2)
        source_dir = input(Fore.CYAN + "Enter the path for the files to be compressed:\n").strip()
        if not source_dir or source_dir == '.':
            source_dir = os.getcwd()
    dist_dir = source_dir
    use_dif_path = input("Prompt 'Y' if you want to use a destination path different from the given root:\n").strip().lower() == 'y'
    if use_dif_path:
        try:
            custom_path = input("Enter the destination:\n").strip()
            if custom_path:
                os.makedirs(custom_path, exist_ok=True)
                dist_dir = custom_path
        except PermissionError as e:
            print(Fore.RED + perm_error + ". The compressed file will be placed at the same root level.")
            dist_dir = source_dir
        except Exception as e:
            print(Fore.RED + "An undefined error occurred. The compressed file will be placed at the same root level.")
            dist_dir = source_dir
    while True:
        add = input(f"Do you want to include additional paths to be skipped?\nCurrently the list is: {exclude_dirs}\n(Press Enter to skip)\n").strip()
        if not add:
            break
        exclude_dirs.append(add)
    zip_file_name = f"{os.path.basename(os.path.normpath(source_dir))}_{datetime.now().strftime('%Y-%m%d-%H%M%S')}.zip"
    dist_zip_path = os.path.join(dist_dir, zip_file_name)
    zip_dir(src=source_dir, dist=dist_zip_path)
    print(Fore.GREEN + f"\nZip file created at: {dist_zip_path}")
