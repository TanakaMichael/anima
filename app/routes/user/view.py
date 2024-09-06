# app/routes/user/view.py

from flask import  request,Blueprint, render_template, redirect, url_for, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from functools import wraps
from app import db, limiter, login_manager
from app.model import User, GameProgress  # モデルをインポート
import requests
import os
user_bp = Blueprint('user', __name__, url_prefix='/user')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=25, message="ユーザー名は4文字以上25文字以下で入力してください。")
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="有効なメールアドレスを入力してください。")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="パスワードは8文字以上で入力してください。")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="パスワードが一致しません。")
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """ユーザー名の重複チェック"""
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError("ユーザー名は既に使用されています。")

    def validate_email(self, email):
        """メールアドレスの重複チェック"""
        existing_user = User.query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError("メールアドレスは既に使用されています。")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="有効なメールアドレスを入力してください。")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="パスワードは8文字以上で入力してください。")
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

@user_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # パスワードのハッシュ化
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        # ユーザーの作成
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        flash('アカウントが作成されました。', 'success')
        return redirect(url_for('user.login'))
    print(form.errors)
    return render_template('user/register.html', form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if user.account_locked_until and user.account_locked_until > datetime.now():
                lock_time = user.account_locked_until.strftime('%Y-%m-%d %H:%M:%S')
                flash(f'アカウントがロックされています。{lock_time}まで再度ログインしてください。', 'danger')
                return redirect(url_for('user.login'))

            # Reset login attempts
            user.login_attempts = 0
            db.session.commit()
            login_user(user, remember=True)
            flash('ログインに成功しました。', 'success')

            # Redirect to the search page after login
            return redirect(url_for('game.index'))
        else:
            if user:
                user.login_attempts += 1
                if user.login_attempts >= 5:
                    user.account_locked_until = datetime.now() + timedelta(minutes=10)
                    flash('アカウントがロックされました。', 'danger')
                else:
                    flash('メールアドレスまたはパスワードが間違っています。', 'danger')
                db.session.commit()
            else:
                flash('メールアドレスまたはパスワードが間違っています。', 'danger')
    return render_template('user/login.html', form=form)
@user_bp.route('/gate')
def gate():
    return render_template('gate/index.html')

@user_bp.route('/gate/about')
#@access_required(page_key='game', min_version=1)
def about():
    return render_template('gate/about.html')

@user_bp.route('/document')
def document():
    return render_template('gate/document.html')

@user_bp.route('/policy')
def policy():
    return render_template('gate/policy.html')

def access_required(page_key=None, min_version=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('ログインが必要です。', 'danger')
                return redirect(url_for('user.login'))
            
            # バージョンチェック
            if min_version is not None and current_user.version < min_version:
                flash('ゲームのバージョンが足りません。', 'danger')
                return redirect(url_for('user.gate'))
            
            # ページアクセス権限チェック
            if page_key is not None:
                progress = GameProgress.query.filter_by(user_id=current_user.id, page_access=page_key).first()
                if progress is None:
                    flash('アクセス権限がありません。', 'danger')
                    return redirect(url_for('user.gate'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
def grant_access_to_page(user, page_key):
    progress = GameProgress(page_access=page_key, user_id=user.id)
    db.session.add(progress)
    db.session.commit()
def grant_access_to_news(user):
    user.news_version = True
    db.session.commit()

def grant_access_to_community(user):
    user.community_version = True
    db.session.commit()

def grant_access_to_chat(user):
    user.chat_version = True
    db.session.commit()
def grant_access_to_voice(user):
    user.voice_version = True
    db.session.commit()

def has_access_to_page(user, page_key):
    """ユーザーが特定のページにアクセス可能かどうかを確認する"""
    return GameProgress.query.filter_by(user_id=user.id, page_access=page_key).first() is not None
def has_access_to_news(user):
    """ユーザーがnews_versionを持っているかどうかを確認する"""
    return user.news_version
def has_access_to_community(user):
    """ユーザーがcommunity_versionを持っているかどうかを確認する"""
    return user.community_version
def has_access_to_chat(user):
    """ユーザーがchat_versionを持っているかどうかを確認する"""
    return user.chat_version
def has_access_to_voice(user):
    """ユーザーがvoice_versionを持っているかどうかを確認する"""
    return user.voice_version

def get_all_log_pages():
    """すべてのログページを取得する関数"""
    logs_dir = os.path.join(current_app.root_path, 'templates', 'logs')
    all_pages = {}
    
    for filename in os.listdir(logs_dir):
        if filename.endswith('.html'):
            date_key = filename[:-5]  # ".html"を削除して日付キーを取得
            all_pages[date_key] = f'{date_key} Log'  # 任意でログの名前を設定
    
    return all_pages

def get_available_pages(user):
    """ユーザーが取得していないページを取得する関数"""
    all_pages = get_all_log_pages()
    acquired_keys = [progress.page_access for progress in user.game_progress.all()]
    available_pages = {key: name for key, name in all_pages.items() if key not in acquired_keys}
    return available_pages, acquired_keys