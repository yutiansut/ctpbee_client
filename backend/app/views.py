from datetime import datetime
from time import sleep
from flask import request, session
from flask_socketio import disconnect
from flask.views import MethodView
from ctpbee import CtpBee, current_app as bee_current_app, del_app
from ctpbee import helper
from .default_settings import DefaultSettings, true_response, false_response
from .ext import io
from app.global_var import G
from app.auth import Auth, auth_required
from app.helper import load_strategy, delete_strategy


@io.on('connect')
def connect_handle():
    G.socket_blacklist.append(request.sid)


@io.on('disconnect')
def disconnect_handle():
    if request.sid in G.socket_blacklist:
        G.socket_blacklist.remove(request.sid)


@io.on('identify')
def identify_handle(json):
    if json['key'] == G.current_user['token']:
        io.emit('response', 'ok')
    else:
        try:
            disconnect(request.sid)
        except Exception as e:
            print("disconnect:", e)
    if request.sid in G.socket_blacklist:
        G.socket_blacklist.remove(request.sid)


class LoginView(MethodView):
    def post(self):
        """
        bee_app：   token if check userid,password else false_response
        not bee_app:  token if td_login_status else false_response
        :return:
        """
        info = dict(request.values)
        authorization = info.pop('authorization', None)
        if not authorization or not G.check_authorization(authorization):
            return false_response(msg='授权码错误')
        userid = info.get('userid')
        password = info.get('password')
        # bee_current_app存在
        if bee_current_app and \
                bee_current_app.trader and \
                bee_current_app.td_login_status:
            if userid == bee_current_app.trader.userid and password == bee_current_app.trader.password:
                token = Auth.authenticate(info)
                return true_response(data=token, msg='登录成功')
            return false_response(msg='Refuse!')

        else:  # bee_current_app 不不存在
            bee_app = CtpBee(name=info.get("username"), import_name=__name__, refresh=True)
            login_info = {
                "CONNECT_INFO": info,
                "INTERFACE": info.get('interface'),
                "TD_FUNC": True,
                "MD_FUNC": True,
            }
            bee_app.config.from_mapping(login_info)
            default = DefaultSettings("default_settings", bee_app, io)
            load_strategy(bee_app)  # 加载策略
            bee_app.start()
            sleep(1)

            if bee_current_app and \
                    bee_current_app.trader and \
                    bee_current_app.td_login_status:
                token = Auth.authenticate(info)

                return true_response(data=token, msg='重新登录成功')
            else:
                del_app(__name__)
                return false_response(msg="重新登录出现错误")


class LogoutView(MethodView):
    @auth_required
    def post(self):
        auth_code = request.values.get('authorization', "")
        if auth_code and len(auth_code) > 6 and G.check_authorization(auth_code):
            del_app(__name__)
            G.current_user.clear()
            print("bee_app： ", bee_current_app)
            return true_response(msg='服务器已安全退出')
        else:
            return false_response(msg='授权码错误')


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
            print("contract", contracts)
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


class StrategyView(MethodView):
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


class AuthCodeView(MethodView):
    @auth_required
    def put(self):
        password = request.values.get('password')
        code = request.values.get('authorization', "")
        if password == bee_current_app.trader.password and len(code) >= 6:
            G.authorization = code
            return true_response(msg='修改成功')
        return false_response(msg='修改失败')
