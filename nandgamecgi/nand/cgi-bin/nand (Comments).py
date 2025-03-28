#!/usr/bin/python3  # スクリプトがPython 3で実行されることを指定
# coding: utf-8  # ソースコードの文字エンコーディングをUTF-8に設定

import cgi  # CGI（Common Gateway Interface）モジュールをインポート
import cgitb  # CGIトレースバックモジュールをインポート
# cgitb.enable()  # エラーメッセージをブラウザに表示する（デバッグ用）

# フォームデータを取得
form = cgi.FieldStorage()
v1 = form.getfirst('value1')  # フォームから'value1'の値を取得
v2 = form.getfirst('value2')  # フォームから'value2'の値を取得

# 論理演算を行う関数
def nand(a, b):
    try:
        a = int(a)  # 入力値aを整数に変換
        b = int(b)  # 入力値bを整数に変換
        # 論理演算の結果を辞書に格納
        results = {
            "AND": str(a * b),  # AND演算
            "OR": str(a + b - a * b),  # OR演算
            "XOR": str(a + b - 2 * a * b),  # XOR演算
            "NAND": str(1 - a * b),  # NAND演算
            "NOR": str(1 - a - b + a * b),  # NOR演算
            "XNOR": str(1 - a - b + 2 * a * b)  # XNOR演算
        }
        return results  # 結果を返す
    except ValueError:  # 整数に変換できなかった場合
        return {'Error': '整数で入力してください'}  # エラーメッセージを返す

# 論理演算を実行し、結果を取得
try:
    results = nand(v1, v2)
except ValueError:  # 数値でない値が入力された場合
    results = {'Error': '数字を入力してください'}
except Exception:  # その他の例外が発生した場合
    results = {'Error': '正しく入力してください'}

# HTTPヘッダーを出力
print("Content-Type: text/html; charset=utf-8")
print()  # 空行を出力してヘッダーの終了を示す

# HTMLコンテンツを出力
print(f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8">  # 文字エンコーディングをUTF-8に設定
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  # ビューポートの設定（レスポンシブデザイン対応）
    <style>
        body {{
            background-color: #ecf0f1;  # 背景色を設定
            color: #2c3e50;  # 文字色を設定
            font-family: Arial, sans-serif;  # フォントを設定
            margin: 0;  # マージンを0に設定
            padding: 0;  # パディングを0に設定
            display: flex;  # フレックスボックスを使用
            flex-direction: column;  # フレックス方向を縦に設定
            justify-content: center;  # 垂直方向に中央揃え
            align-items: center;  # 水平方向に中央揃え
            height: 100vh;  # 高さを100%に設定
            text-align: center;  # テキストを中央揃え
            box-sizing: border-box;  # ボックスサイズをborder-boxに設定
        }}
        h1 {{
            color: #3498db;  # 見出しの文字色を設定
        }}
        .container {{
            background-color: #ffffff;  # コンテナの背景色を設定
            padding: 20px;  # パディングを設定
            border-radius: 10px;  # 角を丸くする
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);  # ボックスシャドウを設定
            width: 90%;  # 幅を90%に設定
            max-width: 400px;  # 最大幅を400pxに設定
            box-sizing: border-box;  # ボックスサイズをborder-boxに設定
            margin-bottom: 20px;  # 下部マージンを設定
        }}
        p {{
            margin: 10px 0;  # 上下マージンを設定
        }}
        a {{
            color: #3498db;  # リンクの文字色を設定
            text-decoration: none;  # 下線を削除
        }}
        a:hover {{
            text-decoration: underline;  # ホバー時に下線を表示
        }}
        .ad-container {{
            width: 100%;  # 幅を100%に設定
            text-align: center;  # テキストを中央揃え
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>論理演算の結果</h1>
        {''.join(f'<p>{key}: {value}</p>' for key, value in results.items() if key != 'Error')}  # エラーでない結果を表示
        {''.join(f'<p>{value}</p>' for key, value in results.items() if key == 'Error')}  # エラーメッセージを表示
        <hr/>
        <a href="../nand.html">戻る</a>  # 戻るリンク
    </div>
    <div class="ad-container">
        <!-- 広告スペース -->
    </div>
</body>
</html>
""")

