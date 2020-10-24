import pprint
import re
from tabulate import tabulate
import argparse
import os
from itertools import combinations


class CssFileParser:
    def __init__(self, css_file):
        with open(css_file, 'r') as file:
            self.lines = file.readlines()
        self.medias, rules = self.process_css_text()
        self.rules = [CssRule(rule['block'], rule['lines']) for rule in rules]

    def process_css_text(self):
        rules = []
        medias = []
        rule = {"lines": [0, 0], "block": ''}
        media = {"lines": [0, 0], "rule": ''}
        comment_block = False
        for i, line in enumerate(self.lines, 1):
            line = self.strip_comments(line.strip())
            if line.startswith('/*'):
                comment_block = True
                continue
            if line.startswith('*/'):
                comment_block = False
                continue
            if comment_block:
                continue
            if line.startswith('@'):
                media['lines'][0] = i
                if '{' in line or 'document' in line:
                    media['rule'] = line.strip(' {')
                else:
                    media['lines'][1] = i
                    media['rule'] = line.strip('; ')
                    medias.append(media)
                    media = {"lines": [0, 0], "rule": ''}
                rule = {"lines": [0, 0], "block": ''}
                continue
            if '}' in line:
                if rule['lines'][0] == 0:
                    media['lines'][1] = i
                    medias.append(media)
                    media = {"lines": [0, 0], "rule": ''}
                    continue
                rule['block'] += line
                rule['lines'][1] = i
                rules.append(rule)
                rule = {"lines": [0, 0], "block": ''}
                continue
            if rule['lines'][0] == 0:
                rule['lines'][0] = i
            rule['block'] += line
        return medias, rules

    @staticmethod
    def strip_comments(text):
        comment_pattern = re.compile(r'\/\*[\s\S]*?\*\/|([^\\:]|^)\/\/.*$')
        return re.sub(comment_pattern, '', text)


class CssRule:
    def __init__(self, rule, lines=None):
        self.rule = rule
        self.lines = lines
        self.selectors = []
        self.decleration_block = []
        selectors, decleration = rule.split('{')
        self.parse_selectors(selectors)
        self.parse_decleration(decleration)

    def parse_selectors(self, selectors):
        selectors = [selector.strip()
                     for selector in selectors.split(',')]
        for selector in selectors:
            self.selectors.append(CssSelector(selector))

    def parse_decleration(self, decleration):
        decleration = decleration.split(';')
        decleration = [param.strip() for param in decleration]
        if '}' in decleration:
            decleration.remove('}')
        for pv in decleration:
            prop, value = pv.split(':')
            self.decleration_block.append(
                CssProperty(prop, value.strip()))

    def __eq__(self, other):
        return sorted(self.selectors, key=lambda selector: selector.selector) == sorted(other.selectors, key=lambda selector: selector.selector) and sorted(self.decleration_block, key=lambda cpv: cpv.porperty) == sorted(other.decleration_block, key=lambda cpv: cpv.porperty)

    def __repr__(self):
        return f'{type(self).__name__}({self.selectors}:{self.decleration_block} )'

    def __str__(self):
        selectors = ',\n'.join([str(selector) for selector in self.selectors])
        props = '\n'.join([str(prop) for prop in self.decleration_block])
        return f'Lines: {self.lines}\n{selectors} (\n{props}\n)'


class CssSelector:
    def __init__(self, selector):
        self.selector = selector

    def __repr__(self):
        return f'{type(self).__name__}({self.selector})'

    def __str__(self):
        return self.selector

    def __eq__(self, other):
        return self.selector == other.selector


class CssProperty:
    def __init__(self, porperty, value):
        self.porperty = porperty
        self.value = value
        self.pair = {porperty: value}

    def __repr__(self):
        return f'{type(self).__name__}({self.pair})'

    def __str__(self):
        return f'{self.porperty}: {self.value};'

    def __eq__(self, other):
        return self.value == other.value and self.porperty == other.porperty


def get_duplicates(file1, file2, verbous=True):
    file1_parser = CssFileParser(file1)
    file2_parser = CssFileParser(file2)
    results = []
    for rule1 in file1_parser.rules:
        for rule2 in file2_parser.rules:
            if rule1 == rule2:
                if verbous:
                    results.append([rule1,
                                    rule2])
                    header = [file1, file2]
                else:
                    results.append([rule1.lines, rule2.lines])
                    header = [f'{file1}\nLines', f'{file2}\nLines']
    if results:
        print(f'Found {len(results)} Duplicate(s) between {file1} and {file2}:')
        return tabulate(results, header, tablefmt="grid")
    else:
        print(f'No duplicates found between {file1} and {file2}')
        return ''


def get_simmilarities(file1, file2, verbous=True):
    file1_parser = CssFileParser(file1)
    file2_parser = CssFileParser(file2)
    results = []
    for rule1 in file1_parser.rules:
        for rule2 in file2_parser.rules:
            if sorted(rule1.selectors, key=lambda s: s.selector) == sorted(rule2.selectors, key=lambda s: s.selector):
                props1 = rule1.decleration_block
                props2 = rule2.decleration_block
                percent = 0
                total = max(len(props1),
                            len(props2))
                similars = []
                for prop in props1:
                    if prop in props2:
                        percent += (1/total)
                        similars.append(str(prop))
                if percent > 0:
                    if verbous:
                        comp_string = f'{round(percent*100, 1)}%\n' + \
                            ("\n".join(similars))
                        results.append(
                            [rule1, rule2, comp_string])
                        header = [file1, file2, '% similarity']
                    else:
                        results.append([rule1.lines, rule2.lines,
                                        f'{round(percent*100)}%'])
                        header = [f'{file1}\nLines',
                                  f'{file2}\nLines',
                                  '% similarity']
    if results:
        print(f'Found {len(results)} Similarities between {file1} and {file2}:')
        return tabulate(results, header, tablefmt="grid")
    else:
        print(f'No Similarities found between {file1} and {file2}')
        return ''


def main():
    parser = argparse.ArgumentParser(
        description="Compare css files for similarities or duplicates")
    subparsers = parser.add_subparsers(dest='subcommand',
                                       help='chose either comparing 2 css files or all css files in a directory')
    two_files_parser = subparsers.add_parser('f', help='Compare 2 css files')
    two_files_parser.add_argument('file1', help='path of first css file')
    two_files_parser.add_argument('file2', help='path of second css file')
    all_parser = subparsers.add_parser('a', help='Compare all css files')
    all_parser.add_argument(
        '-a', '--all', help='checks all css files in the directory, compares each one to the other', action='store_true', default=True)
    functions_group = parser.add_mutually_exclusive_group()
    functions_group.add_argument(
        '-s', '--similar', help='Show Similar Css Rules', action='store_true', default=True)
    functions_group.add_argument(
        '-d', '--duplicate', help='Show Duplicate Css Rules', action='store_true')
    parser.add_argument('-v', '--verbous',
                        help='display full discription', action='store_false')

    args = parser.parse_args()
    if args.subcommand == 'a':
        css_files = [f for f in os.listdir() if os.path.splitext(f)
                     [-1] == '.css']
        combs = list(combinations(css_files, 2))
        for f1, f2 in combs:
            if args.similar:
                print(get_simmilarities(f1, f2, args.verbous))
            elif args.duplicate:
                print(get_duplicates(f1, f2, args.verbous))
    else:
        if args.similar:
            print(get_simmilarities(args.file1, args.file2, args.verbous))
        elif args.duplicate:
            print(get_duplicates(args.file1, args.file2, args.verbous))


if __name__ == "__main__":
    main()
