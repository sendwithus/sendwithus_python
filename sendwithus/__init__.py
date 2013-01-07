#!/usr/bin/env python
"""
Send With Us - Python Client
Copyright SendWithus 2013
"""

try:
    import urllib2 as urllib
    from urllib import urlencode
except:
    import urllib

class SWUApi(object):
    API_PROTOCOL = 'https'
    API_HOST = 'api.sendwithus.com'
    API_VERSION = '0'
    SEND_ENDPOINT = 'send'


    API_CLIENT_VERSION = '0.1'
    API_KEY = '0'

    def __init__(self, api_key=None, wait=False, *args, **kwargs):
        """Constructor, expects api key"""

        if not api_key:
            raise Exception("You must speicfy an api key")

        self.API_KEY = api_key
        self.wait = wait

    def _build_request_path(self, endpoint):
        return "%s://%s/v%s/%s" % (self.API_PROTOCOL, self.API_HOST, 
                self.API_VERSION, endpoint)

    def _api_request(self, endpoint, *args, **kwargs):
        """Private method for api requests"""

        headers = {'X-SWU-API-KEY': self.API_KEY}

        if 'headers' in args:
            headers.update(kwargs['headers'])

        data = urlencode(kwargs['data'])
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

