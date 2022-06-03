from datetime import datetime
from nanoid import generate
from src import db

nano_txn = generate("1234567780", 8)


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    trans_id = db.Column(db.String, unique=True, default=nano_txn)
    from_user = db.Column(db.String)
    to_user = db.Column(db.String)
    amount = db.Column(db.Integer)
    currency_type = db.Column(db.String)
    transaction_type = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
