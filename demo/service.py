# -*- coding: utf-8 -*-

from svrkit.rpc.service import Service
from svrkit.rpc.decorator import rpc

class DemoService(Service):
    @rpc
    def echo(self, words:str, times:int):
        print(words)
        print(times)
        return words


