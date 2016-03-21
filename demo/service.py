# -*- coding: utf-8 -*-

from svrkit.rpc.service import Service

class DemoService(Service):
    def __init__(self, prefix, req_proto, resp_proto):
        super().__init__(prefix, req_proto, resp_proto)

    def echo(self, words):
        return words

    def svr(self, seq_id):
        print(seq_id)
        return 0, 'yes!'