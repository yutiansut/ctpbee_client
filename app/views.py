from datetime import datetime
from threading import Thread
from time import sleep

from flask import redirect, url_for, session, current_app
from flask import request, render_template
from flask.views import MethodView

from ctpbee import CtpBee, current_app as bee_current_app
from ctpbee import helper
from .default_settings import DefaultSettings, true_response, false_response
from .ext import io

is_send = True


def login_required(f):
    """Checks whether user is logged in or raises error 401."""

    def decorator(*args, **kwargs):
        try:
            if not current_app.config.get("CURRENT_USER"):
                return redirect(url_for('login'))
        except NameError:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorator


class AccountView(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("account.html")


class LoginView(MethodView):
    def get(self):
        return render_template("login.html")

    def post(self):
        from ctpbee import current_app as bee_current_app
        if bee_current_app != None:
            current_app.config['CURRENT_USER'] = bee_current_app.config["CONNECT_INFO"]['userid']
            return true_response(message="登录成功")
        info = request.values
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
            return false_response(message="登录出现错误")
        app.config['CURRENT_USER'] = login_info['CONNECT_INFO']['userid']

        def run(app: CtpBee):
            while True:
                app.query_position()
                sleep(1)
                app.query_account()
                sleep(1)

        p = Thread(target=run, args=(app,))
        p.start()
        return true_response(message="登录成功")


class IndexView(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("index.html", username=current_app.config.get('CURRENT_USER'))


class MarketView(MethodView):
    decorators = [login_required]

    def post(self):
        symbol = request.values.get("symbol")
        try:
            bee_current_app.subscribe(symbol)
            return true_response(message=f"订阅{symbol}成功")
        except Exception:
            return false_response(message=f"订阅{symbol}失败")

    def put(self):
        """ 更新contract"""
        try:
            contracts = [contract.symbol for contract in bee_current_app.recorder.get_all_contracts()]
            io.emit("contract", contracts)
        except Exception:
            return false_response(message="更新合约失败", )
        return true_response(message="更新合约列表完成")

    def get(self):
        return render_template("market.html")


class OrderView(MethodView):
    decorators = [login_required]

    def get(self, symbol):
        return render_template("send_order.html", symbol=symbol)


class OpenOrderView(MethodView):
    decorators = [login_required]

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
                return false_response(message=bee_current_app.recorder.get_new_error()['data']['ErrorMsg'])
            return true_response(message="成功下单")
        except Exception as e:
            return false_response(message="下单失败")

    def delete(self):
        """ 撤单 """
        info = request.values
        local_symbol = info.get("local_symbol")
        order_id = info.get("order_id")
        exchange = info.get("exchange")
        req = helper.generate_cancel_req_by_str(symbol=local_symbol, exchange=exchange, order_id=order_id)
        try:
            bee_current_app.cancel_order(req)
            return true_response(message="成功撤单")
        except Exception:
            return false_response(message="撤单失败")


class LogoutView(MethodView):
    decorators = [login_required]

    def get(self):
        current_app.config['CURRENT_USER'] = None
        return true_response(message="注销成功")


class WriteStrategy(MethodView):
    decorators = [login_required]

    def get(self):
        session["count"] = 0
        session["time_now"] = datetime.now()
        return render_template("write_strategy.html")
