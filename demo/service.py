# -*- coding: utf-8 -*-

from svrkit.rpc.service import Service


class DemoService(Service):
    def echo(self, words):
        return words


