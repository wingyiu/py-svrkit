# -*- coding: utf-8 -*-
import logging
import configparser

from svrkit.rpc.client import Client
from svrkit.protocol.msgpack import MsgpackProto
from svrkit.protocol.json import JsonProto
from svrkit.rpc.exception import RpcUnsupportedProto
from svrkit.exception import SvrkitSeqIdMissingException

logger = logging.getLogger('svrkit')

class SvrkitClient(Client):
    """
    a client that use the `seq_id` in `kwargs` to select the target server
    """

    def __init__(self, config_path):
        # read configuration from ini file
        self.config_path = config_path
        self.parser = configparser.ConfigParser()
        self.parser.read(config_path)
        # only parse svrkit related configs
        svrkit_configs = self._parse_svrkit_configs(self.parser)
        self.servers = svrkit_configs['servers']
        #
        super().__init__(host=self.servers[0]['host'], port=self.servers[0]['port'], service=svrkit_configs['service']['prefix'],
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
            req_p = parser['proto']['req']
            try:
                configs['proto']['req'] = globals()[parser['proto']['req']]
                configs['proto']['resp'] = globals()[parser['proto']['resp']]
            except KeyError:
                raise RpcUnsupportedProto()
        if 'servers' in parser:
            configs['servers'] = []
            section_keys = parser['servers']['keys'].split(', ')
            for sk in section_keys:
                s = {}
                s['host'] = parser[sk]['host']
                s['port'] = parser[sk]['port']
                configs['servers'].append(s)
        return configs

    def _get_server(self, service, method, *args, **kwargs):
        # seq_id
        seq_id = kwargs.get('seq_id', None)
        if seq_id is None:
            raise SvrkitSeqIdMissingException()
        logger.debug('seq_id: %s', seq_id)
        server_count = len(self.servers)
        idx = abs(hash(seq_id)) % server_count
        selected_server = self.servers[idx]
        logger.debug('selected server: [%d] %s:%s', idx, selected_server['host'], selected_server['port'])
        return selected_server['host'], selected_server['port']

