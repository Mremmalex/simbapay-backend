from src.accounts.accnum import accounGen
from src.worker import db


class EurAccount(db.Model):
    __tablename__ = "eur_account"

    id = db.Column(db.Integer, primary_key=True)
    account_num = db.Column(db.String, unique=True, default=accounGen())
    balance = db.Column(db.Integer, default=0)
    user_id = db.Column(db.String, nullable=False)


class NgnAccount(db.Model):
    __tablename__ = "ngn_account"

    id = db.Column(db.Integer, primary_key=True)
    account_num = db.Column(db.String, unique=True, default=accounGen())
    balance = db.Column(db.Integer, default=0)
    user_id = db.Column(db.String, nullable=False)


class UsdAccount(db.Model):
    __tablename__ = "usd_account"

    id = db.Column(db.Integer, primary_key=True)
    account_num = db.Column(db.String, unique=True, default=accounGen())
    balance = db.Column(db.Integer, default=1000)
    user_id = db.Column(db.String, nullable=False)
