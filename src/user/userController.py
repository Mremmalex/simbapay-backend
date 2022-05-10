from flask import Blueprint, jsonify, make_response
from src.user.userModel import User, db

route = Blueprint("__name__", "user")


@route.get("/auth/user")
def handle_user():
    return make_response(jsonify({'message': "welcome user route"}))


@route.get("/auth")
def handle_register_user():
    user = User(username="emma", email="djdh@gmail.com", password="holy5555")
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify({'res': "user register"}))
