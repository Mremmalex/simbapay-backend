
from transactions.transactionModel import Transaction, db


def createTransaction():
    transsaction = Transaction()
    db.session.add(transsaction)
    db.session.commit()
