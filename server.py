import socket
from typing import Dict, Any, Union, List

from views.view import routes


def dispatch(request):
    path_info: str = request['PATH_INFO']
    for path, view in routes.items():
        if path_info.startswith(path):
            return view


def app(raw_request):
    request = make_request(raw_request)
    view = dispatch(request)
    return make_response(*view(request))


def make_request(raw_request: str) -> Dict[str, Any]:
    if isinstance(raw_request, bytes):
        raw_request = raw_request.decode('utf-8')
    header, body = raw_request.split('\r\n\r\n', 1)
    headers = header.splitlines()
    method, path, proto = headers[0].split(' ', 2)
    request = {
        'headers': headers[0],
        'body': body,
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'SERVER_PROTOCOL': proto,
    }
    print(request)
    return request


def make_response(status: str, headers: list, body: bytes):
    status_line = ('HTTP/1.1 %s' % status).encode('utf-8')
    hl = []
    for k, v in headers:
        h = '%s: %s' % (k, v)
        hl.append(h)
    header = ('\r\n'.join(hl)).encode('utf-8')
    raw_resonse = status_line + b'\r\n' + header + b'\r\n\r\n' + body
    return raw_resonse


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 1234))
        s.listen()
        while True:
            conn, _ = s.accept()
            with conn:
                data = b''
                while True:
                    chunk = conn.recv(4096)
                    data += chunk
                    if len(chunk) < 4096:
                        break
                conn.sendall(app(data))


if __name__ == '__main__':
    main()
