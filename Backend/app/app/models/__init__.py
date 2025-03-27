from flask_sqlalchemy import SQLAlchemy

# Inisialisasi database
db = SQLAlchemy()

from .user import User
from .attendance import Attendance
from ._class import Class
from .student import Student
