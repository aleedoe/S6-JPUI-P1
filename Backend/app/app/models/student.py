from . import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    nis = db.Column(db.String(100), unique=True, nullable=False)
    class_id = db.Column(db.String(100), nullable=False)
    photo_url = db.Column(db.String(225), nullable=False)
    face_encoding = db.Column(db.String(225), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f'<Student {self.name}>'