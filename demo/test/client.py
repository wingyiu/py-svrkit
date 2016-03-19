# -*- coding: utf-8 -*-
import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))

from svrkit.rpc.client import Client
from svrkit.client import SvrkitClient
from svrkit.protocol.json import JsonProto
from svrkit.protocol.msgpack import MsgpackProto

if __name__ == '__main__':
    client = Client('localhost', '8080', 'demo', MsgpackProto, MsgpackProto)
    ret = client.echo(words=b'\xF0\xFF')
    print(ret)

    client2 = SvrkitClient('')
    ret2, data = client2.svr(1)
    print(ret2)
    print(data)
