# -*- coding: utf-8 -*-
import json
import datetime
import decimal
import uuid

from svrkit.protocol.tz_util import utc
from svrkit.protocol.base import Proto
from svrkit.protocol.exception import ProtoDecodeException, ProtoEncodeException

class ComplexEncoder(json.JSONEncoder):

    def default(self, obj):
        if hasattr(obj, 'items'):  # kw
            return dict(((k, self.default(v)) for k, v in iter(obj)))
        elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):  # iterable but not str or bytes
            return list((self.default(v) for v in obj))
        elif isinstance(obj, datetime.datetime):
            return {'__datetime__': obj.strftime('%Y-%m-%d %H:%M:%S.%f%z')}
        elif isinstance(obj, datetime.date):
            return {'__date__': obj.strftime('%Y-%m-%d')}
        elif isinstance(obj, decimal.Decimal):
            return {'__decimal__': str(obj)}
        elif isinstance(obj, uuid.UUID):
            return {"__uuid__": obj.hex}
        else:
            return json.JSONEncoder.default(self, obj)


def object_hook(dct):
    if '__date__' in dct:
        date = datetime.datetime.strptime(dct["__date__"], '%Y-%m-%d').date()
        return date
    elif '__datetime__' in dct:
        dtm = dct["__datetime__"]
        unaware = datetime.datetime.strptime(dtm[:26], "%Y-%m-%d %H:%M:%S.%f")
        offset = dtm[26:]
        if not offset:
            return unaware
        else:
            aware = unaware.replace(tzinfo=utc)
            if offset == 'Z':
                return aware

            if len(offset) == 5:
                # Offset  in format (+|-)HHMM
                secs = (int(offset[1:3]) * 3600 + int(offset[3:]) * 60)
            elif ':' in offset and len(offset) == 6:
                # RFC-3339 format (+|-)HH:MM
                hours, minutes = offset[1:].split(':')
                secs = (int(hours) * 3600 + int(minutes) * 60)
            else:
                # Not RFC-3339 compliant
                raise ValueError("invalid format for offset")
            if offset[0] == "-":
                secs *= -1
            # work for py 3.2+
            return aware.replace(tzinfo=datetime.timezone(datetime.timedelta(seconds=secs)))
    elif '__decimal__' in dct:
        return decimal.Decimal(dct["__decimal__"])
    elif "__uuid__" in dct:
        return uuid.UUID(dct["__uuid__"])
    return dct


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
            data = json.loads(json_str, object_hook=object_hook)
        except:
            raise ProtoDecodeException()
        return data
