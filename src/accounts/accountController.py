
from flask import Blueprint, jsonify, make_response, request
from src.accounts.accountService import getEurAccount, getNgnAccount, getUsdAccount
from src.middleware.requiredUser import required_user
from src.utils.jwtencode import decode_jwt


route = Blueprint("accounts", "accounts")


@route.get("/api/auth/accounts")
@required_user()
def handle_user_accounts():
    json_token = request.headers.get(
        "Authorization") or request.cookies.get("accessToken")

    userData = decode_jwt(json_token)

    user_id = userData['payload'].get("user_id")
    try:
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
        return make_response(jsonify({"data": payload})), 200
    except AttributeError:

        return make_response(jsonify({"message": "account could not be retrieved"}))
