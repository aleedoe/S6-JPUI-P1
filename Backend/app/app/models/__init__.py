from flask_sqlalchemy import SQLAlchemy

# Inisialisasi database
db = SQLAlchemy()

from .user import User
from .attendance import Attendance
from .grade import Grade
from .student import Student
from .student_image import StudentImage
from .meet import Meet