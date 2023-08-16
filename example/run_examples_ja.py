import os
import etupem.exec
import etupem.ja

etupem.exec.init()
for filename in os.listdir('./examples'):
    path = './examples/' + filename
    print(f'--- テスト「{filename}」実行 ---')
    with open(path, 'r') as f:
        print(f.read())
    print('--- エラーメッセージ ---')
    etupem.ja.print_error(etupem.exec.run('auto', [path]))
