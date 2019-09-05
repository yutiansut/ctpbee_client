from datetime import datetime
from threading import Thread
from time import sleep
from flask import request, session
from flask.views import MethodView
from ctpbee import CtpBee, current_app as bee_current_app, del_app
from ctpbee import helper
from .default_settings import DefaultSettings, true_response, false_response
from .ext import io
from app.global_var import G
from app.auth import Auth, auth_required
from time import time
from app.helper import load_strategy, delete_strategy

is_send = True


@io.on('my_connect')
def connect_handle(key):
    print('connect(key): ', key)
    if key == G.socket_key:
        G.socket_connect = int(time())
        io.emit('customEmit', "ok")
    else:
        return False


def socket_connect():
    """
    socket 连接成功后才登录
    :return:
    """
    if int(time()) - G.socket_connect < 90:
        return True
    return False


class AuthCode(MethodView):
    @auth_required
    def put(self):
        password = request.values.get('password')
        code = request.values.get('authorization', "")
        if password == bee_current_app.trader.password and len(code) >= 6:
            G.authorization = code
            return true_response(msg='修改成功')
        return false_response(msg='修改失败')


class BeeQuery(Thread):
    def __init__(self, bee_app):
        super().__init__()
        self.bee_app = bee_app
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        while self._running:
            # print('run...',currentThread().ident)
            self.bee_app.query_position()
            sleep(1)
            self.bee_app.query_account()
            sleep(1)


class LoginView(MethodView):
    def post(self):
        if not socket_connect():
            return false_response(msg='停留太久,刷新试试')
        info = dict(request.values)
        authorization = info.pop('authorization', None)
        if not authorization or not G.check_authorization(authorization):
            return false_response(msg='authorization error')

        userid = info.get('userid')
        password = info.get('password')
        from ctpbee import current_app as bee_current_app
        if bee_current_app:
            if userid == bee_current_app.trader.userid and password == bee_current_app.trader.password:
                return Auth.authenticate(info)
            else:
                return false_response(msg='账户或密码错误')
        else:
            bee_app = CtpBee(name=info.get("username"), import_name=__name__)
            login_info = {
                "CONNECT_INFO": info,
                "INTERFACE": "ctp",
                "TD_FUNC": True,
                "MD_FUNC": True,
            }
            bee_app.config.from_mapping(login_info)
            default = DefaultSettings("default_settings", bee_app, io)
            load_strategy(bee_app)  # 加载策略
            bee_app.start()
            sleep(1)
            if not bee_app.td_login_status:
                return false_response(msg="登录出现错误")

            if G.bee_query:
                G.bee_query.stop()  # 停止线程
            p = BeeQuery(bee_app=bee_app)
            p.start()
            G.bee_query = p  # 线程加入

            token = Auth.authenticate(info)
            return token


class Logout(MethodView):
    @auth_required
    def get(self):
        del_app(__name__)
        G.current_user = None
        return true_response(msg='清除登录信息成功')


class MarketView(MethodView):
    @auth_required
    def post(self):
        symbol = request.values.get("symbol")
        try:
            bee_current_app.subscribe(symbol)
            return true_response(msg=f"订阅{symbol}成功")
        except Exception:
            return false_response(msg=f"订阅{symbol}失败")

    @auth_required
    def put(self):
        """ 更新contract"""
        try:
            contracts = [contract.symbol for contract in bee_current_app.recorder.get_all_contracts()]
            contracts.sort(key=lambda v: v.upper())
            io.emit("contract", contracts)
        except Exception:
            return false_response(msg="更新合约失败", )
        return true_response(msg="更新合约列表完成")


class OpenOrderView(MethodView):
    @auth_required
    def post(self):
        """ 发单 """
        info = request.values.to_dict()
        local_symbol = info.get("local_symbol")
        direction = info.get("direction")
        offset = info.get("offset")
        type = info.get("type")
        price = info.get("price")
        volume = info.get("volume")
        exchange = info.get("exchange")
        req = helper.generate_order_req_by_str(symbol=local_symbol,
                                               exchange=exchange,
                                               direction=direction, offset=offset, volume=int(volume),
                                               price=float(price),
                                               type=type)
        try:
            req_id = bee_current_app.send_order(req)
            sleep(0.2)
            order = bee_current_app.recorder.get_order(req_id)
            if order.status.value == "拒单":
                return false_response(msg=bee_current_app.recorder.get_new_error()['data']['ErrorMsg'])
            return true_response(msg="成功下单")
        except Exception as e:
            return false_response(msg="下单失败")

    @auth_required
    def delete(self):
        """ 撤单 """
        info = request.values
        local_symbol = info.get("local_symbol")
        order_id = info.get("order_id")
        exchange = info.get("exchange")
        req = helper.generate_cancel_req_by_str(symbol=local_symbol, exchange=exchange, order_id=order_id)
        try:
            bee_current_app.cancel_order(req)
            return true_response(msg="成功撤单")
        except Exception:
            return false_response(msg="撤单失败")


class Strategy(MethodView):
    @auth_required
    def get(self):
        G.session = dict(token=session['token'], data=dict(count=0, time_now=datetime.now()))
        result = []
        for k, v in bee_current_app.extensions.items():
            temp = {}
            temp['name'] = k
            temp['status'] = "停止" if v.frozen else "运行中"
            result.append(temp)
        return true_response(data=result)

    @auth_required
    def put(self):
        operation = request.values.get('operation')
        name = request.values.get('name')
        if name in bee_current_app.extensions:
            if operation == "开启":
                res = bee_current_app.enable_extension(name)
            elif operation == "关闭":
                res = bee_current_app.suspend_extension(name)
            else:
                res = 'unknown'
            res = '成功' if res is True else '失败'
            return true_response(msg=f'{operation} {name} {res}')
        return false_response(msg=f"{name} not found！")

    @auth_required
    def delete(self):
        name = request.values.get('name')
        if delete_strategy(name):
            return true_response(msg=f'删除{name}成功')
        return false_response(msg=f'删除{name}失败')
