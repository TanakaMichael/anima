# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from itsdangerous import URLSafeTimedSerializer
import os
# 各種拡張機能のインスタンス化
csrf = CSRFProtect()
db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address, default_limits=["1000 per day", "100 per hour"])
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mysecretkey')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
    
    # 拡張機能の初期化
    csrf.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    with app.app_context():
        from app.model import User
        db.create_all()
    # Blueprint の登録
    from app.routes.user.view import user_bp
    from app.routes.lain.view import lain_bp
    from app.routes.webhook.view import webhook_bp
    from app.routes.index import index_bp
    from app.routes.past_relics.view import game_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(lain_bp)
    app.register_blueprint(webhook_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(game_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.model import User  # ここでUserをインポート
    return User.query.get(int(user_id))