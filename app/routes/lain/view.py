
from flask import Blueprint, render_template, jsonify
from app.utils.helpers import get_random_position

lain_bp = Blueprint('lain', __name__)

@lain_bp.route('/lain')
def lain():
    return render_template('lain/lain.html')

@lain_bp.route('/lain/add', methods=['POST'])
def lain_add():
    image_url = '/static/images/lain.gif'
    position = get_random_position()
    return jsonify(image_url=image_url, position=position)