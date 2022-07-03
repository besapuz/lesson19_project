import calendar
import datetime

import jwt

from constants import PWD_HASH_SALT, ALGO, JWT_SECRET
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generation_token(self, username, password):
        user = self.user_service.get_by_username(username)
        print(user)
        if user is None:
            return "Пользователь не найден", 404

        if not self.user_service.compare_password(user.password, password):
            return "Пароль не совпадает", 400

        data = {
            "username": username,
            "password": password
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=ALGO)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=ALGO)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201
