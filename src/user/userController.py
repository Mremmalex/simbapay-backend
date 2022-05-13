from flask import Blueprint, jsonify, make_response, request, Response
from werkzeug.security import generate_password_hash, check_password_hash
from src.middleware.requiredUser import required_user
from src.accounts.accountService import generateAccounts, getEurAccountByAccNumber, getNgnAccountByAccNumber, getUsdAccountByAccNumber
from src.utils.jwtencode import decode_jwt, generate_jwt
from flask_expects_json import expects_json
import logging
from flask_cors import cross_origin
from src.user.userService import addUser, getUserByEmail, getUserByUserId, getUserByUsername


route = Blueprint("__name__", "user")
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.DEBUG)


@route.get("/api/auth/user")
def handle_user():
    json_token = request.headers.get(
        "Authorization") or request.cookies.get("accessToken")

    userData = decode_jwt(json_token)
    currentUser = getUserByUsername(userData['payload'].get("username"))
    payload = {
        "user_id": currentUser.user_id,
        "username": currentUser.username,
        "email": currentUser.email
    }
    return make_response(jsonify({'message': "welcome to user route",
                                  "data": payload}))


reg_schema = {
    'type': "object",
    'properties': {
        "username": {'type': 'string', "minLength": 4, "maxLength": 60},
        "email": {'type': 'string', "minLength": 10},
        "password": {'type': 'string', "minLength": 6},
    },
    "required": ['email', "username", "password"]
}
login_schema = {
    'type': "object",
    'properties': {
        "username": {'type': 'string', "minLength": 4, "maxLength": 60},

        "password": {'type': 'string', "minLength": 6},
    },
    "required": ["username", "password"]
}


@route.post("/api/auth/register")
@cross_origin()
@expects_json(reg_schema, check_formats=['email'])
def handle_register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    hashed_pwd = generate_password_hash(password.strip(), "sha256", 16)

    userExitsbyUsername = getUserByUsername(username)

    userExitsbyEmail = getUserByEmail(email)

    if userExitsbyUsername:
        return make_response(jsonify({'error':
                                      "username already in use",
                                      "status": 400,
                                      "statusText": "ok"}), 400)

    if userExitsbyEmail:
        return make_response(jsonify({'error':
                                      "email already in use",
                                      "status": 400,
                                      "statusText": "ok"}), 400)

    user = addUser(username=username, email=email,
                   password=hashed_pwd)

    generateAccounts(user.user_id)
    return make_response(jsonify({'message': "user registration successful",
                                  "data": {"user_id": user.user_id, "email":
                                             user.email, "username":
                                             user.username}}), 201)


@ route.post("/api/auth/login")
def handle_login_user():
    data = request.json
    username = data['username']
    password = data['password']

    user = getUserByUsername(username)
    if not user:
        return make_response(jsonify({"message":
                                     "user does not exit please create account"}))

    if check_password_hash(user.password, password):
        payload = {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email
        }

        jwteconded = generate_jwt(payload)
        resp = make_response(jsonify(
            {"message": "login successful",
             "token": jwteconded,
             "data": payload,
             "status": "ok",
             "statusCode": 200,
             }), 200)
        resp.set_cookie("accessToken", value=jwteconded, max_age=0.005e10)
        return resp

    else:
        return make_response(jsonify({"message": "password does not match"}))


@route.get("/api/auth/accountDetailsEur/<acc_num>")
@required_user()
def handle_user_with_eur_acoount(acc_num):
    userEur = getEurAccountByAccNumber(acc_num)
    user = getUserByUserId(userEur.user_id)
    if user:
        payload = {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email
        }
        return make_response(jsonify({"message": "happy to bring you user details",
                                      "data": payload}), 200)

    return make_response(jsonify({"error": "Service Not Avaliable"}), 301)


@route.get("/api/auth/accountDetailsUsd/<acc_num>")
@required_user()
def handle_user_with_usd_acoount(acc_num):
    userEur = getUsdAccountByAccNumber(acc_num)
    user = getUserByUserId(userEur.user_id)
    if user:
        payload = {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email
        }
        return make_response(jsonify({"message": "happy to bring you user details",
                                      "data": payload}), 200)

    return make_response(jsonify({"error": "Service Not Avaliable"}), 301)


@route.get("/api/auth/accountDetailsNgn/<acc_num>")
@required_user()
def handle_user_with_ngn_acoount(acc_num):
    userEur = getNgnAccountByAccNumber(acc_num)
    user = getUserByUserId(userEur.user_id)
    if user:
        payload = {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email
        }
        return make_response(jsonify({"message": "happy to bring you user details",
                                      "data": payload}), 200)

    return make_response(jsonify({"error": "Service Not Avaliable"}), 301)
