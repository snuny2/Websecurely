from flask import Blueprint, send_from_directory

from appmain import app

# 객체 생성
main = Blueprint('main', __name__)

# /home
@main.route('/')
@main.route('/home')
def home():
    return send_from_directory(app.root_path, 'templates/index.html')