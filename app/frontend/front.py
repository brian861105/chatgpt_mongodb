from flask import Blueprint, send_file
from backend.src.Database import DatabaseManager

database = DatabaseManager()
static_server_bp = Blueprint('static_server', __name__)
@static_server_bp.route('/chatroom')
def index():
    return send_file('frontend/template/chatroom.html', database.ReadUser(UserId="TestForFront"))