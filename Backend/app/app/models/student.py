from . import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    nis = db.Column(db.String(100), unique=True, nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=False)
    face_encoding = db.Column(db.String(225), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f'<Student {self.name}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "nis": self.nis,
            "grade_id": self.class_id,
            "photo_url": self.photo_url,
            "face_encoding": self.face_encoding,
            "created_at": self.created_at.isoformat()
        }