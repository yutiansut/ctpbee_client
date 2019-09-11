from flask import request
from flask.views import MethodView
from app.auth import auth_required
from ctpbee import current_app as bee_current_app
from app.default_settings import true_response, false_response


class ConfigView(MethodView):
    @auth_required
    def get(self):
        config = bee_current_app.config
        return true_response(data=config)

    @auth_required
    def put(self):
        key = request.values.get('key')
        value = request.values.get('value')
        if key not in bee_current_app.config:
            return false_response(msg='key error')
        bee_current_app.config[key] = value
        return true_response(msg='修改成功')
