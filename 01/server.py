import re

from flask import Flask
from flask_sockets import Sockets


app = Flask(__name__)
sockets = Sockets(app)

RE_INT = re.compile(r'^[-+]?[0-9]+$')
RE_FLOAT = re.compile(r'\d+\.\d+|(?<=angle\s)\d+')


@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        text = ws.receive().split()

        integer_values = list(filter(lambda x: RE_INT.match(x), text))
        float_values = list(filter(lambda x: RE_FLOAT.match(x), text))
        another = list(filter(
            lambda x: x not in integer_values + float_values, text
        ))

        ws.send(
            f'integers:\t{integer_values}\nfloats:\t\t{float_values}\n'
            f'and e.t.c:\t{another}')


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(
        ('', 12345), app, handler_class=WebSocketHandler
    )
    server.serve_forever()
