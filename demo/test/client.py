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

if __name__ == '__main__':
    client = Client('localhost', '8080', 'demo', JsonProto, JsonProto)
    import datetime
    ret = client.echo(dt= datetime.date.today(), times=Decimal('0.000001'))
    print(ret)

