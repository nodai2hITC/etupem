import sys
import os
import re
import traceback
import locale
import asyncio
import subprocess
import linecache
import unicodedata
import colorama
from colorama import Fore, Back, Style

def init():
    colorama.just_fix_windows_console()


def check(argument_error, file_not_found):
    del sys.argv[0]
    mode = 'async'
    if sys.argv and sys.argv[0] in ['--exec', '--subp', '--async']:
        mode = sys.argv[0][2:]
        del sys.argv[0]

    if (len(sys.argv) == 0 or
        sys.argv == ['-c'] or
        sys.argv == ['-h'] or
        sys.argv == ['--help']):
        print(argument_error)
        sys.exit()

    path = sys.argv[0]
    if (not os.path.isfile(path) and
        not os.path.isfile(path + '/__main__.py') and
        path != '-c'):
        print(file_not_found % path)
        sys.exit()

    return mode


def python_command():
    if sys.executable:
        return sys.executable

    cp = subprocess.run(['python3', '--version'],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return 'python' if cp.returncode else 'python3'


def run_by_asyncio(args):
    return asyncio.run(_run_by_asyncio(args))

async def _run_by_asyncio(args):
    err = ''
    cp = await asyncio.create_subprocess_exec(
        python_command(),
        *args,
        stderr=asyncio.subprocess.PIPE
    )

    while True:
        if cp.stderr.at_eof():
            break

        bin = (await cp.stderr.read(4096))
        try:
            line = bin.decode('utf-8')
        except UnicodeDecodeError:
            line = bin.decode(locale.getpreferredencoding())
        if line:
            print(line, file=sys.stderr, end='', flush=True)
            err += line
        await asyncio.sleep(0.01)

    await cp.communicate()
    return err if cp.returncode else ''


def run_by_subprocess(args):
    python = python_command()
    cp = subprocess.Popen([python] + args, stderr=subprocess.PIPE)
    err = ''

    while True:
        bin = cp.stderr.readline()
        try:
            line = bin.decode('utf-8')
        except UnicodeDecodeError:
            line = bin.decode(locale.getpreferredencoding())
        err += line
        print(line, file=sys.stderr, end='')

        if not line and cp.poll() is not None:
            break

    return err if cp.returncode else ''


def run_by_exec(filename, script):
    try:
        exec(script)
        return ""
    except Exception:
        t = traceback.format_exc()
        t = t.replace('  File "<string>",', f'  File "{filename}",')
        t = re.sub(r'  File "[^"]*exec\.py", line \d+, in run_by_exec\n *exec\(script\)\n', "", t)
        print(t, file=sys.stderr, end='')
        return t


def run(mode, args):
    if mode == 'async':
        return run_by_asyncio(args)
    elif mode == 'subp':
        return run_by_subprocess(args)
    else:
        filename = args[0]
        if filename == '-c':
            script = args[1]
            del args[1]
            filename = '<string>'
        else:
            with open(filename, "rb") as f:
                script = f.read()
        return run_by_exec(filename, script)


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


def print_script(script):
    lines = script.splitlines()
    if len(lines) > 1 and re.fullmatch(r"[ \t\~\^]+", lines[-1]):
        print(Fore.LIGHTGREEN_EX + '\n'.join(lines[0:-1]) + Fore.RESET)
        last_line = ''
        for i in range(len(lines[-1])):
            char = lines[-2][i] if i < len(lines[-2]) else ' '
            if unicodedata.east_asian_width(char) in ['F', 'W', 'A']:
                last_line += lines[-1][i] * 2
            else:
                last_line += lines[-1][i]
        last_line = re.sub(r"(\^+)", Fore.LIGHTYELLOW_EX + '\\1' + Fore.RED, last_line)
        print(Fore.RED + last_line + Fore.RESET)
    else:
        print(Fore.LIGHTGREEN_EX + script + Fore.RESET, end='')
