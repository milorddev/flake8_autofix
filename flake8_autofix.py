import argparse
import multiprocessing
import os
import re
import subprocess as sp
from dataclasses import dataclass

omitlist = []


@dataclass
class Entry:
    file: str
    line: int
    col: int
    error_code: str
    error_msg: str

    @classmethod
    def parse(cls, text):
        file_line_col, errorcode_errormsg = text.split(": ", 1)
        file, line, col = file_line_col.rsplit(":", 2)
        error_code, error_msg = errorcode_errormsg.strip().split(" ", 1)
        return cls(
            file=file,
            line=int(line),
            col=int(col),
            error_code=error_code,
            error_msg=error_msg,
        )

    @property
    def message(self):
        return f"{self.error_code} {self.error_msg}"


def get_all_files(source, select=None):
    """Get all files that need fixing."""
    options = " --exit-zero"
    if select:
        options += f' --select="{select}"'

    source_files = " ".join(f'"{target}"' for target in source)
    cmd = f"flake8{options} {source_files}"

    exit_code, output = sp.getstatusoutput(cmd)
    if exit_code:
        raise RuntimeError(f"An error occurred while running {cmd!r}.\nCommand output:\n{output}")

    if output.strip():
        return {Entry.parse(x).file for x in output.strip().split('\n')}
    else:
        return set()


def flake8_file(fpath, select=None):
    """Retrieve lint warnings for a specific file."""
    options = ""
    if select:
        options += f' --select="{select}"'

    file = sp.getoutput(f'flake8{options} "{fpath}"')

    filelist = file.strip().split('\n')
    filelist = list(filter(None, filelist))
    filelist = [x for x in filelist if x not in omitlist]

    return filelist


def extract_details(entry):
    '''
    fetch information from flake8 message string
    '''
    obj = Entry.parse(entry)
    return (obj.file, obj.line - 1, obj.col - 1, obj.message, entry)


def find_fix(message):
    '''
    look through func_fix dict, find key
    '''
    keys = list(func_fix.keys())
    for key in keys:
        if key in message:
            return key
    return None


def delete_line(bundle):
    '''
    delete line of mentioned row
    '''
    lines, details = bundle
    path, row, col, message, entry = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index != row:
                f.write(line)


def delete_blank_line(bundle):
    '''
    delete previous line of mentioned row
    '''
    lines, details = bundle
    path, row, col, message, entry = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index != row-1:
                f.write(line)


def insert_line(bundle):
    '''
    insert an new line at row
    '''
    lines, details = bundle
    path, row, col, message, entry = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index == row:
                f.write('\n')
            f.write(line)


def newline_EOF(bundle):
    '''
    insert new line at EOF
    '''
    lines, details = bundle
    path, row, col, message, entry = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            f.write(line)
        f.write('\n')


def insert_space_before(bundle):
    '''
    insert space at mentioned col
    '''
    lines, details = bundle
    path, row, col, message, entry = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index == row:
                newline = line[:col] + ' ' + line[col:]
                f.write(newline)
            else:
                f.write(line)


def insert_space_after(bundle):
    '''
    insert space after mentioned col
    '''
    lines, details = bundle
    path, row, col, message, entry = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index == row:
                newline = line[:col+1] + ' ' + line[col+1:]
                f.write(newline)
            else:
                f.write(line)


def convert_tabs_to_spaces(bundle):
    '''
    convert all tabs to 4 spaces
    '''
    lines, details = bundle
    path, row, col, message, entry = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            line = re.sub('\t', '    ', line)
            f.write(line)


def remove_semicolon(bundle):
    '''
    remove semicolons
    '''
    lines, details = bundle
    path, row, col, message, entry = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index == row:
                line = line.replace(';', '')
            f.write(line)


def delete_character(bundle):
    '''
    delete a character at row, col
    '''
    lines, details = bundle
    path, row, col, message, entry = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index == row:
                line = line[:col] + line[col+1:]
            f.write(line)


def fix_trailing_whitespace(bundle):
    """Fix trailing whitespace."""
    lines, details = bundle
    path, row, _, _, _ = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index == row:
                line = f"{line.rstrip()}\n"
            f.write(line)


def delete_unused_import(bundle):
    '''
    delete a character at row, col
    '''
    global omitlist
    lines, details = bundle
    path, row, col, message, entry = details
    string_to_remove = message.split("'")[1].split('.')[-1]
    if string_to_remove in lines[row]:
        with open(path, 'w') as f:
            for index, line in enumerate(lines):
                if index == row:
                    spl = line.split('import')
                    imports = spl[-1].split(',')
                    imports = [x.strip() for x in imports]
                    imports.remove(string_to_remove)
                    if len(imports):
                        new_line = spl[0] + ' import ' + ' ,'.join(imports) + '\n'
                        f.write(new_line)
                else:
                    f.write(line)
    else:
        omitlist.append(entry)


func_fix = {
    'E201': delete_character,
    'E202': delete_character,
    'E203': delete_character,
    'E211': delete_character,
    'E221': delete_character,
    'E222': delete_character,
    'E225': insert_space_before,
    'E231': insert_space_after,
    'E251': delete_character,
    'E252': insert_space_before,
    'E261': insert_space_before,
    'E262': insert_space_after,
    'E265': insert_space_after,
    'E266': delete_character,
    'E272': delete_character,
    'E302': insert_line,
    'E303': delete_blank_line,
    'E305': insert_line,
    'E703': remove_semicolon,
    'F401': delete_unused_import,
    'W191': convert_tabs_to_spaces,
    'W291': fix_trailing_whitespace,
    'W292': newline_EOF,
    'W293': delete_character,
    'W391': delete_line,
}


def solution_selector(full_details):
    '''
    selects the solution to deal out
    '''
    global omitlist
    path, row, col, message, entry = full_details

    key = find_fix(message)
    if key is None:
        omitlist.append(entry)
        return

    print(f"Fixing {entry}")
    with open(path, 'r') as f:
        lines = f.readlines()
        bundle = (lines, full_details)
        func_fix[key](bundle)


def fix_a_file(file, select):
    resolved = False
    while not resolved:
        file_errors = flake8_file(file, select=select)
        if file_errors:
            details = extract_details(file_errors[0])
            solution_selector(details)
        else:
            resolved = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--numprocesses", type=int, default=multiprocessing.cpu_count())
    parser.add_argument("--select", default="")
    parser.add_argument("source", nargs="*", default=[os.getcwd()])
    args = parser.parse_args()

    files = get_all_files(args.source, select=args.select)

    if args.numprocesses:
        p = multiprocessing.Pool(args.numprocesses)
        p.starmap(fix_a_file, [(file, args.select) for file in files])
    else:
        for file in files:
            global omitlist
            omitlist.clear()
            fix_a_file(file, args.select)

    return 0


if __name__ == "__main__":
    exit(main())
