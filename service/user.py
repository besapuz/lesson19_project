import base64
import hashlib
import hmac

from constants import ALGO, PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDao


class UserService:
    def __init__(self, dao: UserDao):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        return self.dao.get_username(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d["password"] = self.generate_password(user_d["password"])
        return self.dao.create(user_d)

    def update(self, user_d):
        user_d["password"] = self.generate_password(user_d["password"])
        self.dao.update(user_d)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

    def generate_password(self, password):
        hash_digest = base64.b64encode(hashlib.pbkdf2_hmac(
            ALGO,
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )).decode('utf-8')
        return hash_digest

    def compare_password(self, password_hash, other_password):
        # decoded_digest = base64.b64decode(password_hash)
        print(other_password)
        hash_digest = base64.b64encode(hashlib.pbkdf2_hmac(
            ALGO,
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )).decode('utf-8')
        print(hash_digest)
        return hmac.compare_digest(password_hash, hash_digest)
