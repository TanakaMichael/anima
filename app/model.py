# app/model.py
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime, nullable=True)
    version = db.Column(db.Integer, default=1)  # バージョンをUserに組み込む
    chat_version = db.Column(db.Boolean, default=False)
    community_version = db.Column(db.Boolean, default=True)
    news_version = db.Column(db.Boolean, default=False)
    voice_version = db.Column(db.Boolean, default=False)
    game_progress = db.relationship('GameProgress', backref='user', lazy='dynamic')

class GameProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_access = db.Column(db.String(100), nullable=False)  # アクセス許可されたページ
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)