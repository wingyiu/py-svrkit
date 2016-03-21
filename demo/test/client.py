# -*- coding: utf-8 -*-
import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))

from svrkit.rpc.client import Client
from svrkit.protocol.msgpack import MsgpackProto

if __name__ == '__main__':
    client = Client('localhost', '8080', 'demo', MsgpackProto, MsgpackProto)
    import datetime
    ret = client.echo(words= datetime.datetime.now())
    print(ret)

