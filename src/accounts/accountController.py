
from flask import Blueprint, jsonify, make_response
from src.accounts.accountService import getEurAccount, getNgnAccount, getUsdAccount
from src.middleware.requiredUser import required_user


route = Blueprint("accounts", "accounts")


@route.get("/api/auth/accounts/<user_id>")
def handle_user_accounts(user_id):
    eur = getEurAccount(user_id)
    usd = getUsdAccount(user_id)
    ngn = getNgnAccount(user_id)
    payload = {
        "eur": {
            "account_num": eur.account_num,
            "balance": eur.balance
        },
        "usd": {
            "account_num": usd.account_num,
            "balance": usd.balance
        },
        "ngn": {
            "account_num": ngn.account_num,
            "balance": ngn.balance
        }
    }
    return make_response(jsonify({"res": payload})), 200
