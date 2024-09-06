from flask import Blueprint, render_template, jsonify
from app.utils.helpers import get_random_position

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    return render_template('index.html')

def gate():
    return render_template('gate.html')