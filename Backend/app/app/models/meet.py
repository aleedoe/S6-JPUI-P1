from . import db
from datetime import datetime

class Meet(db.Model):
    __tablename__ = 'meet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Meet {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "grade_id": self.grade_id,
            "created_at": self.created_at.isoformat()
        }