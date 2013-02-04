import unittest

from sendwithus import api

class TestAPI(unittest.TestCase):
    API_KEY = 'THIS_IS_A_TEST_API_KEY'
    options = {
        'DEBUG': True,
    }

    def setUp(self):
        self.api = api(self.API_KEY, **self.options) 

    def test_send(self):
        email_data = {'name': 'Jimmy'}
        self.api.send('test', 'test@sendwithus.com', email_data=email_data)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()

