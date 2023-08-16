import sys

lang = ''
if len(sys.argv) > 1:
    lang = sys.argv[1]
    del(sys.argv[1])

if lang == 'ja':
    import etupem.ja
    etupem.ja.runner()
else:
    print('usage: python -m etupem ja [option] script.py')
