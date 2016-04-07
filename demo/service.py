# -*- coding: utf-8 -*-
from datetime import datetime, date

from svrkit.rpc.service import Service
from svrkit.rpc.decorator import rpc
from decimal import Decimal

class DemoService(Service):
    @rpc
    def echo(self, dt: date, times: bytearray, sss):
        print(dt)
        print(times)
        print(sss)
        return times
