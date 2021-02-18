class Request:
    def __init__(self, stream):
        self._stream = stream

        self.headers = {}
        self.body = None
        self.method = None
        self.uri = None
        self.protocol = None

        self._parse_request_line()
        self._parse_headers()
        self._parse_body()
    
    def _parse_request_line(self):
        request_line = self.__readline()
        method, uri, protocol = request_line.split(' ')

        self.method = method
        self.uri = uri

        if protocol != 'HTTP/1.1':
            raise ValueError(f'Wrong protocol: {protocol}')

        self.protocol = protocol
    
    def _parse_headers(self):
        while True:
            raw_header = self.__readline()
            if not raw_header:
                break
            
            header_name, header_value = raw_header.split(': ')
            self.headers[header_name] = header_value
    
    def _parse_body(self):
        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            self.body = self._stream.read(content_length)

    def __readline(self):
        return self._stream.readline().strip().decode()