from flask import Blueprint, Response, jsonify, make_response, request
from src.accounts.accountService import getEurAccountByAccNumber, getEurAccountByUserId, getNgnAccountByAccNumber, getNgnAccountByUserId, getUsdAccountByAccNumber, getUsdAccountByUserId
from src.middleware.requiredUser import required_user
from src.user.userService import getUserByUserId
from src.utils.jwtencode import decode_jwt
from src import db
from src.transactions.transactionService import createTransaction
import requests
import os


route = Blueprint("transaction", "transaction")


KEY = os.environ['CURRENCY_API_KEY']

url = f"https://api.getgeoapi.com/v2/currency/convert?api_key={KEY}"


@route.post("/api/auth/transfer")
@required_user()
def handle_transfer_money() -> Response:
    data = request.json
    currency = data['currency']
    account_num = data["account_num"]
    amount = data["amount"]

    json_token = request.headers.get(
        "Authorization") or request.cookies.get("accessToken")

    userData = decode_jwt(json_token)

    user_id = userData['payload'].get("user_id")

    loggedIn = getUserByUserId(user_id)

    if currency == "EUR":
        try:
            userEur = getEurAccountByAccNumber(account_num)
            user = getUserByUserId(userEur.user_id)
            loggedInUserAcc = getEurAccountByUserId(loggedIn.user_id)

            if loggedInUserAcc.account_num == account_num:
                return make_response(jsonify({"message": "you can not transfer to your account"}))
            else:
                if loggedInUserAcc.balance >= amount:
                    loggedInUserAcc.balance = loggedInUserAcc.balance - amount
                    db.session.commit()
                    userEur.balance = userEur.balance + amount
                    db.session.commit()
                    createTransaction(loggedIn.username,
                                      user.username, amount, currency, "send")
                    return make_response(jsonify({"message": "transfer Successfull",
                                                  "amount": amount}), 201)

                else:
                    return make_response(jsonify({"message": "You Currently do not have up to the amount",
                                                  "amount": amount}), 406)

        except AttributeError:

            return make_response(jsonify({"message": "No user with this Account"}), 406)

    elif currency == "USD":
        try:
            userUsd = getUsdAccountByAccNumber(account_num)
            user = getUserByUserId(userUsd.user_id)
            loggedInUserAcc = getUsdAccountByUserId(loggedIn.user_id)

            if loggedInUserAcc.account_num == account_num:
                return make_response(jsonify({"message": "you can not transfer to your account"}), 406)
            else:
                if loggedInUserAcc.balance >= amount:
                    loggedInUserAcc.balance = loggedInUserAcc.balance - amount
                    db.session.commit()
                    userUsd.balance = userUsd.balance + amount
                    db.session.commit()
                    createTransaction(loggedIn.username,
                                      user.username, amount, currency, "send")
                    return make_response(jsonify({"message": "transfer Successfull",
                                                  "amount": amount}), 201)

                else:
                    return make_response(jsonify({"message": "You Currently do not have up to the amount",
                                                  "amount": amount}), 406)
        except AttributeError:
            return make_response(jsonify({"message": "No user with this Account"}), 406)
    else:
        try:
            if currency == "NGN":
                userNgn = getNgnAccountByAccNumber(account_num)
                user = getUserByUserId(userNgn.user_id)
                loggedInUserAcc = getNgnAccountByUserId(loggedIn.user_id)
                if loggedInUserAcc.account_num == account_num:
                    return make_response(jsonify({"message": "you can not transfer to your account"}), 406)
                else:
                    if loggedInUserAcc.balance >= amount:
                        loggedInUserAcc.balance = loggedInUserAcc.balance - amount
                        db.session.commit()
                        userNgn.balance = userNgn.balance + amount
                        db.session.commit()
                        createTransaction(
                            loggedIn.username, user.username, amount, currency, "send")
                        return make_response(jsonify({"message": "transfer Successfull",
                                                      "amount": amount}), 201)

                    else:
                        return make_response(jsonify({"message": "You Currently do not have up to the amount",
                                                      "amount": amount}), 406)
        except AttributeError:
            return make_response(jsonify({"message": "No user with this Account"}), 406)

    return make_response(jsonify({"message": "Can not process this request"}), 406)


