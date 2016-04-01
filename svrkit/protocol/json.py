# -*- coding: utf-8 -*-
import json
import datetime
import decimal
from svrkit.protocol.base import Proto
from svrkit.protocol.exception import ProtoDecodeException, ProtoEncodeException


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class JsonProto(Proto):
    def __init__(self):
        super().__init__()

    def encode(self, data, is_req=False):
        try:
            json_str = json.dumps(data, cls=ComplexEncoder)
            binary = json_str.encode('utf-8')
        except:
            raise ProtoEncodeException()
        return binary

    def decode(self, binary, is_req=False):
        try:
            json_str = binary.decode('utf-8')
            data = json.loads(json_str)
        except:
            raise ProtoDecodeException()
        return data
