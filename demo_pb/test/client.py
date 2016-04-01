# -*- coding: utf-8 -*-
import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))

from svrkit.rpc.client import Client
from svrkit.protocol.protobuf import BufProtoV1
from demo_pb import addressbook_pb2

if __name__ == '__main__':

    person = addressbook_pb2.Person()
    person.name = 'hello'
    person.id = 1
    person.email = 'word@hello.com'

    client = Client('localhost', '8082', 'demopb', BufProtoV1, BufProtoV1)
    ret = client.echo(person)
    print(ret)
    person_ret = addressbook_pb2.Person()
    person_ret.ParseFromString(ret)
    print(person_ret)

