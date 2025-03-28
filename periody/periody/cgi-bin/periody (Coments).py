#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import cgi  # CGIモジュールをインポート
import cgitb  # CGIトレースバックモジュールをインポート
import os  # OSモジュールをインポート
import time  # 時間モジュールをインポート

cgitb.enable()  # CGIトレースバックを有効にする

# フォームデータを取得
form = cgi.FieldStorage()
personal_name = form.getvalue('personal_name')  # 名前を取得
email = form.getvalue('email')  # メールアドレスを取得
contents = form.getvalue('contents')  # 内容を取得
action = form.getvalue('action')  # アクションを取得
post_id = form.getvalue('post_id')  # 投稿IDを取得

bbs_file = './bbs.txt'  # 掲示板データファイルのパス

# データを読み込む関数
def read_data():
    if not os.path.exists(bbs_file):  # ファイルが存在しない場合
        return []
    with open(bbs_file, 'r', encoding='utf-8') as f:  # ファイルを読み込みモードで開く
        return f.readlines()  # 行ごとに読み込んで返す

# データを書き込む関数
def write_data(data):
    with open(bbs_file, 'a', encoding='utf-8') as f:  # ファイルを追記モードで開く
        f.write(data)  # データを書き込む

# 投稿を削除する関数
def delete_post(post_id):
    lines = read_data()  # データを読み込む
    with open(bbs_file, 'w', encoding='utf-8') as f:  # ファイルを上書きモードで開く
        inside_post = False  # 投稿内かどうかのフラグ
        for line in lines:
            if f'id="{post_id}"' in line:  # 投稿IDが一致する行を見つけた場合
                inside_post = True  # 投稿内フラグを立てる
            elif inside_post and line.strip() == "</div>":  # 投稿の終了タグを見つけた場合
                inside_post = False  # 投稿内フラグを下ろす
            elif not inside_post:  # 投稿内でない場合
                f.write(line)  # 行を書き込む

# 投稿を通報する関数
def report_post(post_id):
    time.sleep(10)  # 10秒待機
    delete_post(post_id)  # 投稿を削除する

# HTTPヘッダーを出力
print("Content-Type: text/html\n")
print("""
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>ＮＩＳＡ積立掲示板「ＰＥＲＩＯＤＹ」</title>
<meta charset="utf-8">
<meta name="description" content="">
<meta name="author" content="">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="">
<style>
    input[type="text"], input[type="email"], textarea {
        width: 100%;  # フォーム要素の幅を100%に設定
        padding: 10px;  # パディングを10pxに設定
        margin-bottom: 10px;  # 下部マージンを10pxに設定
        border: 1px solid #ccc;  # 枠線を設定
        border-radius: 4px;  # 角を丸くする
        box-sizing: border-box;  # ボックスサイズをborder-boxに設定
    }
    @media (max-width: 600px) {  # 画面幅が600px以下の場合のスタイル
        input[type="text"], input[type="email"], textarea {
            padding: 8px;  # パディングを8pxに設定
        }
    }
</style>
</head>
<body>
<p>ＮＩＳＡ積立掲示板「ＰＥＲＩＯＤＹ」</p>
<form method="POST" action="periody.py">
    <input type="text" name="personal_name" placeholder="名前"><br><br>  # 名前入力フィールド
    <input type="email" name="email" placeholder="メールアドレス（任意）"><br><br>  # メールアドレス入力フィールド
    <textarea name="contents" rows="8" cols="40" placeholder="内容"></textarea><br><br>  # 内容入力フィールド
    <input type="submit" name="action" value="投稿する">  # 投稿ボタン
</form>
""")

# 投稿するアクションが実行された場合
if action == "投稿する" and personal_name and contents:
    post_id = str(int(time.time()))  # 現在のタイムスタンプを投稿IDとして使用
    email_link = f'<a href="mailto:{email}">{email}</a>' if email else '（メールアドレスなし）'  # メールリンクを作成
    contents = contents.replace("\n", "<br>")  # 改行をHTMLの<br>タグに変換
    data = f'<div id="{post_id}"><hr>\n<p>投稿者: {personal_name} {email_link}</p>\n<p>内容:</p>\n<p>{contents}</p>\n'  # 投稿データを作成
    data += f'<form method="POST" action="periody.py"><input type="hidden" name="post_id" value="{post_id}">'  # 隠しフィールドに投稿IDを設定
    data += f'<input type="submit" name="action" value="削除"><input type="submit" name="action" value="通報"></form></div>\n'  # 削除と通報ボタンを追加
    write_data(data)  # データを書き込む

# 削除アクションが実行された場合
if action == "削除" and post_id:
    delete_post(post_id)  # 投稿を削除する

# 通報アクションが実行された場合
if action == "通報" and post_id:
    report_post(post_id)  # 投稿を通報する

# データを読み込んで出力
for line in read_data():
    print(line)

print("""
</body>
</html>
""")

