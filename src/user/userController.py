from flask import Blueprint, jsonify, make_response, request
from flask.typing import StatusCode
from werkzeug.security import generate_password_hash, check_password_hash
from src.accounts.accountService import generateAccounts
from src.utils.validtaion import solve
from src.utils.jwtencode import generate_jwt
from flask_expects_json import expects_json
import logging
from flask_cors import cross_origin
from src.user.userService import addUser, getUserByEmail, getUserByUsername

route = Blueprint("__name__", "user")
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.DEBUG)


@route.get("/api/auth/user")
def handle_user():
    return make_response(jsonify({'message': "welcome to user route"}))


reg_schema = {
    'type': "object",
    'properties': {
        "username": {'type': 'string', "minLength": 4, "maxLength": 60},
        "email": {'type': 'string', "minLength": 10},
        "password": {'type': 'string', "minLength": 6},
    },
    "required": ['email', "username", "password"]
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
        return make_response(jsonify({'message':
                                      "username already in use",
                                      "status": 400,
                                      "statusText": "ok"},
                                     )),
    if userExitsbyEmail:
        return make_response(jsonify({'message':
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
        return make_response(jsonify(
            {"message": "login successful",
             "token": jwteconded,
             "data": payload,
             "status": "ok",
             "statusCode": 200,
             })), 200
    else:
        return make_response(jsonify({"message": "password does not match"}))
