from flask_socketio import SocketIO

io = SocketIO()


@io.on('my_connect')
def connect_handle(json):
    print('received message: ', json)
