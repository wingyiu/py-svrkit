# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger('svrkit.server')

class WsgiApplication(object):
    """

    """

    def __init__(self, application):
        super().__init__()
        self.application = application

    def __call__(self, environ, start_response):
        # get the request serivce and the method
        request_path_info = environ.get('PATH_INFO', None)
        logger.info('request path: %s', request_path_info)
        _, service_prefix, method = request_path_info.split('/')
        # get the request data
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        logger.debug('request body: %s', request_body)

        # invoke the method and get return
        response_body = self.application.handle_call(service_prefix, method, request_body)
        response_body_len = str(len(response_body))
        logger.debug('response data: %s', response_body)
        logger.debug('response data length: %s', response_body_len)

        headers = [('Content-Type', 'application/octet-stream'),
                   ('Content-Length', response_body_len),
                   ('Cache-Control', 'no-cache, no-store, must-revalidate'),
                   ('Pragma', 'no-cache')]
        status = '200 OK'
        start_response(status, headers)

        return [response_body,]
