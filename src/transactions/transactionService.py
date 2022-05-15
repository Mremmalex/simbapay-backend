
from transactions.transactionModel import Transaction, db


def createTransaction(from_user, to_user, amount, currency_type, transaction_type):
    transsaction = Transaction(
        from_user, to_user, amount, currency_type, transaction_type)
    db.session.add(transsaction)
    db.session.commit()
