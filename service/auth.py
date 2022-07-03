import calendar
import datetime

import jwt

from constants import ALGO, JWT_SECRET
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generation_token(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)

        if user is None:
            return "Пользователь не найден", 404

        if not is_refresh:
            if not self.user_service.compare_password(user.password, password):
                return "Пароль не совпадает", 400

        data = {
            "username": username,
            "password": password
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        print(data["exp"])
        access_token = jwt.encode(data, JWT_SECRET, algorithm="HS256")

        days30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data["exp"] = calendar.timegm(days30.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm="HS256")
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms="HS256")
        username = data.get("username")
        return self.generation_token(username, None, is_refresh=True)
