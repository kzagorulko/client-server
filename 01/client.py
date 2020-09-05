import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5000         # The port used by the server

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str.encode(input('Enter message: ')))
        data = s.recv(1024)

    print(f'Received: "{data.decode("utf-8")}"')
