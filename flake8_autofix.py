import os
import subprocess as sp

omitlist = []


def flake8_file(fpath):
    '''
    see all messages in 1 file
    '''
    file = sp.getoutput('flake8 ' + fpath)
    filelist = file.strip().split('\n')
    filelist = list(filter(None, filelist))
    filelist = [x for x in filelist if x not in omitlist]
    return filelist


def extract_details(entry):
    entrysplit = entry.split(':')
    path = entrysplit[0]
    row = int(entrysplit[1])-1
    col = int(entrysplit[2])-1
    message = ''.join(entrysplit[3])
    return (path, row, col, message, entry)


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
    return None


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


def newline_EOF(bundle):
    print('inserting line at end')
    lines, details = bundle
    path, row, col, message = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            f.write(line)
        f.write('\n')


def insert_space_before(bundle):
    print('inserting space')
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
    print('inserting space')
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
    print('deleting semicolon')
    lines, details = bundle
    path, row, col, message = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index == row:
                line = line.replace(';', '')
            f.write(line)


def delete_space(bundle):
    print('deleting space')
    lines, details = bundle
    path, row, col, message = details
    with open(path, 'w') as f:
        for index, line in enumerate(lines):
            if index == row:
                line = line[:col] + line[col+1:]
            f.write(line)


func_fix = {
    'E203': delete_space,
    'E302': insert_line,
    # 'E303': delete_line,
    'E305': insert_line,
    'E231': insert_space_after,
    'E252': insert_space_before,
    'E261': insert_space_before,
    'E262': insert_space_after,
    'E265': insert_space_after,
    'E703': remove_semicolon,
    'F401': delete_line,
    'W292': newline_EOF,
    'W293': delete_line,
    'W391': delete_line,
}


def solution_selector(full_details):
    '''
    selects the solution to deal out
    '''
    global omitlist
    path, row, col, message, entry = full_details
    details = (path, row, col, message)
    with open(path, 'r') as f:
        lines = f.readlines()
        key = find_fix(message)
        if key is None:
            print("Manually fix", entry)
            omitlist.append(entry)
        else:
            print(key, entry)
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
