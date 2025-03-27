from . import db
from datetime import datetime

class StudentImage(db.Model):
    __tablename__ = 'student_image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    image_url = db.Column(db.String(225), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'image_url': self.image_url,
            'created_at': self.created_at
        }