import etupem.exec
import sys
import re
import colorama
from colorama import Fore, Back, Style


def runner():
    colorama.init()
    argument_error = '使い方： etupemja script.py'
    file_not_found = 'ファイル「%s」が見つかりませんでした。ファイル名を確認してください。'
    etupem.exec.check(argument_error, file_not_found)
    err = etupem.exec.run(sys.argv[1:])
    if not err:
        sys.exit()
    print_error(err)


def print_error(err):
    class_, msg, filename, lineno, in_, script = etupem.exec.analyze(err)

    # Print Caution
    print(Fore.LIGHTBLACK_EX +
          '上に表示されているのが本来のエラーメッセージです。' +
          'エラーについて調べる場合は、上のエラーメッセージで検索して下さい。' +
          Fore.RESET)

    # Print error type
    print(Back.LIGHTRED_EX + Fore.BLACK
          + _error_type(class_)
          + Fore.RESET + Back.RESET)

    # Print location where the error occurrd
    if filename[0] == '<':
        print(Style.BRIGHT + filename + Style.NORMAL + ' の ', end='')
    else:
        print('ファイル「' + Style.BRIGHT + filename + Style.NORMAL + '」の ', end='')
    print(f'{Style.BRIGHT}{lineno}{Style.NORMAL}行目でエラーが発生しました。{Style.RESET_ALL}')
    print(Fore.LIGHTGREEN_EX + script + Fore.RESET, end='')

    # Print error message
    print(_error_message(class_, msg))


def _error_type(error_class):
    error_classes = {
        'SyntaxError': '文法エラー',
        'IndentationError': 'インデントのエラー',
        'TabError': 'タブとスペースの混在エラー',
        'NameError': '名前に関するエラー',
        'AttributeError': '属性に関するエラー',
        'ModuleNotFoundError': 'モジュールエラー',
        'IndexError': 'インデクス範囲外エラー',
        'ValueError': '値に関するエラー',
        'ZeroDivisionError': '0除算エラー',
        'TypeError': '型に関するエラー'
        }
    if error_class in error_classes:
        return f'【{error_classes[error_class]}({error_class})】'
    else:
        return f'【エラー({error_class})】'


