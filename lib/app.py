routes = {}


def route(path):
    def _route(handler):
        routes[path] = handler
    return _route
