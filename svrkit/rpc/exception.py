# -*- coding: utf-8 -*-


class SvrkitParamsError(Exception):
    """
    传入参数与方法要求参数不符
    """
    pass


class SvrkitUnsupportedService(Exception):
    """
    服务不存在
    """
    pass


class SvrkitUnsupportedMethod(Exception):
    """
    方法不存在
    """
    pass


class SvrkitCallError(Exception):
    """
    调用远端时发生异常,如超时等
    """
    pass


class SvrkitRemoteError(Exception):
    """
    远端服务异常 500
    """
    pass


class SvrkitReturnFormatError(Exception):
    """
    远端返回数据格式错误
    """
    pass


class SvrkitReturnError(Exception):
    """
    远端返回非具体错误
    """
    pass


class SvrkitUnsupportedProto(Exception):
    """
    不支持的protocol
    """
    pass


class SvrkitRemoteUnsupportedProto(Exception):
    """
    远端服务不支持该protocol,即远端无法解析请求数据
    """
    pass


class SvrkitClientUnsupportedProto(Exception):
    """
    客户端不支持该protocol,即客户端无法解析响应数据
    """
    pass
