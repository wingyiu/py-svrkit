# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))
import logging
logging.basicConfig(level=logging.DEBUG)

from svrkit.rpc.application import Application
from svrkit.protocol.http import UrlEncodedForm
from svrkit.protocol.json import JsonProto
from svrkit.protocol.msgpack import MsgpackProto
from svrkit.server.wsgi import WsgiApplication
from demo.service import DemoService

application = Application(DemoService,
                          req_proto=MsgpackProto,
                          resp_proto=MsgpackProto,
                          config={}
                          )

if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(application)
    # read configure from
    server = make_server('0.0.0.0', 8080, wsgi_app)
    server.serve_forever()
