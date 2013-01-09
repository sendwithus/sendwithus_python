import unittest

from sendwithus import api

class TestAPI(unittest.TestCase):
    API_KEY = '64cc90d08fcb358f34202279c87deed4f2ad29fd'
    options = {
        'DEBUG': True,
        'API_PROTO': 'http',
        'API_HOST': 'localhost',
        'API_PORT': '8000'
    }

    def setUp(self):
        self.api = api(self.API_KEY, **self.options) 

    def test_send(self):
        data = {'name': 'Jimmy'}
        self.api.send('test_send', 'matt@sendwithus.com', data=data)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()

