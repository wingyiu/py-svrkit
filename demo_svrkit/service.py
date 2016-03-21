# -*- coding: utf-8 -*-


from svrkit.service import SvrkitService


class DemoSvrkitService(SvrkitService):
    def echo(self, seq_id, words):
        return seq_id, words
