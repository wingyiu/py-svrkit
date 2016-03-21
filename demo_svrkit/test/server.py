# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))
import logging

logging.basicConfig(level=logging.DEBUG)

from svrkit.server.wsgi import WsgiApplication
from demo_svrkit.service import DemoSvrkitService


service = DemoSvrkitService('service.ini')

if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(service)
    server = make_server('0.0.0.0', 8081, wsgi_app)
    server.serve_forever()
