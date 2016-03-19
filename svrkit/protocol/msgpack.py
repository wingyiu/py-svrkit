# -*- coding: utf-8 -*-
import msgpack
import datetime
import decimal
from svrkit.protocol.base import Proto
from svrkit.protocol.exception import ProtoDecodeException, ProtoEncodeException


class MsgpackProto(Proto):
    """
    msgpack protocol
    """
    def __init__(self):
        super().__init__()

    def encode(self, data):
        try:
            # TODO support complex like datetime
            binary = msgpack.packb(data, use_bin_type=True)
        except:
            raise ProtoEncodeException()
        return binary

    def decode(self, binary):
        try:
            # TODO support complex like datetime
            data = msgpack.unpackb(binary, encoding='utf-8', use_list=False)
        except:
            raise ProtoDecodeException()
        return data