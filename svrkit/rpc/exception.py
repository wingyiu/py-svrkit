# -*- coding: utf-8 -*-


class RpcParamsError(Exception):
    """
    传入参数与方法要求参数不符
    """
    pass


class RpcUnsupportedService(Exception):
    """
    服务不存在
    """
    pass


class RpcUnsupportedMethod(Exception):
    """
    方法不存在
    """
    pass


class RpcCallError(Exception):
    """
    调用远端时发生异常,如超时等
    """
    pass


class RpcServerError(Exception):
    """
    远端服务异常 500
    """
    pass


class RpcReturnFormatError(Exception):
    """
    远端返回数据格式错误
    """
    pass


class RpcReturnError(Exception):
    """
    远端返回非具体错误
    """
    pass


class RpcUnsupportedProto(Exception):
    """
    不支持的protocol
    """
    pass


class RpcServerUnsupportedProto(Exception):
    """
    远端服务不支持该protocol,即远端无法解析请求数据
    """
    pass


class RpcClientUnsupportedProto(Exception):
    """
    客户端不支持该protocol,即客户端无法解析响应数据
    """
    pass
