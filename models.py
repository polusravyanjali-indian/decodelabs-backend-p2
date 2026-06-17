from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(255), unique=True, nullable=False)
    age        = db.Column(db.Integer)
    is_active  = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id":         self.id,
            "email":      self.email,
            "age":        self.age,
            "is_active":  self.is_active,
            "created_at": str(self.created_at)
        }