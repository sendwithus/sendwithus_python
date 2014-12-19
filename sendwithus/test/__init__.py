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
        self.enabled_drip_campaign_id = 'dc_Rmd7y5oUJ3tn86sPJ8ESCk'
        self.disabled_drip_campaign_id = 'dc_AjR6Ue9PHPFYmEu2gd8x5V'
        self.false_drip_campaign_id = 'false_drip_campaign_id'
        self.drip_campaign_step_id = 'dcs_yaAMiZNWCLAEGw7GLjBuGY'

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

    def test_get_template(self):
        """ Test template endpoint. """
        result = self.api.get_template("pmaBsiatWCuptZmojWESme")
        self.assertSuccess(result)

    def test_get_template_with_version(self):
        """ Test template with version endpoint. """
        result = self.api.get_template("pmaBsiatWCuptZmojWESme", version="ver_pYj27c8DTBsWB4MRsoB2MF")
        self.assertSuccess(result)

    def test_create_email_success(self):
        """ Test create emails endpoint """
        result = self.api.create_email(
            'name', 'subject', '<html><head></head><body></body></html>')
        self.assertSuccess(result)

    def test_create_new_version_success(self):
        result = self.api.create_new_version(
            'name', 'subject', text="Some stuff", template_id="pmaBsiatWCuptZmojWESme"
        )
        self.assertSuccess(result)

    def test_update_template_version(self):
        result = self.api.update_template_version(
            'name', 'subject', "pmaBsiatWCuptZmojWESme", "ver_pYj27c8DTBsWB4MRsoB2MF", text="Some more stuff",
        )
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
        """ Test create emails endpoint invalid html (no longer fails) """
        result = self.api.create_email(
            'name', 'subject', '<html><he></body></html>')
        self.assertEqual(result.status_code, 200)

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
        """ Test send with invalid email_id. """
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

    def test_customer_conversion(self):
        result = self.api.customer_conversion('test+python@sendwithus.com')
        self.assertSuccess(result)

    def test_customer_conversion_revenue(self):
        result = self.api.customer_conversion('test+python@sendwithus.com', revenue=1234)
        self.assertSuccess(result)

    def test_send_segment(self):
        result = self.api.send_segment(self.EMAIL_ID, self.segment_id)
        self.assertSuccess(result)

    def test_list_drip_campaigns(self):
        """ Test listing drip campaigns. """
        result = self.api.list_drip_campaigns()
        self.assertSuccess(result)

    def test_start_on_drip_campaign(self):
        """ Test starting a customer on a drip campaign. """
        result = self.api.start_on_drip_campaign(
            self.email_address,
            self.enabled_drip_campaign_id)
        self.assertSuccess(result)

    def test_start_on_disabled_drip_campaign(self):
        """ Test starting a customer on a drip campaign. """
        result = self.api.start_on_drip_campaign(
            self.email_address,
            self.disabled_drip_campaign_id)
        self.assertFail(result)

    def test_start_on_false_drip_campaign(self):
        """ Test starting a customer on a drip campaign. """
        result = self.api.start_on_drip_campaign(
            self.email_address,
            self.false_drip_campaign_id)
        self.assertFail(result)

    def test_start_on_drip_campaign_with_data(self):
        """ Test starting a customer on a drip campaign with data. """
        result = self.api.start_on_drip_campaign(
            self.email_address,
            self.enabled_drip_campaign_id,
            email_data=self.email_data)
        self.assertSuccess(result)

    def test_remove_from_drip_campaign(self):
        """ Test removing a customer from a drip campaign. """
        result = self.api.remove_from_drip_campaign(
            self.email_address,
            self.enabled_drip_campaign_id)
        self.assertSuccess(result)

    def test_drip_campaign_details(self):
        """ Test listing drip campaign details. """
        result = self.api.drip_campaign_details(self.enabled_drip_campaign_id)
        self.assertSuccess(result)

    def test_drip_campaign_customers(self):
        """ Test listing drip campaign customers. """
        result = self.api.drip_campaign_customers(self.enabled_drip_campaign_id)
        self.assertEqual(result.json().get('object'), 'drip_campaign')

    # def test_drip_campaign_step_customers(self):
    #     """ Test listing drip campaign customers. """
    #     result = self.api.drip_campaign_step_customers(
    #         self.enabled_drip_campaign_id, self.drip_campaign_step_id)
    #     self.assertEqual(result.json().get('object'), 'drip_step')

    def test_batch_create_customer(self):
        batch_api = self.api.start_batch()

        data = {'segment': 'Batch Updated Customer'}
        for x in range(10):
            batch_api.customer_create('test+python+%s@sendwithus.com' % x, data)
            self.assertEqual(batch_api.command_length(), x + 1)

        result = batch_api.execute().json()
        # should return a list of 10 result objects
        self.assertEqual(len(result), 10)
        for response in result:
            self.assertEqual(response['status_code'], 200)

        # queue should be empty now.
        self.assertEqual(batch_api.command_length(), 0)

    def test_render(self):
        result = self.api.render(self.EMAIL_ID, self.email_data)
        self.assertSuccess(result)

if __name__ == '__main__':
    unittest.main()
