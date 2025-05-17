#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
from time import sleep
from colorama import Fore, init

def are_equivalent_paths(rel1: str, rel2: str) -> bool:
    """
    Return True if rel1 and rel2 refer to the *same* file
    up to at most one extra directory inserted just before the filename.
    """
    if rel1 == rel2:
        return True
    name1 = os.path.basename(rel1)
    name2 = os.path.basename(rel2)
    if name1 != name2:
        return False
    dirs1 = rel1.split(os.sep)[:-1]
    dirs2 = rel2.split(os.sep)[:-1]
    if len(dirs2) - 1== len(dirs1) and dirs2[:len(dirs1)] == dirs1:
        return True
    if len(dirs1) - 1== len(dirs2) and dirs1[:len(dirs2)] == dirs2:
        return True
    return False

def adjust_path_type(path: str) -> str:
    """
    Normalize input (absolute or relative) to an absolute path.
    """
    p = path.strip().strip('"').strip("'")
    return os.path.abspath(p)

def get_public_methods(file_path: str) -> list[str]:
    """
    Return a list of all public method names in a PHP file.
    """
    pattern = re.compile(
        r'^\s*public\s+function\s+&?\s*'
        r'([A-Za-z_]\w*)'
        r'(?=\s*\()',
        re.IGNORECASE
    )
    methods: list[str] = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = pattern.match(line)
            if m:
                methods.append(re.sub(r'[_-]', '', m.group(1).lower()))
    return methods

def main():
    init(autoreset=True)
    print(Fore.GREEN + "You executed the file comparison between two Laravel Modules class methods.\n"
          "Press Ctrl+C to exit, otherwise wait for 5 seconds...")
    sleep(5)
    try:
        print(Fore.YELLOW + "Starting procedure...")
        first_root = adjust_path_type(input(Fore.CYAN + "Enter the ORIGINAL directory path:\n"))
        second_root = adjust_path_type(input(Fore.CYAN + "Enter the DERIVED directory path:\n"))
        for d in (first_root, second_root):
            if not os.path.isdir(d):
                raise TypeError(f"The given path {d!r} is not a directory.")
        first_php, second_php = [], []
        for base, coll in ((first_root, first_php), (second_root, second_php)):
            for root, _, files in os.walk(base):
                for fn in files:
                    if fn.lower().endswith('.php'):
                        coll.append(os.path.join(root, fn))
        first_rel  = [os.path.relpath(p, first_root)  for p in first_php]
        second_rel = [os.path.relpath(p, second_root) for p in second_php]
        pairs: list[tuple[str,str,str,str]] = []
        for f in first_rel:
            for s in second_rel:
                if are_equivalent_paths(f, s):
                    pairs.append((
                        f, s,
                        os.path.join(first_root, f),
                        os.path.join(second_root, s)
                    ))
                    break
        if not pairs:
            print(Fore.YELLOW + "No matching PHP class files found in both directories.")
            return
        statuses: dict[str,str] = {}
        print()
        eqs = []
        adds = []
        lck = []
        errs = []
        for _, s_rel, path1, path2 in pairs:
            try:
                m1 = get_public_methods(path1)
            except Exception as e:
                errs.append(Fore.RED + f"Error reading {path1}: {e}")
                m1 = []
            try:
                m2 = get_public_methods(path2)
            except Exception as e:
                errs.append(Fore.RED + f"Error reading {path2}: {e}")
                m2 = []
            if not m1 or not m2:
                status, color = "Error", Fore.YELLOW
            elif len(m1) <= len(m2) and all(name in m2 for name in m1):
                if len(m1) == len(m2):
                    status, color = "Equal", Fore.GREEN
                else:
                    status, color = "Added methods", Fore.LIGHTYELLOW_EX
            else:
                status, color = "LACKING METHODS", Fore.RED
            statuses[s_rel] = status
            eval_res = color + f"{s_rel}: {len(m1)} vs {len(m2)} => {status}"
            if color == Fore.RED:
                lck.append(eval_res)
            elif color == Fore.LIGHTYELLOW_EX:
                adds.append(eval_res)
            elif color == Fore.GREEN:
                eqs.append(eval_res)
            else:
                errs.append(eval_res)
        total = len(pairs)
        eq = sum(1 for s in statuses.values() if s == "Equal")
        add = sum(1 for s in statuses.values() if s == "Added methods")
        lack = sum(1 for s in statuses.values() if s == "LACKING METHODS")
        err = sum(1 for s in statuses.values() if s == "Error")
        print()
        for r in (*eqs, *adds, *lck, *errs):
            print(r)
        print(Fore.CYAN + f"Compared {total} file(s): {eq} equal, {add} added, "
              f"{lack} lacking, {err} errors.")
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nOperation cancelled by user.")
        sys.exit(1)
    except TypeError as e:
        print(Fore.RED + f"TypeError: {e}")
    except PermissionError as e:
        print(Fore.RED + f"PermissionError: {e}")
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
