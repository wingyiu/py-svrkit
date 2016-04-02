# py-svrkit
just another square wheel

## what is this wheel?
1.a `rpc` based on `HTTP`

2.a `svrkit` based on the `rpc` mentioned in `1.`

## what is svrkit?
something used in `Wechat`, which use an `seq_id` to selected server(`Load Balancing`) in the client side.

## rpc demo

###1. write some methods on the sever side, and run it with a wsgi server

````

from svrkit.protocol.msgpack import MsgpackProto
from svrkit.server.wsgi import WsgiApplication
from svrkit.rpc.service import Service
from svrkit.rpc.decorator import rpc

class DemoService(Service):
    @rpc
    def echo(self, words: str, times: int):
        print(words)
        print(times)
        return words

service = DemoService('demo', req_proto=MsgpackProto, resp_proto=MsgpackProto)

if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(service)
    server = make_server('0.0.0.0', 8080, wsgi_app)
    server.serve_forever()
````


###2. call these methods on client side like this

````

from svrkit.rpc.client import Client
from svrkit.protocol.msgpack import MsgpackProto

if __name__ == '__main__':
    client = Client('localhost', '8080', 'demo', MsgpackProto, MsgpackProto)
    import datetime
    ret = client.echo(words=datetime.datetime.now(), times='1000')
    print(ret)
````

## svrkit demo
### 1. server side

````

from svrkit.server.wsgi import WsgiApplication
from svrkit.rpc.decorator import rpc

class DemoSvrkitService(SvrkitService):
    @rpc
    def echo(self, seq_id, words):
        return seq_id, words

service = DemoSvrkitService('service.ini')

if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(service)
    server = make_server('0.0.0.0', 8081, wsgi_app)
    server.serve_forever()
````

### 2. client side

````

from svrkit.client import SvrkitClient

if __name__ == '__main__':

    client = SvrkitClient('client.ini')
    ret, data = client.echo(seq_id=3, words='ping pong is good')
    print(ret)
    print(data)

````

## else ?

This wheel is not completed yet. Inspired by [svrkit, zerorpc, spyne].