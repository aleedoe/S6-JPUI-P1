from . import db
from datetime import datetime
import enum


class Role(enum.Enum):
    A = "admin"
    G = "guru"


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender.value,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }