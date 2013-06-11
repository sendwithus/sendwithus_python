"""
Send With Us - Python Client
Copyright SendWithus 2013
"""
import logging
import requests
from json import dumps
import warnings

from encoder import swu_json_encode
from version import version

FORMAT = '%(asctime)-15s %(message)s'
logger = logging.getLogger('sendwithus')
logger.propagate = False

class api:
    API_PROTO = 'https'
    API_PORT = '443'
    API_HOST = 'beta.sendwithus.com'
    API_VERSION = '1_0'
    API_HEADER_KEY = 'X-SWU-API-KEY'
    API_HEADER_CLIENT = 'X-SWU-API-CLIENT'

    HTTP_GET = 'GET'
    HTTP_POST = 'POST'

    EMAILS_ENDPOINT = 'emails'
    SEND_ENDPOINT = 'send'

    API_CLIENT_LANG = 'python'
    API_CLIENT_VERSION = version
    API_KEY = 'THIS_IS_A_TEST_API_KEY'

    DEBUG = False

    JSON_ENCODE_DEFAULT = swu_json_encode

    def __init__(self, api_key=None, **kwargs):
        """Constructor, expects api key"""

        if not api_key:
            raise Exception("You must speicfy an api key")

        self.API_KEY = api_key
        
        if 'API_HOST' in kwargs:
            self.API_HOST = kwargs['API_HOST']
        if 'API_PROTO' in kwargs:
            self.API_PROTO = kwargs['API_PROTO']
        if 'API_PORT' in kwargs:
            self.API_PORT = kwargs['API_PORT']
        if 'API_VERSION' in kwargs:
            self.API_VERSION = kwargs['API_VERSION']
        if 'DEBUG' in kwargs:
            self.DEBUG = kwargs['DEBUG']
        if 'JSON_ENCODE_DEFAULT' in kwargs:
            self.JSON_ENCODE_DEFAULT = kwargs['JSON_ENCODE_DEFAULT']

        if self.DEBUG:
            logging.basicConfig(format=FORMAT, level=logging.DEBUG)
            logger.debug('Debug enabled')
            logger.propagate = True

    def _build_request_path(self, endpoint):
        path = "%s://%s:%s/api/v%s/%s" % (self.API_PROTO, self.API_HOST, 
                self.API_PORT, self.API_VERSION, endpoint)

        logger.debug('\tpath: %s' % path)

        return path

    def _api_request(self, endpoint, http_method, *args, **kwargs):
        """Private method for api requests"""
        logger.debug(' > Sending API request to endpoint: %s' % endpoint)

        client_header = '%s-%s' % (self.API_CLIENT_LANG, self.API_CLIENT_VERSION)

        headers = {
            self.API_HEADER_KEY: self.API_KEY,
            self.API_HEADER_CLIENT: client_header,
            'Content-type': 'application/json', 
            'Accept': 'text/plain'
        }

        if 'headers' in kwargs:
            headers.update(kwargs['headers'])

        logger.debug('\theaders: %s' % headers)

        data = None
        if 'payload' in kwargs:
            data = dumps(kwargs['payload'], default=self.JSON_ENCODE_DEFAULT)
        
        logger.debug('\tdata: %s' % data)

        path = self._build_request_path(endpoint)

        # do some error handling
        if (http_method == self.HTTP_POST):
            if (data):
                r = requests.post(path, data=data, headers=headers)
            else:
                r = requests.post(path, headers=headers)
        else:
            r = requests.get(path, headers=headers)

        logger.debug('\tresponse code:%s' % r.status_code)
        try:
            logger.debug('\tresponse: %s' % r.json())
        except:
            logger.debug('\tresponse: %s' % r.content)

        return r

    def emails(self):
        """ API call to get a list of emails """
        return self._api_request(self.EMAILS_ENDPOINT, self.HTTP_GET)

    def send(self, email_id, recipient, email_data=None, sender=None, cc=None,
            bcc=None):
        """ API call to send an email """
        if not email_data:
            email_data = {}

        # for backwards compatibility, will be removed
        if isinstance(recipient, basestring):
            warnings.warn("Passing email directly for recipient is deprecated", DeprecationWarning)
            recipient = { 'address' : recipient }

        payload = {
            'email_id':  email_id,
            'recipient': recipient,
            'email_data': email_data
        }

        if sender:
            payload['sender'] = sender
        if cc:
            if not type(cc) == list:
                logger.error('kwarg cc must be type(list), got %s' % type(cc))
            payload['cc'] = cc
        if bcc:
            if not type(bcc) == list:
                logger.error('kwarg bcc must be type(list), got %s' % type(bcc))
            payload['bcc'] = bcc

        return self._api_request(self.SEND_ENDPOINT, self.HTTP_POST, payload=payload)

