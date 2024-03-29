from flask import request
from flask_restx import Resource, Namespace

from utilites.decorators import auth_required
from utilites.implemented import user_service
from utilites.secure import get_token_from_headers

user_ns = Namespace('user')


@user_ns.route("/")
class UserView(Resource):
    @auth_required
    def get(self):
        result = user_service.get()
        return result

    @auth_required
    def patch(self):
        data = request.json
        data["method"] = 'patch'
        data['token'] = get_token_from_headers(request.headers)
        result = user_service.update(data)
        return result


@user_ns.route("/password/")
class UserView(Resource):
    @auth_required
    def put(self):
        data = request.json
        data["method"] = 'put'
        data['token'] = get_token_from_headers(request.headers)
        result = user_service.update(data)
        return result
