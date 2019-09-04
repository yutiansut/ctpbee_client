class GVar:
    g = None

    @classmethod
    def init_app(cls, app):
        cls.g = app.config

    @property
    def current_user(self):
        return self.g.get('CURRENT_USER', {})

    @current_user.setter
    def current_user(self, userinfo):
        userinfo.pop('password', None)
        self.g['CURRENT_USER'] = userinfo

    @property
    def bee_app(self):
        return self.g.get('BEE_APP', None)

    @bee_app.setter
    def bee_app(self, beeapp):
        self.g['BEE_APP'] = beeapp

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
    def session(self, temp):
        """
        'session' : {
                token :{ },
                }
        :param temp: {  'token':token,
                        'data':{_:_},   }
        :return:
        """
        token = temp['token']
        data = temp['data']
        try:
            self.g['SESSION']
            se = self.g['SESSION']
            se[token].update(data)
        except Exception:
            self.g['SESSION'] = {}
            self.g['SESSION'][token] = data


G = GVar()
