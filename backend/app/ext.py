from flask_socketio import SocketIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

io = SocketIO()

limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "10 per hour"])