def _error_message(error_class, msg):
    # SyntaxError
    if 'invalid syntax' == msg:
        return '文法が正しくありません。入力ミス等が無いか確認してください。'
    if m := re.fullmatch(r"'([^\']+)' was never closed", msg):
        return f'「{m.group(1)}」を閉じ忘れています。'
    if m := re.fullmatch(r"unterminated (?:triple-quoted )?string literal \(detected at line (\d+)\)", msg):
        return f'文字列が閉じられていません。クォートを忘れていませんか？（{m.group(1)}行目で検出）'
    if m := re.fullmatch(r"EOF while scanning (?:triple-quoted )?string literal", msg):
        return f'文字列が閉じられていません。クォートを忘れていませんか？'
    if "expected ':'" == msg:
        return 'コロン「:」を忘れています。'
    if 'invalid syntax. Perhaps you forgot a comma?' == msg:
        return '文法が正しくありません。コンマ「,」を忘れていませんか？'
    if "invalid syntax. Maybe you meant '==' or ':=' instead of '='?" == msg:
        return '文法が正しくありません。「=」ではなく「==」や「:=」ではありませんか？'
    if "cannot assign to expression here. Maybe you meant '==' instead of '='?" == msg:
        return '式に代入することはできません。「=」ではなく「==」ではありませんか？'
    if "cannot assign to attribute here. Maybe you meant '==' instead of '='?" == msg:
        return 'ここで属性に代入することはできません。「=」ではなく「==」ではありませんか？'
    if 'EOL while scanning string literal' == msg:
        return '文字列が閉じられていません。クォートを忘れていないか確認してください。'
    if 'unexpected EOF while parsing' == msg:
        return 'カッコ等の閉じ忘れをしていないか確認してください。'
    if m := re.fullmatch(r"unmatched '([^\']+)'", msg):
        return f'対応するカッコの無い「{m.group(1)}」があります。'
    if m := re.fullmatch(r"Missing parentheses in call to '([^\']+)'. Did you mean ([^?]+)\?", msg):
        return f'「{m.group(1)}」を呼び出すにはカッコが必要です。例：{m.group(2)}'
    if 'Generator expression must be parenthesized' == msg:
        return 'ジェネレータ式にはカッコが必要です。'
    if 'did you forget parentheses around the comprehension target?' == msg:
        return '内包表記のターゲットをカッコで囲むのを忘れていませんか？'
    if 'invalid non-printable character U+3000' == msg:
        return '全角空白が使われています。半角空白に直してください。'
    if m := re.fullmatch(r"invalid character '([（）’”＋－＊／％：＜＞＝！])' \(([^\)]+)\)", msg):
        return f'全角の {m.group(1)} が使われています。英語入力状態で書き直してください。'
    if m := re.fullmatch(r"invalid character '(.)' \(([^\)]+)\)", msg):
        return f'不正な文字 {m.group(1)} が使われています。'
    # IndentationError, TabError
    if 'unexpected indent' == msg:
        return 'インデントが入るべきでない場所に入ってしまっています。'
    if 'expected an indented block' == msg:
        return 'インデントが入るべき場所にありません。'
    if 'unindent does not match any outer indentation level' == msg:
        return '合わせるべきインデントが合っていません。'
    if m := re.fullmatch(r"expected an indented block after '([^']+)' statement [oi]n line (\d+)", msg):
        return f'{m.group(2)}行目の {m.group(1)} の後に、インデントがありません。'
    if 'inconsistent use of tabs and spaces in indentation' == msg:
        return 'インデントにタブとスペースが混在しています。'
    # IndexError
    if 'list index out of range' == msg:
        return 'リストの範囲外を参照しようとしています。リストの大きさと参照しようとした位置を確認してください。'
    if 'tuple index out of range' == msg:
        return 'タプルの範囲外を参照しようとしています。タプルの大きさと参照しようとした位置を確認してください。'
    if 'string index out of range' == msg:
        return '文字列の範囲外を参照しようとしています。文字列の長さと参照しようとした位置を確認してください。'
    # NameError
    if m := re.fullmatch(r"name '([^\']+)' is not defined. Did you mean: '([^\']+)'\?", msg):
        return f'「{m.group(1)}」という名前の変数などは見つかりませんでした。「{m.group(2)}」のスペルミスではありませんか？'
    if m := re.fullmatch(r"name '([^\']+)' is not defined", msg):
        return f'「{m.group(1)}」という名前の変数などは見つかりませんでした。スペルミスや、大文字小文字の打ち間違い等をしていないか確認してください。'
    # TypeError
    if m := re.fullmatch(r'can only concatenate str \(not "([^"]+)"\) to str', msg):
        return f'文字列に {_data_type(m.group(1), "のデータ")}を結合することはできません。'
    if m := re.fullmatch(r"unsupported operand type\(s\) for \+: '([^\']+)' and '([^\']+)'", msg):
        return f'{_data_type(m.group(1))}に {_data_type(m.group(2), "のデータ")}を足すことはできません。'
    if m := re.fullmatch(r"([^(]+)\(\) missing (\d+) required positional arguments: (.+)", msg):
        args = m.group(3).replace(', and ', ', ').replace(' and ', ', ')
        return f'{m.group(1)}() に必要な引数が {m.group(2)} 個（{args}）足りません。'
    if m := re.fullmatch(r"([^(]+)\(\) takes (\d+) positional arguments but (\d+) were given", msg):
        return f'{m.group(1)}() は引数（位置引数）を {m.group(2)} 個しか受け取りませんが、{m.group(3)} 個の引数が与えられています。'
    if m := re.fullmatch(r"([^(]+)\(\) takes from (\d+) to (\d+) positional arguments but (\d+) were given", msg):
        return f'{m.group(1)}() は引数（位置引数）を {m.group(2)}～{m.group(3)} 個しか受け取りませんが、{m.group(4)} 個の引数が与えられています。'
    if m := re.fullmatch(r"([^(]+)\(\) got an unexpected keyword argument '([^']+)'", msg):
        return f'{m.group(1)}() に \'{m.group(2)}\' という未対応のキーワード引数が与えられています。'
    # ValueError
    if m := re.fullmatch(r'invalid literal for int\(\) with base (\d+): (\'[^\']*\')', msg):
        return f'文字列 {m.group(2)} は、{m.group(1)}進法の数値として不適切です。'
    if m := re.fullmatch(r'could not convert string to float: (\'[^\']+\')', msg):
        return f'文字列 {m.group(1)} を float 型に変換することはできません。'
    # AttributeError
    if m := re.fullmatch(r"'([^\']+)' object has no attribute '([^\']+)'. Did you mean: '([^\']+)'\?", msg):
        return f'{_data_type(m.group(1), "のオブジェクト")}には、属性 {m.group(2)} はありません。「{m.group(3)}」のスペルミスではありませんか？'
    if m := re.fullmatch(r"'([^\']+)' object has no attribute '([^\']+)'", msg):
        return f'{_data_type(m.group(1), "のオブジェクト")}には、属性 {m.group(2)} はありません。オブジェクトの型は想定通りか、属性名のスペルミスは無いか確認してください。'
    # KeyError
    if error_class == 'KeyError':
        return f'{msg} というキーはありません。スペルミス等をしていないか確認してください。'
    # ModuleNotFoundError, ImportError
    if m := re.fullmatch(r"No module named '([^\']+)'", msg):
        return f'モジュール「{m.group(1)}」が見つかりません。このモジュールがインストールされているか、スペルミスをしていないか確認してください。'
    if m := re.match(r"^cannot import name '([^\']+)' from '([^\']+)'", msg):
        return f'モジュール「{m.group(2)}」に、「{m.group(1)}」という名前のオブジェクトが見つかりません。スペルミスをしていないか等確認してください。'
    # FileNotFoundError
    if m := re.fullmatch(r"\[Errno 2\] No such file or directory: '([^\']+)'", msg):
        return f'ファイル「{m.group(1)}」が見つかりません。スペルミス等をしていないか確認してください。'
    # ZeroDivisionError
    if 'division by zero' == msg:
        return '0 で割ることはできません。除数（割る数）が予期せず 0 になっていないか確認してください。'
    # その他のエラー
    return msg


def _data_type(name, suffix=''):
    types = {
        'str': '文字列',
        'int': '整数',
        'float': '数値',
        'list': 'リスト',
        'tuple': 'タプル'
    }
    if name in types:
        return f'{types[name]}({name}型)'
    else:
        return f'{name}型{suffix}'
