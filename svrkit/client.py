# -*- coding: utf-8 -*-
import logging

from svrkit.rpc.client import Client
from svrkit.protocol.msgpack import MsgpackProto
logger = logging.getLogger('svrkit')

class SvrkitClient(Client):
    """

    """

    def __init__(self, config_path):
        # TODO read host \service\in protocol\ out protocol from configure file
        # read configure file
        # load configurations
        configs = {'servers': [{'host': 'localhost', 'port': '8080'}],
                   'service': 'demo',
                   'in_proto': 'json',
                   'out_proto': 'json'}
        self.servers = configs['servers']
        #
        super().__init__(host=self.servers[0]['host'], port=self.servers[0]['port'], service=configs['service'],
                         req_proto=MsgpackProto,
                         resp_proto=MsgpackProto)

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
        #
        url = self._build_req_url(selected_server['host'], selected_server['port'], self.service, method)
        return url
