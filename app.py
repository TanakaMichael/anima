# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! This is a test update. os ubuntu, app flask and Python! エラーが起こるたびに白髪が増える...imifumeiaewgfawddhgasfgawdtf'

if __name__ == '__main__':
    app.run(debug=True)