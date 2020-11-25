import os
import json
import sys
import argparse


def walk(path):
    if os.path.isdir(path):
        data = {'name': os.path.basename(path), 'files': [], 'directories': []}
        for item in os.listdir(path):
            name = os.path.join(path, item)
            if os.path.isdir(name):
                data['directories'].append(walk(name))
            else:
                data['files'].append(item)
    else:
        return os.path.basename(path)
    return data


parser = argparse.ArgumentParser(
    description='walks the directory tree and export it to json')
parser.add_argument(
    'path', help='path of directory to be walked', nargs="?", default=os.getcwd())
parser.add_argument('-p', '--print',
                    help='prints output to standart out', action='store_true')
args = parser.parse_args()

output = walk(args.path)
jsoned = json.dumps(output, indent=2)
with open(f'{os.path.basename(args.path)}_tree.json', 'w') as file:
    file.write(jsoned)
if args.print:
    print(jsoned)
