import os

for filename in os.listdir('./examples'):
    path = './examples/' + filename
    print(f'--- テスト「{filename}」実行 ---')
    with open(path, 'r') as f:
        print(f.read())
    print('--- エラーメッセージ ---')
    os.system(f'pythonja "{path}"')
