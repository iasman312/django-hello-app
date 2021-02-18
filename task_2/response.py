from os import fstat


class Response:
    HTTP_OK = 200
    HTTP_BAD_REQUEST = 400
    HTTP_NOT_FOUND = 404
    HTTP_INTERNAL_SERVER_ERROR = 500

    MESSAGES = {
        HTTP_OK: 'OK',
        HTTP_BAD_REQUEST: 'Bad Request',
        HTTP_NOT_FOUND: 'Not Found',
        HTTP_INTERNAL_SERVER_ERROR: 'Internal Server Error'
    }
    PROTOCOL = 'HTTP/1.1'

    def __init__(self, strem):
        self._strem = strem

        self._status = '200 OK'
        self._headers = {}
        self._body = None
        self._file_body = None

    
    def set_body(self, body):
        self._body = body.encode()
        self.add_header('Content-Length', len(self._body))
    
    def set_file_body(self, file):
        self._file_body = file
        file_size = fstat(file.fileno()).st_size
        self.add_header('Content-Length', file_size)

    def set_status(self, status_code):
        self._status = f'{status_code} {self.MESSAGES[status_code]}'

    def add_header(self, name, value):
        self._headers[name] = value
    
    def _get_response_head(self):
        response = f'{self.PROTOCOL} {self._status}\r\n'

        header_lines = []
        for name, value in self._headers.items():
            header_lines.append(f'{name}: {value}')
        
        response += '\r\n'.join(header_lines)
        response += '\r\n\r\n'

        return response.encode()
    
    def _get_file_response(self):
        while True:
            data  = self._file_body.read(1024)
            if not data:
                break
            self._strem.write(data)

    def send_response(self):
        response_head = self._get_response_head()
        self._strem.write(response_head)

        if self._body:
            self._strem.write(self._body)
        elif self._file_body:
            self._get_file_response()