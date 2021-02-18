import socket

HOST = '127.0.0.1'
PORT = 8000  

count_line = 0
count_char = 0
secret_word = '--END--'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if data.strip() == secret_word.encode():
                break
            count_char += len(data.decode())
            count_line += 1
        response = f'Hello, Client! \nTotal lines: {count_line} \nTotal length: {count_char}\n'
        conn.sendall(response.encode())