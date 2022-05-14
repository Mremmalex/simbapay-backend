from flask import Blueprint, Response, jsonify, make_response, request
from src.accounts.accountService import getEurAccountByAccNumber, getEurAccountByUserId, getNgnAccountByAccNumber, getNgnAccountByUserId, getUsdAccountByAccNumber, getUsdAccountByUserId
from src.middleware.requiredUser import required_user
from src.user.userService import getUserByUserId
from src.utils.jwtencode import decode_jwt
from src.worker import db


route = Blueprint("transaction", "transaction")


@route.post("/api/auth/transfer")
@required_user()
def handle_transfer_money() -> Response:
    data = request.json
    currency = data['currency']
    account_num = data["account_num"]
    amount = data["ammount"]

    json_token = request.headers.get(
        "Authorization") or request.cookies.get("accessToken")

    userData = decode_jwt(json_token)

    user_id = userData['payload'].get("user_id")

    loggedIn = getUserByUserId(user_id)

    if currency == "eur":
        try:
            userEur = getEurAccountByAccNumber(account_num)
            user = getUserByUserId(userEur.user_id)

            loggedInUserAcc = getEurAccountByUserId(loggedIn.user_id)
            if loggedInUserAcc.balance >= amount:
                loggedInUserAcc.balace = loggedInUserAcc.balance - amount
                userEur.balance = userEur.balance + amount
                db.session.commit()
                return make_response(jsonify({"message": "transfer Successfull",
                                              "amount": amount}))

            else:
                return make_response(jsonify({"message": "You Currently do not have up to the amount",
                                              "amount": amount}))

        except AttributeError:

            return make_response(jsonify({"error": "No user with this Account"}))

    elif currency == "usd":
        try:
            userUsd = getUsdAccountByAccNumber(account_num)
            user = getUserByUserId(userUsd.user_id)
            loggedInUserAcc = getUsdAccountByUserId(loggedIn.user_id)
            if loggedInUserAcc.balance >= amount:
                loggedInUserAcc.balace = loggedInUserAcc.balance - amount
                userEur.balance = userEur.balance + amount
                db.session.commit()
                return make_response(jsonify({"message": "transfer Successfull",
                                              "amount": amount}))

            else:
                return make_response(jsonify({"message": "You Currently do not have up to the amount",
                                              "amount": amount}))
        except AttributeError:
            return make_response(jsonify({"error": "No user with this Account"}))
    else:
        try:
            if currency == "ngn":
                userNgn = getNgnAccountByAccNumber(account_num)
                user = getUserByUserId(userNgn.user_id)
                loggedInUserAcc = getNgnAccountByUserId(loggedIn.user_id)
                if loggedInUserAcc.balance >= amount:
                    loggedInUserAcc.balace = loggedInUserAcc.balance - amount
                    userEur.balance = userEur.balance + amount
                    db.session.commit()
                    return make_response(jsonify({"message": "transfer Successfull",
                                                  "amount": amount}))

                else:
                    return make_response(jsonify({"message": "You Currently do not have up to the amount",
                                                  "amount": amount}))
        except AttributeError:
            return make_response(jsonify({"error": "No user with this Account"}))

    return make_response(jsonify({"error": "Service Not Avaliable"}), 301)
