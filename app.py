# app.py
from flask import Flask
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! This is a test update. os ubuntu, app flask and Python! 何が問題なのかわからない...多分動いてる動いて。。たのむfe'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # GitHub Webhookからのリクエストを受け取り
        payload = request.json
        # リポジトリのパスに移動
        os.chdir('/home/ubuntu/myflaskapp')
        # リポジトリを最新にプル
        subprocess.run(['git', 'pull'])
        # 必要に応じてアプリケーションを再起動
        subprocess.run(['sudo', 'systemctl', 'restart', 'myflaskapp'])
        return 'Success', 200
    else:
        return 'Failed', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)