import unittest

from sendwithus import api

class TestAPI(unittest.TestCase):
    API_KEY = 'THIS_IS_A_TEST_API_KEY'
    options = {
        'DEBUG': True,
        'API_PROTO': 'http',
        'API_HOST': 'beta.sendwithus.com',
        'API_PORT': '80'
    }

    def setUp(self):
        self.api = api(self.API_KEY, **self.options) 

    def test_send(self):
        data = {'name': 'Jimmy'}
        self.api.send('test', 'test@sendwithus.com', data=data)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()

