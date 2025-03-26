from flask import Blueprint

user_bp = Blueprint('user_bp', __name__)

def register_blueprint_user(app):
    app.register_blueprint(user_bp)

@user_bp.route('/home/', methods=['GET'])
def home():
    return "Halo, Selamat datang di aplikasi Flask!"