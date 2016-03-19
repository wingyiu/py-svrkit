# -*- coding: utf-8 -*-

class Proto(object):
    def __init__(self):
        pass

    def encode(self, data):
        raise NotImplementedError

    def decode(self, binary):
        raise NotImplementedError


