import unittest

from sendwithus import api

class TestAPI(unittest.TestCase):
    API_KEY = '68c9f6ccd3aa206362640c7fa9be236d4e0dd837'
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

