from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
from server import MyTCPHandler


HOST = '127.0.0.1'
PORT = 8000


class ThereadedTCPServer(ThreadingMixIn, TCPServer):
    pass

if __name__ == '__main__':
    ThereadedTCPServer.allow_reuse_address = True
    with ThereadedTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()