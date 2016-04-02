# -*- coding: utf-8 -*-
import functools


def rpc(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        return method(self, *args, **kwargs)
    wrapper.is_rpc = True

    return wrapper

