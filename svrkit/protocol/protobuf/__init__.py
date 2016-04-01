# -*- coding: utf-8 -*-

from svrkit.protocol.base import Proto
from svrkit.protocol.exception import ProtoEncodeException, ProtoDecodeException
from svrkit.protocol.protobuf import wrapper_pb2
from svrkit.protocol.protobuf import wrapper_v1_pb2


class BufProtoV1(Proto):
    def encode(self, data, is_req=False):
        try:
            if is_req:
                wrapper = wrapper_v1_pb2.RequestWrapper()
                # 取第一个arg或者第一个kwarg
                if len(data['args']) == 1:
                    wrapper.request = data['args'][0].SerializeToString()
                elif len(data['kwargs']) == 1:
                    wrapper.request = data['kwargs'].items[0][1].SerializeToString()
                else:
                    raise ProtoEncodeException('BufProtoV1 support 1 arg or 1 kwarg')

                binary = wrapper.SerializeToString()
                return binary
            else:
                wrapper = wrapper_v1_pb2.ResponseWrapper()
                wrapper.RET = data['RET']
                if data['DATA'] is not None:
                    wrapper.DATA = data['DATA'].SerializeToString()
                binary = wrapper.SerializeToString()
                return binary
        except:
            raise ProtoEncodeException()

    def decode(self, binary, is_req=False):
        try:
            if is_req:
                data = {'args': [], 'kwargs': {}}
                wrapper = wrapper_v1_pb2.RequestWrapper.FromString(binary)
                data['args'].append(wrapper.request)
                return data
            else:
                data = {}
                wrapper = wrapper_v1_pb2.ResponseWrapper.FromString(binary)
                data['RET'] = wrapper.RET
                data['DATA'] = wrapper.DATA
                return data
        except:
            raise ProtoDecodeException()


class BufProtoV2(Proto):
    def encode(self, data, is_req=False):
        try:
            if is_req:
                wrapper = wrapper_pb2.RequestWrapper()
                wrapper.args.extend(data['args'])
                for k, v in data['kwargs'].items():
                    wrapper.kwargs[k] = v
                binary = wrapper.SerializeToString()
                return binary
            else:
                wrapper = wrapper_pb2.ResponseWrapper()
                wrapper.RET = data['RET']
                wrapper.DATA.CopyFrom(data['DATA'])
                binary = wrapper.SerializeToString()
                return binary
        except:
            raise ProtoEncodeException()

    def decode(self, binary, is_req=False):
        try:
            if is_req:
                data = {'args': [], 'kwargs': {}}
                wrapper = wrapper_pb2.RequestWrapper.FromString(binary)
                for b in wrapper.args:
                    data['args'].append(b)
                for k in wrapper.kwargs:
                    data['kwargs']['k'] = wrapper.kwargs[k]
                return data
            else:
                data = {}
                wrapper = wrapper_pb2.ResponseWrapper.FromString(binary)
                data['RET'] = wrapper.RET
                data['DATA'] = wrapper.DATA
                return data
        except:
            raise ProtoDecodeException()


BufProto = BufProtoV1
