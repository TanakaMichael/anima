from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
import os
from app.model import GameProgress
from app.routes.user.view import access_required, grant_access_to_page, has_access_to_page, get_available_pages, has_access_to_news, has_access_to_community, has_access_to_chat, grant_access_to_news, grant_access_to_community, grant_access_to_chat, has_access_to_voice, grant_access_to_voice
from app import db
from flask_wtf import FlaskForm
game_bp = Blueprint('game', __name__)
class UpgradeForm(FlaskForm):
    pass
# アクセス制御が必要なページを定義
restricted_pages = {
    # キーがあればアクセスできるページ
    '2024-12-24': {'page_key': '2024-12-24'},
    
    # バージョンが足りていればアクセスできるページ
    '2024-12-25': {'min_version': 2},
    
    # キーとバージョンの両方が必要なページ
    '2024-11-25': {'min_version': 3, 'page_key': '2024-11-25'},
    
    # バージョンもキーも必要ないページ
    # '2024-09-01': {} のように空の辞書を使うか、リストから除外して定義しない
}

@game_bp.route('/game/<string:date>', methods=['GET'])
@login_required
def view_log(date):
    # アクセス制御が必要なページかどうかをチェック
    if date in restricted_pages:
        page_info = restricted_pages[date]
        
        # キーチェックが必要か
        if 'page_key' in page_info and not has_access_to_page(current_user, page_info['page_key']):
            flash('アクセス権限がありません。', 'danger')
            return redirect(url_for('game.index'))

        # バージョンチェックが必要か
        if 'min_version' in page_info and current_user.version < page_info['min_version']:
            flash('ゲームのバージョンが足りません。', 'danger')
            return redirect(url_for('game.index'))
        base_path = os.path.join('templates/logs', date)
        
    log_file_path = os.path.join('app/templates/logs', f'{date}')

    if not os.path.exists(log_file_path):
        flash('その日のログは存在しません。', 'warning')
        return redirect(url_for('game.index'))
    # 各コンテンツの存在チェック app/でないとos.path.joinはうごかない
    community_available = os.path.exists(os.path.join("app/" + base_path, 'community.html'))
    chat_available = os.path.exists(os.path.join("app/" + base_path, 'chat.html'))
    news_available = os.path.exists(os.path.join("app/" + base_path, 'news.html'))
    voice_available = os.path.exists(os.path.join("app/" + base_path, 'voice.html'))
    if not community_available and not chat_available and not news_available:
        # コンテンツが一つもない場合は404を返す
        print(f"コンテンツが一つもない場合は404を返す{base_path}")
        abort(404)
    
    return render_template(
        f'logs/{date}/index.html',
        date=date,
        community_available=community_available,
        chat_available=chat_available,
        news_available=news_available,
        voice_available=voice_available
    )

@game_bp.route('/game/<string:date>/<string:content>', methods=['GET'])
@login_required
def view_log_content(date, content):
    # 例えば、バージョンやアクセス権のチェックをここで行う
    if content == 'news':
        if not has_access_to_news(current_user):
            flash('ニュースにアクセスする権限がありません。', 'danger')
            return redirect(request.referrer or url_for('game.index'))
    elif content == 'community':
        if not has_access_to_community(current_user):
            flash('コミュニティにアクセスする権限がありません。', 'danger')
            return redirect(request.referrer or url_for('game.index'))
    elif content == 'chat':
        if not has_access_to_chat(current_user):
            flash('チャットにアクセスする権限がありません。', 'danger')
            return redirect(request.referrer or url_for('game.index'))
    elif content == 'voice':
        if not has_access_to_voice(current_user):
            flash('ボイスにアクセスする権限がありません。', 'danger')
            return redirect(request.referrer or url_for('game.index'))

    content_path = os.path.join('app/templates/logs', date, f'{content}.html')
    
    if not os.path.exists(content_path):
        print(f"{content_path}が存在しません. htmlファイルがありません")
        abort(404)
    
    return render_template(f'logs/{date}/{content}.html')
@game_bp.route('/game', methods=['GET'])
@login_required
def index():
    available_pages, acquired_keys = get_available_pages(current_user)
    return render_template('past-relics/index.html', available_pages=available_pages, acquired_keys=acquired_keys)

@game_bp.route('/game/grant_key/<string:page_key>', methods=['GET'])
@login_required
def grant_key(page_key):
    if not has_access_to_page(current_user, page_key):
        grant_access_to_page(current_user, page_key)
        flash(f'{page_key}のキーを取得しました。', 'success')
    else:
        flash(f'{page_key}のキーは既に取得済みです。', 'info')
    
    # 直前のページにリダイレクトする
    return redirect(request.referrer or url_for('game.index'))
@game_bp.route('/game/grant_news/', methods=['GET'])
@login_required
def grant_news():
    if not has_access_to_news(current_user):
        grant_access_to_news(current_user)
        flash(f'newsのアクセス権を取得しました。', 'success')
    else:
        flash(f'newsのアクセス権は既に取得済みです。', 'info')
    
    # 直前のページにリダイレクトする
    return redirect(request.referrer or url_for('game.index'))
@game_bp.route('/game/grant_community/', methods=['GET'])
@login_required
def grant_community():
    if not has_access_to_community(current_user):
        grant_access_to_community(current_user)
        flash(f'communityのアクセス権を取得しました。', 'success')
    else:
        flash(f'communityのアクセス権は既に取得済みです。', 'info')

    # 直前のページにリダイレクトする
    return redirect(request.referrer or url_for('game.index'))
@game_bp.route('/game/grant_chat/', methods=['GET'])
@login_required
def grant_chat():
    if not has_access_to_chat(current_user):
        grant_access_to_chat(current_user)
        flash(f'chatのアクセス権を取得しました。', 'success')
    else:
        flash(f'chatのアクセス権は既に取得済みです。', 'info')

    # 直前のページにリダイレクトする
    return redirect(request.referrer or url_for('game.index'))
@game_bp.route('/game/grant_voice/', methods=['GET'])
@login_required
def grant_voice():
    if not has_access_to_voice(current_user):
        grant_access_to_voice(current_user)
        flash(f'voiceのアクセス権を取得しました。', 'success')
    else:
        flash(f'voiceのアクセス権は既に取得済みです。', 'info')

@game_bp.route('/game/keys', methods=['GET'])
@login_required
def keys():
    user = current_user
    keys = GameProgress.query.filter_by(user_id=user.id).all()
    return render_template('past-relics/keys.html', keys=keys)

@game_bp.route('/upgrade_version', methods=['GET'])
@login_required
def upgrade_version():
    # 演出ページを表示
    return render_template('past-relics/upgrade.html', form=UpgradeForm())

@game_bp.route('/perform_upgrade', methods=['POST'])
@login_required
def perform_upgrade():
    # ユーザーのバージョンを1段階上げる
    current_user.version += 1
    db.session.commit()
    flash('バージョンアップが完了しました！', 'success')
    
    # 元のページに戻す
    return redirect(url_for('game.index'))

@game_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('past-relics/profile.html', user=current_user)