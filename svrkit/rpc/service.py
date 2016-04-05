# -*- coding: utf-8 -*-
import logging
import inspect
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

        # 判断该method是否带有rpc decorator,没有rpc的方法不是可调用的
        method = getattr(self, method_name, None)
        if method is None or not callable(method) or not getattr(method, 'is_rpc', False):  # or not has decorator rpc
            return self._encode_output(RET_UNSUPPORTED_METHOD, None)

        # 利用function annotations做参数类型判断或者参数转换,而不用decorator
        sig = inspect.signature(method)
        parameters = sig.parameters  # 参数有序字典
        arg_names = tuple(parameters.keys())  # 参数名称

        # 尝试转换(如果已经是相同类型,则不转换)
        try:
            args_conv = []
            for i, value in enumerate(args):
                arg_name = arg_names[i]
                anno = parameters[arg_name].annotation
                if anno and not isinstance(value, anno):
                        args_conv.append(anno(value))
                else:
                    args_conv.append(value)

            kwargs_conv = {}
            for arg_name, value in kwargs.items():
                anno = parameters[arg_name].annotation
                if anno and not isinstance(value, anno):
                    kwargs_conv[arg_name] = anno(value)
                else:
                    kwargs_conv[arg_name] = value
        except ValueError as e:
            logger.exception(e)
            return self._encode_output(RET_PARAMS_ERROR, None)
        except TypeError as e:
            logger.exception(e)
            return self._encode_output(RET_PARAMS_ERROR, None)
        except:
            return self._encode_output(RET_ERROR, None)

        try:
            # 调用服务的方法
            result = method(*args_conv, **kwargs_conv)  # bounded method, no need to pass self
            return self._encode_output(RET_OK, result)
        except TypeError as e:
            logger.exception(e)
            return self._encode_output(RET_PARAMS_ERROR, None)
        except:
            logger.error('call except')
            return self._encode_output(RET_ERROR, None)
