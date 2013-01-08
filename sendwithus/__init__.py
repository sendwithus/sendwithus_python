"""
Send With Us - Python Client
Copyright SendWithus 2013
"""
import logging
FORMAT = '%(asctime)-15s %(message)s'
logger = logging.getLogger('sendwithus')
logger.propagate = False

try:
    # this is a botched python2 attempt, do something better later
    import urllib2 as urllib
    from urllib import urlencode
except:
    import urllib

class api:
    API_PROTO = 'https'
    API_PORT = '80'
    API_HOST = 'api.sendwithus.com'
    API_VERSION = '0'
    API_HEADER_KEY = 'X-SWU-API-KEY'

    SEND_ENDPOINT = 'send'

    API_CLIENT_VERSION = '0.1'
    API_KEY = 'xxxexy'

    DEBUG = False

    def __init__(self, api_key=None, wait=False, **kwargs):
        """Constructor, expects api key"""

        if not api_key:
            raise Exception("You must speicfy an api key")

        self.API_KEY = api_key
        self.wait = wait
        
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

        headers = {self.API_HEADER_KEY: self.API_KEY}

        if 'headers' in args:
            headers.update(kwargs['headers'])

        logger.debug('\theaders: %s' % headers)

        data = urlencode(kwargs['data'])
        logger.debug('\tdata: %s' % data)

        path = self._build_request_path(endpoint)
        
        req = urllib.Request(path, data, headers)

        resp = urllib.urlopen(req)
        
        if self.wait:
            return resp.read()

        return True

    def send(self, email_name, email_to, data=None):
        if not data:
            data = {}

        data['email_name'] = email_name
        data['email_to'] = email_to

        return self._api_request(self.SEND_ENDPOINT, data=data)

