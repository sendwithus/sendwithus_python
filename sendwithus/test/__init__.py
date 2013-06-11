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
        self.recipient = {
                'name': 'Matt',
                'address': 'us@sendwithus.com'}
        self.incomplete_recipient = {'name': 'Matt'}
        self.email_data = {
                'name': 'Jimmy',
                'plants': ['Tree', 'Bush', 'Shrub']}
        self.sender = {
                'name': 'Company',
                'address':'company@company.com',
                'reply_to':'info@company.com'}
        self.cc_test = [{
                'name': 'Matt CC',
                'address': 'test+cc@sendwithus.com'}]
        self.bcc_test = [{
                'name': 'Matt BCC',
                'address': 'test+bcc@sendwithus.com'}]

    def assertSuccess(self, result):
        self.assertEqual(result.status_code, 200)
        try:
            self.assertIsNotNone(result.json())
        except:
            self.fail("json() data expected on success")

    def assertSuccessSend(self, result):
        self.assertSuccess(result)
        self.assertEqual(result.json().get('status'), 'OK')
        self.assertTrue(result.json().get('success'))
        self.assertIsNotNone(result.json().get('receipt_id'))

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
        result = self.api.send(self.EMAIL_ID, self.recipient, email_data=self.email_data, sender=self.sender)
        self.assertSuccess(result)

    def test_send_cc(self):
        """ Test send with cc info. """
        result = self.api.send(self.EMAIL_ID, self.recipient, email_data=self.email_data, cc=self.cc_test)
        self.assertSuccess(result)

    def test_send_bcc(self):
        """ Test send with bcc info. """
        result = self.api.send(self.EMAIL_ID, self.recipient, email_data=self.email_data, bcc=self.bcc_test)
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

    def test_send_invalid_cc(self):
        result = self.api.send(self.EMAIL_ID, self.recipient, email_data=self.email_data, cc='bad')
        self.assertFail(result)

    def test_send_invalid_bcc(self):
        result = self.api.send(self.EMAIL_ID, self.recipient, email_data=self.email_data, bcc='bad')
        self.assertFail(result)


if __name__ == '__main__':
    unittest.main()

