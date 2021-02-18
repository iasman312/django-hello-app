from socketserver import StreamRequestHandler
from static_responder import StaticResponder
from request import Request
from response import Response

class MyTCPHandler(StreamRequestHandler):
    def handle(self):
        request = Request(self.rfile)
        print(f'method: {request.method}')
        print(f'uri: {request.uri}')
        print(f'protocol: {request.protocol}')
        print(f'headers: {request.headers}')

        if request.uri == '/' and request.method == 'GET':
            request.uri = '/index.html'
        elif request.uri == '/one' and request.method == 'GET':
            request.uri = '/first_page.html'
        elif request.uri == '/two' and request.method == 'GET':
            request.uri = '/second_page.html'
        elif request.uri == '/three' and request.method == 'GET':
            request.uri = '/third_page.html'

        response = Response(self.wfile)
        response.add_header('Connection', 'close')
        static_responder = StaticResponder(
            request,
            response,
            'static'
        )
        print(static_responder.file)
        if static_responder.file:
            static_responder.prepare_response()
        else:
            response.set_body('<h1>File Not Found</h1>')
            response.set_status(Response.HTTP_NOT_FOUND)
            response.add_header('Content-Type', 'text/html')

        response.send_response()