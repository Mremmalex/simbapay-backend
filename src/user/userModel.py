from datetime import datetime
from nanoid import generate
from src.worker import db


nano_id = generate("1234567899anyueiwoalmnbvc", 13)



class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, default=nano_id)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self) -> str:
        return f"{self.username},:{self.email}"

