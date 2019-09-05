import datetime
from functools import wraps
import time
import jwt
from flask import request, session

from app.setting import JWT_SECRET_KEY
from app.ext import log
from app.global_var import G
from app.default_settings import true_return, false_return, false_response, true_response


class Auth:
    @staticmethod
    def encode_auth_token(user_info):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        """
        "exp": 过期时间
        "nbf": 表示当前时间在nbf里的时间之前，则Token不被接受
        "iss": token签发者
        "aud": 接收者
        "iat": 发行时间
        """
        try:
            payload = {
                'exp': datetime.datetime.now() + datetime.timedelta(days=2, hours=0, seconds=0),
                # 'exp': datetime.datetime.now() + datetime.timedelta(seconds=10),  # test
                'iat': datetime.datetime.now(),
                'iss': 'looper_me',
                'data': user_info
            }
            return jwt.encode(
                payload,
                JWT_SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            log.error(e)
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: dict|string
        """
        try:
            payload = jwt.decode(auth_token, JWT_SECRET_KEY, leeway=datetime.timedelta(seconds=10))
            # payload = jwt.decode(auth_token, JWT_SECRET_KEY, options={'verify_exp': False})# 取消过期时间验证
            if 'data' in payload and 'userid' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    @staticmethod
    def authenticate(user):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param username
        :return:
        """
        user = dict(user)
        login_time = int(time.time())
        user_info = {
            "login_time": login_time,
            "userid": user.get('userid')
        }
        user.update(user_info)
        G.current_user = user  # current_user

        token = Auth.encode_auth_token(user_info).decode()
        G.session = dict(token=token, data=user_info)
        return true_response(data=token, msg='登录成功')

    @staticmethod
    def identify(request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_tokenArr = auth_header.split(" ")
            if not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2:
                result = false_return(msg='请传递正确的验证头信息')
            else:
                auth_token = auth_tokenArr[1]
                payload = Auth.decode_auth_token(auth_token)
                if isinstance(payload, str):
                    result = false_return(msg=payload)
                else:
                    user = G.current_user
                    if not user or user and user['userid'] != payload['data']['userid']:
                        log.error('找不到该用户信息')
                        result = false_return(msg='token error')
                    else:
                        if user['login_time'] == payload['data']['login_time']:
                            session['token'] = auth_token  # Strategy
                            result = true_return(data=user, msg='请求成功')
                        else:
                            log.error('Token已过期')
                            result = false_return(msg='token error')
        else:
            log.error('未提供token')
            result = false_return(msg='token error')
        return result


def auth_required(view_func):
    """
    装饰器，保护需登陆后操作的路由
    :param view_func: 视图函数
    :return:
    """

    @wraps(view_func)
    def wrapper(self, *args, **kwargs):
        result = Auth.identify(request)
        if result['success'] and result['data']:
            log.success("Token验证成功")
            return view_func(self, *args, **kwargs)
        else:
            return false_response(msg=result['msg'])

    return wrapper


def heartbeat(auth_token):
    payload = Auth.decode_auth_token(auth_token)
    if isinstance(payload, str):
        result = false_return(msg=payload)
    else:
        user = G.current_user
        if not user or user and user['userid'] != payload['data']['userid']:
            log.warn('心跳检测：找不到该用户信息')
            result = false_return()
        else:
            if user['login_time'] == payload['data']['login_time']:
                log.success('心跳检测：请求成功')
                result = true_return()
            else:
                log.warn('心跳检测：Token已过期')
                result = false_return()
    return result
