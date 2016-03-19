# -*- coding: utf-8 -*-


class SvrkitParamsError(Exception):
    """
    传入参数与方法要求参数不符
    """
    pass

class SvrkitMethodNotExist(Exception):
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