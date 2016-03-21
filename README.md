# py-svrkit
just another square wheel

## what is this wheel?
1.a `rpc` based on `HTTP`

2.a `svrkit` based on the `rpc` mentioned in `1.`

## what is svrkit?
something used in `Wechat`, which use an `seq_id` to selected server(`Load Balancing`) in the client side.

## how to use it?

###1. write some methods on the sever side, and run it with a wsgi server

````
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))
import logging
logging.basicConfig(level=logging.DEBUG)

from svrkit.protocol.json import JsonProto
from svrkit.protocol.msgpack import MsgpackProto
from svrkit.server.wsgi import WsgiApplication
from svrkit.rpc.service import Service

class DemoService(Service):
    def __init__(self, prefix, req_proto, resp_proto):
        super().__init__(prefix, req_proto, resp_proto)

    def echo(self, words):
        return words

    def svr(self, seq_id):
        print(seq_id)
        return 0, 'yes!'


service = DemoService('demo', req_proto=MsgpackProto, resp_proto=MsgpackProto)

if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(service)
    # read configure from
    server = make_server('0.0.0.0', 8080, wsgi_app)
    server.serve_forever()
````


###2. call these methods on client side like this

````
import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))

from svrkit.rpc.client import Client
from svrkit.client import SvrkitClient
from svrkit.protocol.msgpack import MsgpackProto

if __name__ == '__main__':
    # simple rpc client
    client = Client('localhost', '8080', 'demo', MsgpackProto, MsgpackProto)
    ret = client.echo(words=b'\xF0\xFF')
    print(ret)

    # svrkit client which requires a seq_id.
    client2 = SvrkitClient('client.ini')
    ret2, data = client2.svr(seq_id=0)
    print(ret2)
    print(data)
````

## else ?

This wheel is not completed yet. Inspired by [svrkit, zerorpc, spyne].