from typing import List, Tuple, Any
from mimetypes import guess_type
import os

from lib.app import route


@route('/hello')
def hello(request: dict) -> Tuple[str, List[tuple], bytes]:
    body = b'''
    <html><body>
        <h1>hello, world.</h1>
    </body></html>
    '''
    return '200 OK', [], body


@route('/static/')
def file_view(request: dict) -> Tuple[str, list, bytes]:
    path: str = request['PATH_INFO'].lstrip('/')
    if not os.path.isfile(path):
        return not_found_view(request)
    ct = guess_type(path)
    if ct is None:
        ct = 'application/octet-stream'
    headers = [
        ('Content-Type', ct),
    ]
    return '200 OK', headers, open(path, 'rb').read()


@route('/')
def not_found_view(request: dict) -> Tuple[str, List[tuple], bytes]:
    return '404 Not Found', [], b'404 not found'
