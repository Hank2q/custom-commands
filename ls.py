import os
import subprocess
import argparse
from pprint import pprint
import sys
from glob import glob as no_hidden


def dir_size(dir):
    size = 0
    for dirpath, dis, files in os.walk(dir):
        for f in files:
            name = os.path.join(dirpath, f)
            if not os.path.islink(name):
                size += os.path.getsize(name)
    return size


def list_dir(args):
    # print(args)

    if args.all:
        dirList = os.listdir(args.path)  # list with hidden items
    else:
        dirList = no_hidden(
            os.path.join(args.path, '*'))  # list without hidden items
        dirList = [os.path.split(f)[-1] for f in dirList]

    result = []
    files = 0
    total_f = 0
    dirs = 0
    total_d = 0
    for f in dirList:
        if os.path.isdir(f):
            dirs += 1
            if args.files:
                continue
            size = dir_size(f)
            total_d += size
            if args.size:
                result.append(f'[{f}] - {round(size/1000, 2)} kB')
            else:
                result.append(f'[{f}]')
        else:
            files += 1
            if args.folders:
                continue
            size = os.path.getsize(f)
            total_f += size
            if args.size:
                result.append(f'{f} - {round(size/1000, 2)} kB')
            else:
                result.append(f)
    total_z = round((total_f + total_d) / 1000, 2)
    total_f = round(total_f/1000, 2)
    total_d = round(total_d/1000, 2)
    formated_result = '\n'.join(result)
    info = f'''\
Directory of: {os.path.abspath(args.path)} - {total_z} kB

{formated_result}

{files} File(s) - {total_f} kB
{dirs} Dir(s)  - {total_d} kB
'''
    print(info)
    if args.output:
        with open(f'lsOutput.txt', 'w') as output:
            output.write(info)


def main():
    parser = argparse.ArgumentParser(
        description="List directory files and folders")
    parser.add_argument('path', nargs="?",
                        help='Path to list items (default to current dir)', default='.')
    parser.add_argument('-a', '--all',
                        help='Show all files including hidden ones', action='store_true')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-f', '--files', help='Show only files', action='store_true')
    group.add_argument(
        '-d', '--folders', help='Show only folders', action='store_true')
    parser.add_argument(
        '-z', '--size', help="Display size in kilobytes", action='store_true')
    parser.add_argument(
        '-o', '--output', help="Stores result in an output text file", action='store_true')
    args = parser.parse_args()
    list_dir(args)
    return 0


if __name__ == "__main__":
    exit(main())


# todo: make a recursive option with os.walk
# todo: add tabular formating
# todo: add function to format size accordingly
