#!/usr/local/bin/python3
# coding: utf-8

import cgi
import cgitb
# cgitb.enable()  # エラーメッセージをブラウザに表示する

form = cgi.FieldStorage()
v1 = form.getfirst('value1')
v2 = form.getfirst('value2')

def nand(a, b):
    try:
        a = int(a)
        b = int(b)
        results = {
            "AND": str(a * b),
            "OR": str(a + b - a * b),
            "XOR": str(a + b - 2 * a * b),
            "NAND": str(1 - a * b),
            "NOR": str(1 - a - b + a * b),
            "XNOR": str(1 - a - b + 2 * a * b)
        }
        return results
    except ValueError:
        return {'Error': '整数で入力してください'}

try:
    results = nand(v1, v2)
except ValueError:
    results = {'Error': '数字を入力してください'}
except Exception:
    results = {'Error': '正しく入力してください'}

print("Content-Type: text/html; charset=utf-8")
print()
print(f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            background-color: #ecf0f1;
            color: #2c3e50;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
            box-sizing: border-box;
        }}
        h1 {{
            color: #3498db;
        }}
        .container {{
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 90%;
            max-width: 400px;
            box-sizing: border-box;
            margin-bottom: 20px;
        }}
        p {{
            margin: 10px 0;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .ad-container {{
            width: 100%;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>論理演算の結果</h1>
        {''.join(f'<p>{key}: {value}</p>' for key, value in results.items() if key != 'Error')}
        {''.join(f'<p>{value}</p>' for key, value in results.items() if key == 'Error')}
        <hr/>
        <a href="../nand.html">戻る</a>
    </div>
    <div class="ad-container">
        <!-- 広告スペース -->
    </div>
</body>
</html>
""")

