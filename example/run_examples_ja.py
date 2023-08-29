import sys
import os
import etupem.exec
import etupem.ja

etupem.exec.init()
mode = 'async'
if len(sys.argv) > 1 and sys.argv[1] in ['--exec', '--subp', '--async']:
    mode = sys.argv[1][2:]

for filename in os.listdir('./examples'):
    os.system('cls' if os.name == 'nt' else 'clear')
    path = './examples/' + filename
    print(f'--- テスト「{filename}」実行 ---')
    with open(path, 'r') as f:
        print(f.read())
    print('\n--- エラーメッセージ ---')
    etupem.ja.print_error(etupem.exec.run(mode, [path]))
    if input() == 'q':
        break
