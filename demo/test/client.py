# -*- coding: utf-8 -*-
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
    import datetime
    ret = client.echo(words= datetime.datetime.now())
    print(ret)

    # svrkit client which requires a seq_id.
    client2 = SvrkitClient('client.ini')
    ret2, data = client2.svr(seq_id=3)
    print(ret2)
    print(data)
