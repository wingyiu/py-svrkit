# -*- coding: utf-8 -*-
import logging
from svrkit.protocol.json import JsonProto
from svrkit.protocol.exception import ProtoDecodeException
from svrkit.rpc.define import *

logger = logging.getLogger('svrkit')


class Service(object):
    """

    """

    def __init__(self, prefix, req_proto, resp_proto):
        #
        self.prefix = prefix
        self.req_proto = req_proto
        self.resp_proto = resp_proto

    def _decode_input(self, input):
        logger.debug('decoding input: %s', input)
        proto = self.req_proto if self.req_proto else JsonProto
        data = proto().decode(input, is_req=True)
        logger.debug('decoded input: %s', data)
        return data

    def _encode_output(self, ret, result=None):
        output = {'RET': ret, 'DATA': result}
        logger.debug('encoding ret and result: %s', output)
        proto = self.req_proto if self.req_proto else JsonProto
        resp = proto().encode(output, is_req=False)
        logger.debug('encoded ret and result: %s', resp)
        return resp

    def handle_call(self, service_prefix, method_name, input):
        """

        :param service_prefix:
        :param method_name:
        :param input:
        :return:
        """
        logger.info('handle rpc call: %s, %s', service_prefix, method_name)
        if service_prefix != self.prefix:
            return self._encode_output(RET_UNSUPPORTED_SERVICE, None)

        # decode input (in_protocol)
        try:
            params = self._decode_input(input)
        except ProtoDecodeException:
            return self._encode_output(RET_UNSUPPORTED_PROTO, None)

        # convert params to *args and **kwargs
        args = params['args']
        kwargs = params['kwargs']

        # TODO 判断该method是否带有rpc decorator
        # TODO 利用function anotations做参数类型判断或者参数转换,而不用decorator
        method = getattr(self, method_name, None)
        if method is None or not callable(method):  # or not has decorator rpc
            return self._encode_output(RET_UNSUPPORTED_METHOD, None)

        try:
            # call method of service
            result = method(*args, **kwargs)  #bounded method, no need to pass self
            return self._encode_output(RET_OK, result)
        except TypeError:
            return self._encode_output(RET_PARAMS_ERROR, None)
        except:
            return self._encode_output(RET_ERROR, None)
