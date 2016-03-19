# -*- coding: utf-8 -*-
import logging
import urllib.request
import urllib.error
from svrkit.rpc.exception import *
from svrkit.rpc.define import *
from svrkit.protocol.json import JsonProto

logger = logging.getLogger('svrkit.client')


class Client(object):
    """
    rpc client
    """

    def __init__(self, host, port, service, req_proto, resp_proto):
        self.host = host
        self.service = service
        self.port = port
        self.req_proto = req_proto
        self.resp_proto = resp_proto

    def _encode_req(self, *args, **kwargs):
        """
        use the req_protocol to encode the params to bytes
        :param args:
        :param kwargs:
        :return:
        """
        #
        req = {'*args': args, '**kwargs': kwargs}
        # if no req_proto is suppled, default use json proto
        proto = self.req_proto if self.req_proto else JsonProto
        # encode to bytes
        logger.debug('encoding args: %s', req)
        x = proto().encode(req)
        logger.debug('encoded args: %s', x)
        return x

    def _decode_resp(self, resp_data):
        '''
        use the resp protocol to decode the response data to return
        :param resp_data:
        :return:
        '''
        # if no req_proto is suppled, default use json proto
        proto = self.req_proto if self.req_proto else JsonProto
        # decode bytes
        logger.debug('decoding resp: %s', resp_data)
        resp = proto().decode(resp_data)
        logger.debug('decoded resp: %s', resp)
        try:
            ret = resp.get('RET')
            result = resp.get('DATA')
        except:
            raise SvrkitReturnFormatError()

        return ret, result

    def _build_req_url(self, host, port, service, method):
        url = 'http://{}:{}/{}/{}'.format(host, port, service, method)
        return url

    def _get_req_url(self, method, *args, **kwargs):
        url = self._build_req_url(self.host, self.port, self.service, method)
        return url

    def _remote_call(self, method, *args, **kwargs):
        # 在这连接service,序列化参数,请求,反序列化响应数据,并return
        req_data = self._encode_req(*args, **kwargs)
        data_len = len(req_data)

        url = self._get_req_url(method, *args, **kwargs)
        req = urllib.request.Request(url, req_data)
        req.add_header('Cache-Control', 'no-cache')
        req.add_header('Content-Length', '%d' % data_len)
        req.add_header('Content-Type', 'application/octet-stream')
        req.add_header('Content-transfer-encoding', 'binary')
        #
        try:
            resp = urllib.request.urlopen(req)
            resp_data = resp.read()
        except urllib.error.HTTPError as e:
            logger.error('remote call http error: %s', e.code)
            raise SvrkitRemoteError()
        except:
            logger.error('remote call fail')
            raise SvrkitCallError()
        #
        ret, data = self._decode_resp(resp_data)

        if ret == RET_METHOD_NOT_EXIST:
            raise SvrkitMethodNotExist()
        elif ret == RET_PARAMS_ERROR:
            raise SvrkitParamsError()
        elif ret == RET_ERROR:
            raise SvrkitReturnError

        return data

    def __call__(self, method, *args, **kwargs):
        ret = self._remote_call(method, *args, **kwargs)
        return ret

    def __getattr__(self, method):
        # 返回一个闭包,该闭包封装了self和method.
        # 当这个闭包被执行时,即x(*args, **kwargs),
        # 即self(method, *args, **kargs)被运行,
        # 即self.__call__(self, method, *args, **kwargs)
        f = lambda *args, **kwargs: self(method, *args, **kwargs)
        return f


class JsonClient(Client):
    """
    client that use json as req and resp protocol
    """

    def __init__(self, host, port, service):
        super().__init__(host, port, service, JsonProto, JsonProto)


class AsyncClient(object):
    pass
