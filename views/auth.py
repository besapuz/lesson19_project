from flask import request, abort
from flask_restx import Resource, Namespace

from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get("username", None)
        password = req_json.get("password", None)

        if None in [username, password]:
            abort(400)

        token = auth_service.generation_token(username, password)
        return token, 201

    def put(self):
        req_json = request.json
        token = req_json.get("refresh_token")
        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201