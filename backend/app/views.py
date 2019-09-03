import functools
from datetime import datetime
from threading import Thread
from time import sleep
from flask_socketio import disconnect
from flask import redirect, url_for, session, current_app, jsonify
from flask import request, render_template
from flask.views import MethodView

from ctpbee import CtpBee, current_app as bee_current_app
from ctpbee import helper
from .default_settings import DefaultSettings, true_response, false_response
from .ext import io
from app.model import session, User
from app.auth import Auth, auth_required, heartbeat
from time import time

is_send = True


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


@io.on('my_connect')
def connect_handle(json):
    print('received message: ', json)
    if json == current_app.config['SOCKET_IO_KEY']:
        current_app.config['SOCKET_IO'] = int(time())
        io.emit('customEmit', 'ok')
    else:
        return False


@io.on('heartbeat')
def heartbeat_handle(token):
    result = heartbeat(token)
    if result['success']:
        current_app.config['SOCKET_HEARTBEAT'] = True
    else:
        current_app.config['SOCKET_HEARTBEAT'] = False


def socket_connect():
    """
    socket 连接
    :return:
    """
    if int(time()) - current_app.config.get('SOCKET_IO', 0) < 60:
        return True
    return False


class LoginView(MethodView):
    def post(self):
        if not socket_connect():
            return false_response(msg="登录出现错误:停留太久,刷新试试")

        from ctpbee import current_app as bee_current_app
        if bee_current_app != None:
            userid = bee_current_app.config["CONNECT_INFO"]['userid']
            token = Auth.authenticate(userid=userid)
            return token

        info = request.values
        print(info)
        app = CtpBee(name=info.get("username"), import_name=__name__)
        login_info = {
            "CONNECT_INFO": info,
            "INTERFACE": "ctp",
            "TD_FUNC": True,
            "MD_FUNC": True,
        }
        app.config.from_mapping(login_info)
        default = DefaultSettings("default_settings", app, io)
        app.start()
        sleep(1)
        if not app.td_login_status:
            return false_response(msg="登录出现错误")

        User.add(info)  # 写入数据库，无密码

        def run(app: CtpBee):
            while True:
                app.query_position()
                sleep(1)
                app.query_account()
                sleep(1)

        p = Thread(target=run, args=(app,))
        p.start()
        token = Auth.authenticate(userid=info.get('userid'))
        return token


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
            return false_response(mgs="撤单失败")


class WriteStrategy(MethodView):

    def get(self):
        session["count"] = 0
        session["time_now"] = datetime.now()
        return render_template("write_strategy.html")
