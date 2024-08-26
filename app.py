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
    data = request.get_json()
    if data is None:
        return "Invalid data", 400
    
    # デバッグ用に受信したデータをプリント
    print(data)
    
    if data.get('ref') == 'refs/heads/master':
        try:
            # Gitリポジトリを最新に更新
            subprocess.run(['/usr/bin/git', 'pull'], cwd='/home/ubuntu/myflaskapp', check=True)
            # Flaskアプリケーションを再起動
            subprocess.run(['sudo', 'systemctl', 'restart', 'myflaskapp'], check=True)
            return "Success", 200
        except subprocess.CalledProcessError as e:
            # もしGit pullやアプリケーションの再起動に失敗した場合、エラーメッセージを返す
            print(f"Error during webhook processing: {e}")
            return f"Error during webhook processing: {str(e)}", 500
    else:
        return "No action needed", 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)