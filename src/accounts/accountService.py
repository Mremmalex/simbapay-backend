from src.accounts.accountModel import EurAccount, NgnAccount, UsdAccount, db


def generateAccounts(user_id):
    eur = EurAccount(user_id=user_id)
    usd = UsdAccount(user_id=user_id)
    ngn = NgnAccount(user_id=user_id)
    db.session.add(eur)
    db.session.commit()
    db.session.add(usd)
    db.session.commit()
    db.session.add(ngn)
    db.session.commit()


def getEurAccount(user_id):
    eur = EurAccount.query.filter_by(user_id=user_id).first()
    return eur


def getUsdAccount(user_id):
    usd = UsdAccount.query.filter_by(user_id=user_id).first()
    return usd


def getNgnAccount(user_id):
    ngn = NgnAccount.query.filter_by(user_id=user_id).first()
    return ngn


def getEurAccountByAccNumber(account_num):
    eur = EurAccount.query.filter_by(account_num=account_num).first()
    return eur


def getEurAccountByUserId(user_id):
    eur = EurAccount.query.filter_by(user_id=user_id).first()
    return eur


def getUsdAccountByAccNumber(account_num):
    usd = UsdAccount.query.filter_by(account_num=account_num).first()
    return usd


def getUsdAccountByUserId(user_id):
    usd = UsdAccount.query.filter_by(user_id=user_id).first()
    return usd


def getNgnAccountByAccNumber(account_num):
    ngn = NgnAccount.query.filter_by(account_num=account_num).first()
    return ngn


def getNgnAccountByUserId(user_id):
    ngn = NgnAccount.query.filter_by(user_id=user_id).first()
    return ngn