@route.post("/api/auth/convert")
@required_user()
def currency_conversion():
    data = request.json
    from_currency = data['from_currency']
    to_currency = data['to_currency']
    amount = data['amount']
    json_token = request.headers.get(
        "Authorization") or request.cookies.get("accessToken")
    user_data = decode_jwt(json_token)

    user_id = user_data["payload"].get("user_id")
    logged_in_user = getUserByUserId(user_id)
    if from_currency == "EUR":
        try:
            loggedInUserEurAcc = getEurAccountByUserId(logged_in_user.user_id)
            if to_currency == "USD":
                loggedInUserUsdAcc = getUsdAccountByUserId(
                    logged_in_user.user_id)
                querystring = {"format": "json", "from": "EUR",
                               "to": "USD", "amount": "1", "format": "json"}
                try:
                    response = requests.request("GET", url, params=querystring)

                    rate = response.json().get("rates")[
                        "USD"]['rate_for_amount']

                    amount_to_get = float(rate) * amount

                    if loggedInUserEurAcc.balance >= amount:
                        loggedInUserEurAcc.balance = loggedInUserEurAcc - amount
                        db.session.commit()
                        loggedInUserUsdAcc.balance = loggedInUserUsdAcc.balance + amount_to_get
                        db.session.commit()
                        return make_response(jsonify({"message": "conversion done", "status": 201}), 201)
                    else:
                        return make_response(jsonify({"message": "Not Enough Fund", "status": 400}), 400)
                except ConnectionError:
                    return make_response(jsonify({"message": "Internal Server Error", "status": 500}), 500)
            elif to_currency == "NGN":
                loggedInUserNgnAcc = getNgnAccountByUserId(
                    logged_in_user.user_id)
                querystring = {"format": "json", "from": "EUR",
                               "to": "NGN", "amount": "1", "format": "json"}
                try:
                    response = requests.request("GET", url, params=querystring)

                    rate = response.json().get("rates")[
                        "NGN"]['rate_for_amount']

                    amount_to_get = float(rate) * amount

                    if loggedInUserEurAcc.balance >= amount:
                        loggedInUserEurAcc.balance = loggedInUserEurAcc.balance - amount
                        db.session.commit()
                        loggedInUserNgnAcc.balance = loggedInUserEurAcc.balance - amount_to_get
                        db.session.commit()
                        return make_response(jsonify({"message": "conversion done", "status": 201}), 201)
                    else:
                        return make_response(jsonify({"message": "Not Enough Fund", "status": 400}), 400)
                except ConnectionError:
                    return make_response(jsonify({"message": "Internal Server Error", "status": 500}), 500)
        except AttributeError:
            return make_response(jsonify(({"message": "This Account does not exit", "status": 406})), 406)
    elif from_currency == "USD":
        try:
            loggedInUserUsdAcc = getUsdAccountByUserId(logged_in_user.user_id)
            if to_currency == "EUR":
                loggedInUserEurAcc = getEurAccountByUserId(
                    logged_in_user.user_id)
                querystring = {"format": "json", "from": "USD",
                               "to": "EUR", "amount": "1", "format": "json"}
                try:
                    response = requests.request("GET", url, params=querystring)

                    rate = response.json().get("rates")[
                        "EUR"]['rate_for_amount']

                    amount_to_get = float(rate) * amount
                    if loggedInUserUsdAcc.balance >= amount:
                        loggedInUserUsdAcc.balance = loggedInUserUsdAcc.balance - amount
                        db.session.commit()
                        loggedInUserEurAcc.balance = loggedInUserEurAcc.balance + amount_to_get
                        db.session.commit()
                        return make_response(jsonify({"message": "Conversion Done", "status": 201}), 201)
                    else:
                        return make_response(jsonify({"message": "Not Enough Fund", "status": 400}), 400)
                except ConnectionError:
                    return make_response(jsonify({"message": "Internal Server Error", "status": 500}), 500)
            elif to_currency == "NGN":
                loggedInUserNgnAcc = getNgnAccountByUserId(
                    logged_in_user.user_id)
                querystring = {"format": "json", "from": "USD",
                               "to": "NGN", "amount": "1", "format": "json"}
                try:
                    response = requests.request("GET", url, params=querystring)

                    rate = response.json().get("rates")[
                        "NGN"]['rate_for_amount']

                    amount_to_get = float(rate) * amount
                    if loggedInUserUsdAcc.balance >= amount:
                        loggedInUserUsdAcc.balance = loggedInUserUsdAcc.balance - amount
                        db.session.commit()
                        loggedInUserNgnAcc.balance = loggedInUserNgnAcc.balance + amount_to_get
                        db.session.commit()
                        return make_response(jsonify({"message": "Conversion Done", "status": 201}), 201)
                    else:
                        return make_response(jsonify({"message": "Not Enough Fund", "status": 400}), 400)
                except ConnectionError:
                    return make_response(jsonify({"message": "Internal Server Error", "status": 500}), 500)
        except AttributeError:
            return make_response(jsonify({"message": "This Account Does Not Exit", "status": 406}), 406)
    elif from_currency == "NGN":
        loggedInUserNgnAcc = getNgnAccountByUserId(
            logged_in_user.user_id)
        if to_currency == "EUR":
            loggedInUserEurAcc = getEurAccountByUserId(logged_in_user.user_id)
            querystring = {"format": "json", "from": "NGN",
                           "to": "EUR", "amount": "1", "format": "json"}
            try:
                response = requests.request("GET", url, params=querystring)

                rate = response.json().get("rates")[
                    "EUR"]['rate_for_amount']

                amount_to_get = float(rate) * amount

                if loggedInUserNgnAcc.balance >= amount:
                    loggedInUserNgnAcc.balance = loggedInUserNgnAcc - amount
                    db.session.commit()
                    loggedInUserEurAcc.balance = loggedInUserEurAcc.balance + amount_to_get
                    db.session.commit()
                    return make_response(jsonify({"message": "conversion done", "status": 201}), 201)
                else:
                    return make_response(jsonify({"message": "Not Enough Fund", "status": 400}), 400)
            except ConnectionError:
                return make_response(jsonify({"message": "Internal Server Error", "status": 500}), 500)
        elif to_currency == "USD":
            loggedInUserUsdAcc = getUsdAccountByUserId(
                logged_in_user.user_id)
            querystring = {"format": "json", "from": "NGN",
                           "to": "USD", "amount": "1", "format": "json"}
            try:
                response = requests.request("GET", url, params=querystring)

                rate = response.json().get("rates")[
                    "USD"]['rate_for_amount']

                amount_to_get = float(rate) * amount

                if loggedInUserNgnAcc.balance >= amount:
                    loggedInUserNgnAcc.balance = loggedInUserNgnAcc.balance - amount
                    db.session.commit()
                    loggedInUserUsdAcc.balance = loggedInUserUsdAcc.balance - amount_to_get
                    db.session.commit()
                    return make_response(jsonify({"message": "conversion done", "status": 201}), 201)
                else:
                    return make_response(jsonify({"message": "Not Enough Fund", "status": 400}), 400)
            except ConnectionError:
                return make_response(jsonify({"message": "Internal Server Error", "status": 500}), 500)
