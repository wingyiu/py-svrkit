# -*- coding: utf-8 -*-
import logging
import configparser
from svrkit.rpc.service import Service
from svrkit.protocol.msgpack import MsgpackProto
from svrkit.protocol.json import JsonProto
from svrkit.rpc.exception import RpcUnsupportedProto

logger = logging.getLogger('svrkit')


class SvrkitService(Service):
    def __init__(self, config_path):
        # read configuration from ini file
        self.config_path = config_path
        self.parser = configparser.ConfigParser()
        self.parser.read(config_path)
        # only parse svrkit related configs
        svrkit_configs = self._parse_svrkit_configs(self.parser)
        super().__init__(prefix=svrkit_configs['service']['prefix'],
                         req_proto=svrkit_configs['proto']['req'],
                         resp_proto=svrkit_configs['proto']['resp'])

    def _parse_svrkit_configs(self, parser):
        configs = {}
        if 'service' in parser:
            configs['service'] = {}
            configs['service']['name'] = parser['service']['name']
            configs['service']['prefix'] = parser['service']['prefix']
        if 'proto' in parser:
            configs['proto'] = {}
            try:
                configs['proto']['req'] = globals()[parser['proto']['req']]
                configs['proto']['resp'] = globals()[parser['proto']['resp']]
            except KeyError:
                raise RpcUnsupportedProto()
        return configs
