import os


class GVar:
    g = None
    authorization_path = os.path.dirname(__file__) + '/static/authorization.txt'

    @classmethod
    def init_app(cls, app):
        cls.g = app.config

    @property
    def mongo_token(self):
        return self.g.setdefault('MONGO_TOKEN', '2VhHgS5SX4rVTMKplFHIqndFooZykSL0')

    @property
    def authorization(self):
        return self.g['AUTHORIZATION']

    def load_authorization(self):
        """restart"""
        if os.path.exists(self.authorization_path):
            with open(self.authorization_path, 'r') as f:
                self.g['AUTHORIZATION'] = f.read()

    def check_authorization(self, code: str):
        from werkzeug.security import check_password_hash
        if check_password_hash(self.g['AUTHORIZATION'], code):
            return True
        return False

    @authorization.setter
    def authorization(self, code: str):
        from werkzeug.security import generate_password_hash
        au = generate_password_hash(code)
        self.g['AUTHORIZATION'] = au
        with open(self.authorization_path, 'w') as f:
            f.write(au)

    @property
    def current_user(self):
        self.g.setdefault('CURRENT_USER', {})
        return self.g['CURRENT_USER']

    @current_user.setter
    def current_user(self, userinfo: dict):
        self.g['CURRENT_USER'] = userinfo

    @property
    def session(self):
        self.g.setdefault('SESSION', {})
        return self.g['SESSION']

    @session.setter
    def session(self, raw: dict):
        token = raw['token']
        info = raw['data']
        se = self.g.get('SESSION')  # 获取session {}
        if se:
            se = self.g['SESSION']
            if len(se) > 3:
                temp = se.get(token, {})
                se.clear()  # 清空
                temp.update(info)
                se[token] = temp
            else:
                if se.get(token, None):  # 获取token字典
                    se[token].update(info)
                else:
                    se[token] = info  # session:{ token: info}
        else:
            self.g['SESSION'] = {}
            self.g['SESSION'][token] = info

    @property
    def log_history(self):
        self.g.setdefault('LOG_HISTORY', [])
        return self.g['LOG_HISTORY']


G = GVar()
