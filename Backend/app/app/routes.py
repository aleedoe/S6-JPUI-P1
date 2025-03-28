from flask import Blueprint

user_bp = Blueprint('user_bp', __name__)

def register_blueprint_user(app):
    app.register_blueprint(user_bp)

@user_bp.route('/', methods=['GET'])
def home():
    return "Halo, Selamat datang di aplikasi Flask!"



from app.controllers.attendance_service import take_attendance
attendance_bp = Blueprint('attendance', __name__)

def register_blueprint_attendance(app):
    app.register_blueprint(attendance_bp)

attendance_bp.route('/take-attendance', methods=['POST'])(take_attendance)


from app.controllers.main_face import register_student
student_bp = Blueprint('student', __name__)

def register_blueprint_student(app):
    app.register_blueprint(student_bp)

student_bp.route('/register-student', methods=['POST'])(register_student)