# -*- coding: utf-8 -*-
import msgpack
import datetime
import decimal
from svrkit.protocol.base import Proto
from svrkit.protocol.exception import ProtoDecodeException, ProtoEncodeException


def decode_hook(obj):
    print(obj)
    if '__datetime__' in obj:
        obj = datetime.datetime.strptime(obj['as_str'].decode(), "%Y%m%dT%H:%M:%S.%f")
    return obj


def encode_default(obj):
    if isinstance(obj, datetime.datetime):
        obj = {'__datetime__': True, 'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f").encode()}
    return obj


class MsgpackProto(Proto):
    """
    msgpack protocol
    """

    def __init__(self):
        super().__init__()

    def encode(self, data):
        try:
            # TODO support complex like datetime
            binary = msgpack.packb(data, use_bin_type=True, default=encode_default)
        except:
            raise ProtoEncodeException()
        return binary

    def decode(self, binary):
        try:
            # TODO support complex like datetime
            data = msgpack.unpackb(binary, encoding='utf-8', use_list=False, object_hook=decode_hook)
        except:
            raise ProtoDecodeException()
        return data
