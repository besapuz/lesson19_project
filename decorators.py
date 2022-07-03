import jwt
from flask import request, abort

from constants import JWT_SECRET


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token_ = data.split('Bearer ')[-1]
        try:
            jwt.decode(token_, JWT_SECRET, algorithms="HS256")
        except Exception:
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(funk):
    def wrapper(*args, **kwargs):

        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            user_decode = jwt.decode(token, JWT_SECRET, algorithms="HS256")
            role = user_decode.get("role")
        except Exception as e:
            print(f"JWT decode {e}")
            abort(401)

        if role != "admin":
            abort(403)

        return funk(*args, **kwargs)

    return wrapper
