# -*- coding: utf-8 -*-
import logging
from svrkit.protocol.json import JsonProto
from svrkit.rpc.define import *
logger = logging.getLogger('svrkit')

class Application(object):
    """

    """
    def __init__(self, service, req_proto, resp_proto, config, **kwargs):
        self.service = service
        self.req_proto = req_proto
        self.resp_proto = resp_proto

    def _decode_input(self, input):
        logger.debug('decoding input: %s', input)
        proto = self.req_proto if self.req_proto else JsonProto
        data = proto().decode(input)
        logger.debug('decoded input: %s', data)
        return data

    def _encode_output(self, ret, result=None):
        output = {'RET': ret, 'DATA': result}
        logger.debug('encoding ret and result: %s',output)
        proto = self.req_proto if self.req_proto else JsonProto
        resp = proto().encode(output)
        logger.debug('encoded ret and result: %s', resp)
        return resp

    def handle_call(self, service_prefix, method, input):
        """

        :param service_prefix:
        :param method:
        :param input:
        :return:
        """
        logger.info('handle rpc call: %s, %s', service_prefix, method)
        # decode input (in_protocol)
        params = self._decode_input(input)

        # convert params to *args and **kwargs
        args = params['*args']
        kwargs = params['**kwargs']

        try:
            to_call = self.service.__dict__[method]
        except KeyError:
            return self._encode_output(RET_METHOD_NOT_EXIST, None)
        except:
            return self._encode_output(RET_ERROR, None)

        try:
            # call method of service
            result = to_call(self.service, *args, **kwargs)
            return self._encode_output(RET_OK, result)
        except TypeError:
            return self._encode_output(RET_PARAMS_ERROR, None)
        except:
            return self._encode_output(RET_ERROR, None)
