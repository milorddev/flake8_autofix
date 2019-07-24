import os
import subprocess as sp


def flake8_file(fpath):
    '''
    see all messages in 1 file
    '''
    file = sp.getoutput('flake8 ' + fpath)
    filelist = file.strip().split('\n')
    filelist = list(filter(None, filelist))
    return filelist


def extract_details(entry):
    print('entry', entry)
    path, row, col, message = entry.split(':')
    row = int(row)-1
    col = int(col)-1
    return (path, row, col, message)


def get_all_files():
    '''
    get all files that need linting
    '''
    flake8 = sp.getoutput('flake8 ' + os.getcwd())
    flakelist = flake8.strip().split('\n')
    return {x.split(':')[0] for x in flakelist}


def find_fix(message):
    '''
    look through func_fix dict, find key
    '''
    keys = list(func_fix.keys())
    for key in keys:
        if key in message:
            return key


def delete_line(bundle):
    print('deleting line')
    lines, details = bundle
    path, row, col, message = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index != row:
                f.write(line)


def insert_line(bundle):
    print('inserting line')
    lines, details = bundle
    path, row, col, message = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index == row:
                f.write('\n')
            f.write(line)


def insert_space_before(bundle):
    print('deleting line')
    lines, details = bundle
    path, row, col, message = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index == row:
                newline = line[:col] + ' ' + line[col:]
                f.write(newline)
            else:
                f.write(line)


def insert_space_after(bundle):
    print('deleting line')
    lines, details = bundle
    path, row, col, message = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index == row:
                newline = line[:col+1] + ' ' + line[col+1:]
                f.write(newline)
            else:
                f.write(line)


def remove_semicolon(bundle):
    print('deleting line')
    lines, details = bundle
    path, row, col, message = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index == row:
                line.replace(';', '')
            f.write(line)


func_fix = {
    'W391': delete_line,
    'E302': insert_line,
    'E305': insert_line,
    'E261': insert_space_before,
    'E262': insert_space_after,
    'E703': remove_semicolon
}


def solution_selector(details):
    '''
    selects the solution to deal out
    '''
    path, row, col, message = details
    with open(path, 'r') as f:
        lines = f.readlines()
        key = find_fix(message)
        bundle = (lines, details)
        func_fix[key](bundle)


files = get_all_files()
for file in files:
    resolved = False
    while not resolved:
        file_errors = flake8_file(file)
        if(len(file_errors) == 0):
            resolved = True
        else:
            details = extract_details(file_errors[0])
            solution_selector(details)
