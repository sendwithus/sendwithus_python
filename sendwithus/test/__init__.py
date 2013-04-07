import unittest

from sendwithus import api

class TestAPI(unittest.TestCase):
    API_KEY = 'THIS_IS_A_TEST_API_KEY'
    EMAIL_ID = 'test_fixture_1'
    
    options = {
        'DEBUG': False
    }

    def setUp(self):
        self.api = api(self.API_KEY, **self.options)
        self.recipient = {'name': 'Matt', 'address': 'us@sendwithus.com'}
        self.incomplete_recipient = {'name': 'Matt'}
        self.sender = {'name': 'Company', 'address':'company@company.com', 'reply_to':'info@company.com'}
        self.email_data = {'name': 'Jimmy', 'plants': ['Tree', 'Bush', 'Shrub']}

    def assertSuccess(self, result):
        self.assertEqual(result.status_code, 200)
        self.assertIsNotNone(result.json())
        # test status is OK
        # test success
        # test receipt_id for send

    def assertFail(self, result):
        self.assertNotEqual(result.status_code, 200)
        # test status is error

    def test_get_emails(self):
        """ Test emails endpoint. """
        result = self.api.emails()
        self.assertSuccess(result)

    def test_send(self):
        """ Test a send with no sender info. """
        result = self.api.send(self.EMAIL_ID, self.recipient, email_data=self.email_data)
        self.assertSuccess(result)

    def test_send_sender_info(self):
        """ Test send with sender info. """
        result = self.api.send(self.EMAIL_ID, self.recipient, sender=self.sender, email_data=self.email_data)
        self.assertSuccess(result)

    def test_send_incomplete(self):
        """ Test send with incomplete receiver. """
        result = self.api.send(self.EMAIL_ID, self.incomplete_recipient, email_data=self.email_data)
        self.assertFail(result)

    def test_send_invalid_apikey(self):
        """ Test send with invalid API key. """
        invalid_api = api('INVALID_API_KEY', **self.options)
        result = invalid_api.send(self.EMAIL_ID, self.recipient, email_data=self.email_data)
        self.assertFail(result)
        self.assertEqual(result.status_code, 403) # bad api key

    def test_send_invalid_email(self):
        """ Test send with ivalid email_id. """
        result = self.api.send('INVALID_EMAIL_ID', self.recipient, email_data=self.email_data)
        self.assertFail(result)
        self.assertEqual(result.status_code, 404) # invalid email_id


if __name__ == '__main__':
    unittest.main()

