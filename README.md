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

## Example

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

When using etupem: (It will actually be colored.)

```
$ pythonja type_error.py
Traceback (most recent call last):
  File "E:\scripts\type_error.py", line 1, in <module>
    "あいうえお" + 123
    ~~~~~~~~^~~~~
TypeError: can only concatenate str (not "int") to str
上に表示されているのが本来のエラーメッセージです。エラーについて調べる場合は、上のエラーメッセージで検索して下さい。
【型に関するエラー(TypeError)】
ファイル「F:\scripts\type_error.py」の 1行目でエラーが発生しました。
    "あいうえお" + 123
    ~~~~~~~~~~~~~^~~~~
文字列に 整数(int型)を結合することはできません。
```
