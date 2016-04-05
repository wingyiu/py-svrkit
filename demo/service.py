# -*- coding: utf-8 -*-
from datetime import datetime, date

from svrkit.rpc.service import Service
from svrkit.rpc.decorator import rpc
from decimal import Decimal

class DemoService(Service):
    @rpc
    def echo(self, dt: date, times: Decimal):
        print(dt)
        print(times)
        return times
