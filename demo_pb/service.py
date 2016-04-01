# -*- coding: utf-8 -*-


from svrkit.service import Service

from demo_pb import addressbook_pb2

class DemoPbService(Service):

    def echo(self, req):
        person = addressbook_pb2.Person()
        person.ParseFromString(req)
        print(person)
        return person