
from functools import wraps
from flask import jsonify, make_response, request
from src.utils.jwtencode import decode_jwt


def required_user():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            json_token = request.headers.get("accessToken").strip()
            decode = decode_jwt(json_token)
            if decode["valid"] is False:
                return make_response(jsonify({'status': "error",
                                              "message": "AccessToken has Expired please login"}))
            return fn(*args, **kwargs)
        return wrapper
    return decorator
