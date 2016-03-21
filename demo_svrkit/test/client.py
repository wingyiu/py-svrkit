# -*- coding: utf-8 -*-
import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))

from svrkit.client import SvrkitClient

if __name__ == '__main__':

    client = SvrkitClient('client.ini')
    ret, data = client.echo(seq_id=3, words='ping pong is good')
    print(ret)
    print(data)
