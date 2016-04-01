# -*- coding: utf-8 -*-

class Proto(object):
    def __init__(self):
        pass

    def encode(self, data, is_req=False):
        raise NotImplementedError

    def decode(self, binary, is_req=False):
        raise NotImplementedError


