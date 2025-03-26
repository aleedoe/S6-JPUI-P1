from . import db
from datetime import datetime
import enum

class Status(enum.Enum):
    S = "sakit"
    H = "hadir"
    I = "izin"
    A = "alpha"

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False)
    photo_url = db.Column(db.String(225), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Attendance {self.id}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "status": self.status.value,
            "photo_url": self.photo_url,
            "created_at": self.created_at.isoformat()
        }