import unittest
import decimal

from sendwithus import api


class TestAPI(unittest.TestCase):
    API_KEY = 'THIS_IS_A_TEST_API_KEY'
    EMAIL_ID = 'test_fixture_1'

    options = {
        'DEBUG': False
    }

    def setUp(self):
        self.api = api(self.API_KEY, **self.options)
        self.email_address = 'person@example.com'
        self.segment_id = 'seg_VC8FDxDno9X64iUPDFSd76'
        self.recipient = {
            'name': 'Matt',
            'address': 'us@sendwithus.com'}
        self.incomplete_recipient = {'name': 'Matt'}
        self.email_data = {
            'name': 'Jimmy',
            'plants': ['Tree', 'Bush', 'Shrub']}
        self.email_data_with_decimal = {
            'decimal': decimal.Decimal('5.5')
        }
        self.sender = {
            'name': 'Company',
            'address': 'company@company.com',
            'reply_to': 'info@company.com'}
        self.cc_test = [{
            'name': 'Matt CC',
            'address': 'test+cc@sendwithus.com'}]
        self.bcc_test = [{
            'name': 'Matt BCC',
            'address': 'test+bcc@sendwithus.com'}]
        self.drip_campaign_id = 'dc_Rmd7y5oUJ3tn86sPJ8ESCk'

    def assertSuccess(self, result):
        self.assertEqual(result.status_code, 200)
        try:
            self.assertNotEqual(result.json(), None)
        except:
            self.fail("json() data expected on success")

    def assertSuccessSend(self, result):
        self.assertSuccess(result)
        self.assertEqual(result.json().get('status'), 'OK')
        self.assertTrue(result.json().get('success'))
        self.assertNotEqual(result.json().get('receipt_id'), None)

    def assertFail(self, result):
        self.assertNotEqual(result.status_code, 200)
        # test status is error

    def test_get_emails(self):
        """ Test emails endpoint. """
        result = self.api.emails()
        self.assertSuccess(result)

    def test_create_email_success(self):
        """ Test create emails endpoint """
        result = self.api.create_email(
            'name', 'subject', '<html><head></head><body></body></html>')
        self.assertSuccess(result)

    def test_create_email_bad_name(self):
        """ Test create emails endpoint empty name"""
        result = self.api.create_email(
            '', 'subject', '<html><head></head><body></body></html>')
        self.assertFail(result)
        self.assertEqual(result.status_code, 400)

    def test_create_email_bad_subject(self):
        """ Test create emails endpoint empty subject"""
        result = self.api.create_email(
            'name', '', '<html><head></head><body></body></html>')
        self.assertFail(result)
        self.assertEqual(result.status_code, 400)

    def test_create_email_bad_html(self):
        """ Test create emails endpoint invalid html"""
        result = self.api.create_email(
            'name', 'subject', '<html><he></body></html>')
        self.assertFail(result)
        self.assertEqual(result.status_code, 400)

    def test_send(self):
        """ Test a send with no sender info. """
        result = self.api.send(
            self.EMAIL_ID,
            self.recipient,
            email_data=self.email_data)
        self.assertSuccess(result)

    def test_send_decimal(self):
        """ Test a send with decimal in json """
        result = self.api.send(
            self.EMAIL_ID,
            self.recipient,
            email_data=self.email_data_with_decimal)
        self.assertSuccess(result)

    def test_send_sender_info(self):
        """ Test send with sender info. """
        result = self.api.send(
            self.EMAIL_ID,
            self.recipient,
            email_data=self.email_data,
            sender=self.sender)
        self.assertSuccess(result)

    def test_send_cc(self):
        """ Test send with cc info. """
        result = self.api.send(
            self.EMAIL_ID,
            self.recipient,
            email_data=self.email_data,
            cc=self.cc_test)
        self.assertSuccess(result)

    def test_send_bcc(self):
        """ Test send with bcc info. """
        result = self.api.send(
            self.EMAIL_ID,
            self.recipient,
            email_data=self.email_data,
            bcc=self.bcc_test)
        self.assertSuccess(result)

    def test_send_incomplete(self):
        """ Test send with incomplete receiver. """
        result = self.api.send(
            self.EMAIL_ID,
            self.incomplete_recipient,
            email_data=self.email_data)
        self.assertFail(result)

    def test_send_invalid_apikey(self):
        """ Test send with invalid API key. """
        invalid_api = api('INVALID_API_KEY', **self.options)
        result = invalid_api.send(
            self.EMAIL_ID,
            self.recipient,
            email_data=self.email_data)
        self.assertFail(result)
        self.assertEqual(result.status_code, 403)  # bad api key

    def test_send_invalid_email(self):
        """ Test send with ivalid email_id. """
        result = self.api.send(
            'INVALID_EMAIL_ID',
            self.recipient,
            email_data=self.email_data)
        self.assertFail(result)
        self.assertEqual(result.status_code, 400)  # invalid email_id

    def test_send_invalid_cc(self):
        result = self.api.send(
            self.EMAIL_ID,
            self.recipient,
            email_data=self.email_data,
            cc='bad')
        self.assertFail(result)

    def test_send_invalid_bcc(self):
        result = self.api.send(
            self.EMAIL_ID,
            self.recipient,
            email_data=self.email_data,
            bcc='bad')
        self.assertFail(result)

    def test_send_tags(self):
        result = self.api.send(
            self.EMAIL_ID,
            self.recipient,
            email_data=self.email_data,
            tags=['tag_one', 'tag_two', 'tag_three'])
        self.assertSuccess(result)

    def test_send_tags_invalid(self):
        result = self.api.send(
            self.EMAIL_ID,
            self.recipient,
            email_data=self.email_data,
            tags='bad')
        self.assertFail(result)

    def test_drip_deactivate(self):
        result = self.api.drip_deactivate(self.email_address)
        self.assertSuccess(result)

    def test_version_name(self):
        result = self.api.send(
            self.EMAIL_ID,
            self.recipient,
            email_data=self.email_data,
            email_version_name='version-override')
        self.assertSuccess(result)

    def test_create_customer(self):
        data = {'first_name': 'Python Client Unit Test'}
        result = self.api.customer_create('test+python@sendwithus.com', data)
        self.assertSuccess(result)

    def test_delete_customer(self):
        result = self.api.customer_delete('test+python@sendwithus.com')
        self.assertSuccess(result)

    def test_send_segment(self):
        result = self.api.send_segment(self.EMAIL_ID, self.segment_id)
        self.assertSuccess(result)

    def test_list_drip_campaigns(self):
        result = self.api.list_drip_campaigns()
        self.assertSuccess(result)

    def test_start_on_drip_campaign(self):
        result = self.api.start_on_drip_campaign(self.email_address, self.drip_campaign_id)
        self.assertSuccess(result)

    def test_remove_from_drip_campaign(self):
        result = self.api.remove_from_drip_campaign(self.email_address, self.drip_campaign_id)
        self.assertSuccess(result)

    def test_drip_campaign_details(self):
        result = self.api.drip_campaign_details(self.drip_campaign_id)
        self.assertSuccess(result)

if __name__ == '__main__':
    unittest.main()
