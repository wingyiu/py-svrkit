# -*- coding: utf-8 -*-
import logging
from svrkit.protocol.json import JsonProto
from svrkit.protocol.exception import ProtoDecodeException
from svrkit.rpc.define import *
logger = logging.getLogger('svrkit')

class Application(object):
    """

    """

    def __init__(self, services, req_proto, resp_proto):
        # support multiple services in one application
        self.services = dict(services)
        # self.service = service
        # self.prefix = prefix
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

    def _get_service(self, service_prefix):
        return self.services.get(service_prefix, None)

    def handle_call(self, service_prefix, method, input):
        """

        :param service_prefix:
        :param method:
        :param input:
        :return:
        """
        logger.info('handle rpc call: %s, %s', service_prefix, method)
        # decode input (in_protocol)
        try:
            params = self._decode_input(input)
        except ProtoDecodeException:
            return self._encode_output(RET_UNSUPPORTED_PROTO, None)

        # convert params to *args and **kwargs
        args = params['args']
        kwargs = params['kwargs']

        #
        service = self._get_service(service_prefix)
        if service is None:
            return self._encode_output(RET_UNSUPPORTED_SERVICE, None)

        try:
            to_call = service.__dict__[method]
        except KeyError:
            return self._encode_output(RET_UNSUPPORTED_METHOD, None)
        except:
            return self._encode_output(RET_ERROR, None)

        try:
            # call method of service
            inst = service()
            result = to_call(inst, *args, **kwargs)
            return self._encode_output(RET_OK, result)
        except TypeError:
            return self._encode_output(RET_PARAMS_ERROR, None)
        except:
            return self._encode_output(RET_ERROR, None)
