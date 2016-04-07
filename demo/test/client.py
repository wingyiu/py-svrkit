# -*- coding: utf-8 -*-
import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))

from svrkit.rpc.client import Client
from svrkit.protocol.json import JsonProto
from svrkit.protocol.msgpack import MsgpackProto
from pytz import timezone
from decimal import Decimal
import datetime

class A(object):
    f = 1
    def __init__(self, a, b):
        self.aa = a
        self.ab = b

    def asdfasdf(self):
        pass

class B(A):
    def __init__(self, a, b):
        super().__init__('aa', 'bb')
        self.a = a
        self.b = b

    def asf(self):
        pass

if __name__ == '__main__':
    client = Client('localhost', '8080', 'demo', JsonProto, JsonProto)
    ao = B(1, '3')
    print(ao.__dict__)
    ret = client.echo(dt= datetime.date.today(), times=b'0.000001', sss=ao)
    print(ret)

