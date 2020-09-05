import socket

HOST = '127.0.0.1'
PORT = 5000


def not_closed():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
                if data == b'close':
                    return False
    return True


if __name__ == '__main__':
    while not_closed():
        pass
