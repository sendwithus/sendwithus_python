"""
Send With Us - Python Client
Copyright SendWithus 2013
"""
import logging
import requests
from json import dumps

FORMAT = '%(asctime)-15s %(message)s'
logger = logging.getLogger('sendwithus')
logger.propagate = False

class api:
    API_PROTO = 'https'
    API_PORT = '443'
    API_HOST = 'beta.sendwithus.com'
    API_VERSION = '1_0'
    API_HEADER_KEY = 'X-SWU-API-KEY'

    EMAILS_ENDPOINT = 'emails'
    SEND_ENDPOINT = 'send'

    API_CLIENT_VERSION = '1.0.0'
    API_KEY = 'THIS_IS_A_TEST_API_KEY'

    DEBUG = False

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

        if self.DEBUG:
            logging.basicConfig(format=FORMAT, level=logging.DEBUG)
            logger.debug('Debug enabled')
            logger.propagate = True

    def _build_request_path(self, endpoint):
        path = "%s://%s:%s/api/v%s/%s" % (self.API_PROTO, self.API_HOST, 
                self.API_PORT, self.API_VERSION, endpoint)

        logger.debug('\tpath: %s' % path)

        return path

    def _api_request(self, endpoint, *args, **kwargs):
        """Private method for api requests"""
        logger.debug(' > Sending API request to endpoint: %s' % endpoint)

        headers = {self.API_HEADER_KEY: self.API_KEY,
            'Content-type': 'application/json', 
            'Accept': 'text/plain'
        }

        if 'headers' in args:
            headers.update(kwargs['headers'])

        logger.debug('\theaders: %s' % headers)

        data = None
        if 'payload' in kwargs:
            data = dumps(kwargs['payload'])
        
        logger.debug('\tdata: %s' % data)

        path = self._build_request_path(endpoint)

        # if no data assume a GET
        if (data):
            r = requests.post(path, data=data, headers=headers)
        else:
            r = requests.get(path, headers=headers)

        logger.debug('\tresponse code:%s' % r.status_code)
        try:
            logger.debug('\tresponse: %s' % r.json())
        except:
            logger.debug('\tresponse: %s' % r.content)

        return r

    def emails(self):
        return self._api_request(self.EMAILS_ENDPOINT)

    def send(self, email_id, recipient, sender=None, email_data=None):
        if not email_data:
            email_data = {}
        if not sender:
            sender = {}

        if sender:    
            payload = {
                'email_id':  email_id,
                'recipient': recipient,
                'sender': sender,
                'email_data': email_data
            }
        else:
            payload = {
                'email_id':  email_id,
                'recipient': recipient,
                'email_data': email_data
            }

        return self._api_request(self.SEND_ENDPOINT, payload=payload)

