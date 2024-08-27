# app/__init__.py

from flask import Flask
from app.routes.lain.view import lain_bp
from app.routes.webhook.view import webhook_bp
from app.routes.index import index_bp

def create_app():
    app = Flask(__name__)

    # ブループリントの登録
    app.register_blueprint(lain_bp)
    app.register_blueprint(webhook_bp)
    app.register_blueprint(index_bp)
    return app