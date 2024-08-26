# app.py
from flask import Flask, render_template, request, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()  # ここでrequestを使用
    if data is None:
        return "Invalid data", 400
    # デバッグ用に受信したデータをプリント
    print(data)
    if data.get('ref') == 'refs/heads/master':
        # Git pull やその他のアクションを実行
        return "Success", 200
    else:
        return "No action needed", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)