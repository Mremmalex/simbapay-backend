from flask import Blueprint, jsonify, make_response

user = Blueprint("__name__", "user")


@user.get("/auth/user")
def handle_user():
    return make_response(jsonify({'message': "welcome user route"}))
