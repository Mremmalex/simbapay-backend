import jwt
import os


def generate_jwt(payload):
    jwt_token = jwt.encode(
        payload, os.environ["SECRET_KEY"], "HS256", {"exp": 123476487})
    return jwt_token


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, os.environ['SECRET_KEY'], "HS256")
        return {
            "valid": True,
            "payload": payload
        }
    except jwt.ExpiredSignatureError:
        return {
            "valid": False,
            "error": "accessToken Expired"
        }
