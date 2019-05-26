from lib.app import routes

import views.view


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain; charset=utf-8')])
    return [b'hello, world']


def app(env, start_response):
    view = routes[env['PATH_INFO']]
    status, headers, body = view(env)
    start_response(status, headers)
    return [body]
