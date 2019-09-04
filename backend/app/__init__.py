# this is the web client in here  you can use it to trade or read market fastly
from flask import Flask
from .ext import io
from .global_var import GVar
from .views import LoginView, MarketView, OpenOrderView, WriteStrategy
from .strategy_view import RunCode, CheckCode
from flask_cors import CORS


def create_app():
    app = Flask(__name__, static_folder="./static", template_folder="./templates")
    app.config.from_pyfile('setting.py')
    app.add_url_rule("/login", view_func=LoginView.as_view("login"), methods=["POST"])
    app.add_url_rule("/market", view_func=MarketView.as_view("market"), methods=["POST", "PUT"])
    app.add_url_rule("/order_solve", view_func=OpenOrderView.as_view("order_solve"), methods=['POST', 'DELETE'])

    app.add_url_rule("/write_strategy", view_func=WriteStrategy.as_view("write_strategy"), methods=['GET'])
    app.add_url_rule("/check_code", view_func=CheckCode.as_view("check_code"), methods=['POST'])
    app.add_url_rule("/run_code", view_func=RunCode.as_view("run_code"), methods=['POST'])
    io.init_app(app, cors_allowed_origins="*", manage_session=False)
    GVar.init_app(app)
    CORS(app)
    return app
