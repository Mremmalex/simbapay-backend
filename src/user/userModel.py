from utils.db import db
from nanoid import generate


nano = generate("1234567890", 10)
nano_id = generate("1234567899anyueiwoalmnbvc", 10)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, default=nano_id())
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self) -> str:
        return f"{self.username},:{self.email}"


class EurAccount(db.Model):
    __tablename__ = "eur_account"

    id = db.Column(db.Integer, primary_key=True)
    account_num = db.Column(db.String, unique=True default=nano())
    balance = db.Column(db.String)
    user_id = db.Column(db.Integer)


class NgnAccount(db.Model):
    __tablename__ = "ngn_account"

    id = db.Column(db.Integer, primary_key=True)
    account_num = db.Column(db.String, unique=True default=nano())
    balance = db.Column(db.Integer)
    user_id = db.Column(db.Integer)


class UsdAccount(db.Model):
    __tablename__ = "usd_account"

    id = db.Column(db.Integer, primary_key=True)
    account_num = db.Column(db.String, unique=True default=nano())
    balance = db.Column(db.Integer, default=1000)
    user_id = db.Column(db.Integer)
