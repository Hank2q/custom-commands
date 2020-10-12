import os
import subprocess
import argparse
from pprint import pprint
import sys
from glob import glob as no_hidden


def ls_walk(directory, tabs=0):
    files = os.listdir(directory)
    dirs = [files.pop(i)
            for i, folder in enumerate(files) if os.path.isdir(os.path.join(directory, folder))]
    print(' ' * tabs + f'[{os.path.split(directory)[1]}]:')
    tabs += 1
    for f in files:
        tabbing = (' ' * (tabs-1)) + '|' + ' '
        print(tabbing + f)
    for folder in dirs:
        path = os.path.join(directory, folder)
        ls_walk(path, tabs)


def bytes_parser(number, unit='Bytes'):
    units = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    if unit not in units:
        return number, unit
    if number > 1024:
        number = round(number/1000, 2)
        nextI = units.index(unit) + 1
        if nextI == len(units):
            return number, unit
        unit = units[nextI]
        number, unit = bytes_parser(number, unit)
    return number, unit


def dir_size(folder):
    size = 0
    try:
        for item in os.listdir(folder):
            path = os.path.join(folder, item)
            try:
                if os.path.isdir(path):
                    size += dir_size(path)
                else:
                    size += os.path.getsize(path)
            except FileNotFoundError:
                size += os.path.getsize(path)
    except PermissionError:
        pass
    return size


def list_dir(args):
    if args.walk:
        ls_walk(args.path)
        return
    if args.all:
        dirList = os.listdir(args.path)  # list with hidden items
        dirList = list(map(lambda d: os.path.join(args.path, d), dirList))
    else:
        dirList = no_hidden(
            os.path.join(args.path, '*'))  # list without hidden items

    result = []
    files = 0
    totalFilesSize = 0
    dirs = 0
    totalDirsSize = 0

    # looping through the files in the path to list them with specified options in cli
    for f in dirList:
        name = os.path.split(f)[1]
        if os.path.isdir(f):
            dirs += 1
            if args.files:
                continue
            size = dir_size(f)
            totalDirsSize += size
            if args.size:
                size, unit = bytes_parser(size)
                result.append(f'[{name}] - {size} {unit}')
            else:
                result.append(f'[{name}]')
        else:
            files += 1
            if args.folders:
                continue
            try:
                size = os.path.getsize(f)
                totalFilesSize += size
            except FileNotFoundError:
                pass
            if args.size:
                size, unit = bytes_parser(size)
                result.append(f'{name} - {size} {unit}')
            else:
                result.append(name)

    # getting sizes of files and dirs
    totalPathSize, totalPathUnit = bytes_parser(totalFilesSize + totalDirsSize)
    totalFilesSize, totalFilesUnit = bytes_parser(totalFilesSize)
    totalDirsSize, totalDirsUnit = bytes_parser(totalDirsSize)

    # formating result message
    formated_result = '\n'.join(result)
    info = f'''\
Directory of: {os.path.abspath(args.path)} - {totalPathSize} {totalPathUnit}

{formated_result}

'''
    # showing size of only files or dirs or both depending on cli option -f / -d
    filesInfo = f'{files} File(s) - {totalFilesSize} {totalFilesUnit}\n'
    dirInfo = f'{dirs} Dir(s)  - {totalDirsSize} {totalDirsUnit}\n'
    if args.files:
        dirInfo = ''
    elif args.folders:
        filesInfo = ''
    else:
        pass
    info += filesInfo + dirInfo
    print(info)
    if args.output:
        with open(f'lsOutput.txt', 'w') as output:
            output.write(info)


def main():
    parser = argparse.ArgumentParser(
        description="List directory files and folders")
    parser.add_argument('path', nargs="?",
                        help='Path of directory to list (default to current dir)', default='.')
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
    parser.add_argument(
        '-w', '--walk', help='List all files, directories and subdirectorys of a path', action='store_true')
    args = parser.parse_args()
    try:
        list_dir(args)
    except Exception as err:
        print(err)
        return 1
    else:
        return 0


if __name__ == "__main__":
    exit(main())
