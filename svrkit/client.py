# -*- coding: utf-8 -*-
import logging
import configparser

from svrkit.rpc.client import Client
from svrkit.protocol.msgpack import MsgpackProto
from svrkit.protocol.json import JsonProto
from svrkit.rpc.exception import SvrkitUnsupportedProto

logger = logging.getLogger('svrkit')

class SvrkitClient(Client):
    """
    a client that use the `seq_id` to select the target server
    """

    def __init__(self, config_path):
        # read configuration from ini file
        self.config_path = config_path
        configs = self._parse_configs(config_path)
        logger.debug('client configs: %s', configs)
        self.servers = configs['servers']
        #
        super().__init__(host=self.servers[0]['host'], port=self.servers[0]['port'], service=configs['service']['prefix'],
                         req_proto=configs['proto']['req'],
                         resp_proto=configs['proto']['resp'])

    def _parse_configs(self, config_path):
        parser = configparser.ConfigParser()
        parser.read(config_path)
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
                raise SvrkitUnsupportedProto()
        if 'servers' in parser:
            configs['servers'] = []
            section_keys = parser['servers']['keys'].split(', ')
            print(section_keys)
            for sk in section_keys:
                s = {}
                s['host'] = parser[sk]['host']
                s['port'] = parser[sk]['port']
                configs['servers'].append(s)
        return configs

    def _get_req_url(self, method, *args, **kwargs):
        # seq_id
        seq_id = kwargs.get('seq_id', None)
        if not seq_id:
            seq_id = args[0]
        # TODO 如果seq_id不存在,抛出一个异常
        logger.debug('seq_id: %s', seq_id)
        server_count = len(self.servers)
        idx = abs(hash(seq_id)) % server_count
        selected_server = self.servers[idx]
        logger.debug('selected server: [%d] %s:%s', idx, selected_server['host'], selected_server['port'])
        #
        url = self._build_req_url(selected_server['host'], selected_server['port'], self.service, method)
        return url
