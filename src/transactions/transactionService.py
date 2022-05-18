
from src.transactions.transactionModel import Transaction, db


def createTransaction(from_user, to_user, amount, currency_type, transaction_type):
    transaction = Transaction(from_user=from_user, to_user=to_user, amount=amount,
                              currency_type=currency_type, transaction_type=transaction_type)
    db.session.add(transaction)
    db.session.commit()
