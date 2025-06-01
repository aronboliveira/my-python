#!/usr/bin/env python3
import os
import re
import argparse
from pathlib import Path
from colorama import Fore, init
init(autoreset=True)

def remove_multiple_underscores(path=".", extensions=None, interactive=True):
    """
    Remove multiple consecutive underscores from image filenames.
    
    Args:
        path (str): Directory to start the search (default: current directory)
        extensions (list): List of image extensions to process
        interactive (bool): Whether to ask for confirmation before renaming
    """
    
    if extensions is None:
        extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'svg']
    extensions = [ext.lower() for ext in extensions]
    underscore_pattern = re.compile(r'_{2,}')
    for root, _, files in os.walk(path):
        for filename in files:
            file_ext = Path(filename).suffix[1:].lower()
            if file_ext in extensions and underscore_pattern.search(filename):
                old_path = os.path.join(root, filename)
                new_filename = underscore_pattern.sub('_', filename)
                new_path = os.path.join(root, new_filename)
                should_rename = False
                if interactive:
                    print(f"{Fore.YELLOW}Do you want to replace \"{Fore.RED}{filename}{Fore.YELLOW}\" with \"{Fore.GREEN}{new_filename}{Fore.YELLOW}\" ? (y/N): ", end="")
                    response = input().strip().lower()
                    should_rename = response in ['y', 'yes']
                else:
                    print(f"{Fore.CYAN}Renaming \"{Fore.RED}{filename}{Fore.CYAN}\" to \"{Fore.GREEN}{new_filename}{Fore.CYAN}\"")
                    should_rename = True
                if should_rename:
                    try:
                        os.rename(old_path, new_path)
                        print(f"{Fore.GREEN}✓ Renamed successfully")
                    except OSError as e:
                        print(f"{Fore.RED}✗ Error: {e}")
                elif interactive:
                    print(f"{Fore.LIGHTBLACK_EX}Skipped")

def main():
    parser = argparse.ArgumentParser(description="Remove multiple consecutive underscores from image filenames")
    parser.add_argument("path", nargs="?", default=".", help="Directory to start the search (default: current directory)")
    parser.add_argument("-e", "--extensions", nargs="+", default=["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "svg"],
                       help="Image extensions to process (default: jpg jpeg png gif bmp tiff webp svg)")
    parser.add_argument("--no-interactive", action="store_true", help="Run without interactive prompts")
    args = parser.parse_args()
    if not os.path.exists(args.path):
        print(f"{Fore.RED}Error: Path '{args.path}' does not exist")
        return 1
    interactive = not args.no_interactive
    print(f"{Fore.CYAN}Searching for image files with multiple underscores in: {args.path}")
    print(f"{Fore.CYAN}Extensions: {', '.join(args.extensions)}")
    print(f"{Fore.CYAN}Mode: {'Interactive' if interactive else 'Automatic'}")
    print()
    remove_multiple_underscores(args.path, args.extensions, interactive)
    print(f"\n{Fore.GREEN}Done!")
    return 0


if __name__ == "__main__":
    exit(main())