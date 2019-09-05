import os


class GVar:
    g = None
    authorization_path = os.path.dirname(__file__) + '/static/authorization.txt'

    @classmethod
    def init_app(cls, app):
        cls.g = app.config

    @property
    def authorization(self):
        return self.g['AUTHORIZATION']

    def load_authorization(self):
        if os.path.exists(self.authorization_path):
            with open(self.authorization_path, 'r') as f:
                self.g['AUTHORIZATION'] = f.read()

    def check_authorization(self, code):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.g['AUTHORIZATION'], code)

    @authorization.setter
    def authorization(self, code):
        from werkzeug.security import generate_password_hash
        au = generate_password_hash(code)
        self.g['AUTHORIZATION'] = au
        with open(self.authorization_path, 'w') as f:
            f.write(au)

    @property
    def current_user(self):
        return self.g.get('CURRENT_USER', {})

    @current_user.setter
    def current_user(self, userinfo):
        userinfo.pop('password', None)
        self.g['CURRENT_USER'] = userinfo

    @property
    def bee_query(self):
        return self.g.get('BEE_QUERY', None)

    @bee_query.setter
    def bee_query(self, beequery):
        self.g['BEE_QUERY'] = beequery

    @property
    def socket_key(self):
        return self.g.get('SOCKET_KEY', None)

    @property
    def socket_connect(self):
        return self.g.get('SOCKET_CONNECT', 0)

    @socket_connect.setter
    def socket_connect(self, timestamp):
        self.g['SOCKET_CONNECT'] = timestamp

    @property
    def session(self):
        return self.g.get('SESSION', {})

    @session.setter
    def session(self, raw):
        token = raw['token']
        info = raw['data']
        se = self.g.get('SESSION')  # 获取session {}
        if se:
            if len(se) > 3:
                temp = se.get(token, {})
                se.clear()  # 清空
                temp.updata(info)
                se[token] = temp
            else:
                if se.get(token, None):  # 获取token字典
                    se[token].update(info)
                else:
                    se[token] = info  # session:{ token: info}
        else:
            self.g['SESSION'] = {}
            self.g['SESSION'][token] = info


G = GVar()
