# etupem

make Easy To Understand Python Error Message for those who are not good at English.

Currently, it is only available in Japanese.

Python のエラーメッセージを日本語で表示します。

## Requirements

- Python 3.8 or newer

## Recommended

- Python 3.10 or newer

## Install

    $ pip install etupem

## Usage (for Japanese)

    $ pythonja script.py

or

    $ python -m etupem ja script.py

## Example1

For example, run the following script.

```python:type_error.py
"あいうえお" + 456
```

Original python error message:

```
$ python type_error.py
Traceback (most recent call last):
  File "E:\scripts\type_error.py", line 1, in <module>
    "あいうえお" + 123
    ~~~~~~~~^~~~~
TypeError: can only concatenate str (not "int") to str
```

When using etupem:

![type_error](https://github.com/nodai2hITC/etupem/assets/25577113/c66b7368-bbf8-4918-8539-ef46067b4d6f)

```
$ pythonja type_error.py
Traceback (most recent call last):
  File "E:\scripts\type_error.py", line 1, in <module>
    "あいうえお" + 123
    ~~~~~~~~^~~~~
TypeError: can only concatenate str (not "int") to str
上に表示されているのが本来のエラーメッセージです。エラーについて調べる場合は、上のエラーメッセージで検索して下さい。
【型に関するエラー(TypeError)】
ファイル「E:\scripts\type_error.py」の 1行目でエラーが発生しました。
    "あいうえお" + 123
    ~~~~~~~~~~~~~^~~~~
文字列に 整数(int型)を結合することはできません。
```

## Example2

```python:name_error.py
Print("Hello, World!")
```

Original python error message:

```
$ python name_error.py
Traceback (most recent call last):
  File "E:\scripts\name_error.py", line 1, in <module>
    Print("Hello, World!")
    ^^^^^
NameError: name 'Print' is not defined. Did you mean: 'print'?
```

When using etupem:

![name_error](https://github.com/nodai2hITC/etupem/assets/25577113/a6f8fd9b-a666-4f53-baa7-f36327dc3c6c)

```
$ pythonja name_error.py
Traceback (most recent call last):
  File "E:\scripts\name_error.py", line 1, in <module>
    Print("Hello, World!")
    ^^^^^
NameError: name 'Print' is not defined. Did you mean: 'print'?
上に表示されているのが本来のエラーメッセージです。エラーについて調べる場合は、上のエラーメッセージで検索して下さい。
【名前に関するエラー(NameError)】
ファイル「E:\scripts\name_error.py」の 1行目でエラーが発生しました。
    Print("Hello, World!")
    ^^^^^
「Print」という名前の変数などは見つかりませんでした。「print」の入力ミスではありませんか？
```
