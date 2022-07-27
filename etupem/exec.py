import sys
import os
import re
import locale
import subprocess
import linecache


def check(argument_error, file_not_found):
    if len(sys.argv) < 2:
        print(argument_error)
        sys.exit()

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(file_not_found % path)
        sys.exit()

    return path


def python_command():
    cp = subprocess.run(['python3', '--version'],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return 'python' if cp.returncode else 'python3'


def run(args):
    python = python_command()
    cp = subprocess.Popen([python] + args,
                          encoding=locale.getpreferredencoding(),
                          stderr=subprocess.PIPE)
    err = ''

    while True:
        line = cp.stderr.readline()
        err += line
        print(line, file=sys.stderr, end='')

        if not line and cp.poll() is not None:
            break

    return err if cp.returncode else ''


def analyze(err):
    lines = err.splitlines(True)
    error = lines.pop()
    location_re = r'  File "([^"]+)", line (\d+)(?:, in (\S+))?\s*'
    filename = ''
    lineno = 0
    in_ = ''
    script = ''

    for line in lines:
        if m := re.fullmatch(location_re, line):
            filename = m.group(1)
            lineno = int(m.group(2))
            in_ = m.group(3)
            script = ''
        else:
            script += line

    if m:= re.fullmatch(r'([^:]+): ([\s\S]+)', error):
        error_class = m.group(1)
        error_message = m.group(2).rstrip()
    else:
        error_class = ''
        error_message = error.rstrip()

    if not script and os.path.isfile(filename) and lineno:
        script = '    ' + linecache.getline(filename, lineno).lstrip()

    return error_class, error_message, filename, lineno, in_, script
