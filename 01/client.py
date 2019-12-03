from websocket import create_connection

if __name__ == "__main__":
    ws = create_connection('ws://localhost:12345/echo')
    message = input('input text: ')
    ws.send(message)
    print('Sent')
    print('Receiving...')
    result = ws.recv()
    print(f'Received:\n{result}')
    ws.close()
