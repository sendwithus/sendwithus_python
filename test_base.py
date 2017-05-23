import json
import decimal
import tempfile
import time

import pytest
import six

import sendwithus
from sendwithus.exceptions import APIError, AuthenticationError


def assert_success(result):
    assert result.status_code == 200
    data = result.json()
    assert data is not None, data


def test_get_emails(api):
    """ Test emails endpoint. """
    result = api.emails()
    assert_success(result)


def test_get_template(api):
    """ Test template endpoint. """
    result = api.get_template("pmaBsiatWCuptZmojWESme")
    assert_success(result)


def test_get_template_with_version(api):
    """ Test template with version endpoint. """
    result = api.get_template(
        'pmaBsiatWCuptZmojWESme',
        version='ver_pYj27c8DTBsWB4MRsoB2MF'
    )
    assert_success(result)


def test_create_email_success(api):
    """ Test create emails endpoint """
    result = api.create_email(
        'name',
        'subject',
        '<html><head></head><body></body></html>')
    assert_success(result)


def test_create_new_version_success(api):
    result = api.create_new_version(
        'name',
        'subject',
        text="Some stuff",
        template_id="pmaBsiatWCuptZmojWESme"
    )
    assert_success(result)


def test_update_template_version(api):
    result = api.update_template_version(
        'name',
        'subject',
        'pmaBsiatWCuptZmojWESme',
        'ver_pYj27c8DTBsWB4MRsoB2MF',
        text='Some more stuff',
    )
    assert_success(result)


def test_create_email_bad_name(api):
    """ Test create emails endpoint empty name"""
    result = api.create_email(
        '', 'subject', '<html><head></head><body></body></html>')
    assert result.status_code == 400


def test_create_email_bad_subject(api):
    """ Test create emails endpoint empty subject"""
    result = api.create_email(
        'name', '', '<html><head></head><body></body></html>')
    assert result.status_code == 400


def test_create_email_bad_html(api):
    """ Test create emails endpoint invalid html (no longer fails) """
    result = api.create_email(
        'name', 'subject', '<html><he></body></html>')
    assert result.status_code == 200


def test_send(api, email_id, recipient, email_data):
    """ Test a send with no sender info. """
    result = api.send(email_id, recipient, email_data=email_data)
    assert_success(result)


def test_send_decimal(api, email_id, recipient):
    """ Test a send with decimal in json """
    result = api.send(
        email_id,
        recipient,
        email_data={
            'decimal': decimal.Decimal('5.5')
        }
    )
    assert_success(result)


def test_send_sender_info(api, email_id, recipient, email_data, sender):
    """ Test send with sender info. """
    result = api.send(
        email_id,
        recipient,
        email_data=email_data,
        sender=sender
    )
    assert_success(result)


def test_send_cc(api, email_id, recipient, email_data, cc_test):
    """ Test send with cc info. """
    result = api.send(
        email_id,
        recipient,
        email_data=email_data,
        cc=cc_test
    )
    assert_success(result)


def test_send_bcc(api, email_id, recipient, email_data, bcc_test):
    """ Test send with bcc info. """
    result = api.send(
        email_id,
        recipient,
        email_data=email_data,
        bcc=bcc_test
    )
    assert_success(result)


def test_send_incomplete(api, email_id, email_data):
    """ Test send with incomplete receiver. """
    result = api.send(
        email_id,
        {'name': 'Matt'},
        email_data=email_data
    )
    assert result.status_code != 200


def test_send_invalid_apikey(
    api_options,
    email_id,
    recipient,
    email_data
):
    """ Test send with invalid API key. """
    invalid_api = sendwithus.api('INVALID_API_KEY', **api_options)
    result = invalid_api.send(
        email_id,
        recipient,
        email_data=email_data
    )
    assert result.status_code == 403  # bad api key


def test_send_invalid_email(api, recipient, email_data):
    """ Test send with invalid email_id. """
    result = api.send(
        'INVALID_EMAIL_ID',
        recipient,
        email_data=email_data
    )
    assert result.status_code == 400  # invalid email_id


def test_send_invalid_cc(api, email_id, recipient, email_data):
    result = api.send(
        email_id,
        recipient,
        email_data=email_data,
        cc='bad'
    )
    assert result.status_code != 200


def test_send_invalid_bcc(api, email_id, recipient, email_data):
    result = api.send(
        email_id,
        recipient,
        email_data=email_data,
        bcc='bad'
    )
    assert result.status_code != 200


def test_send_tags(api, email_id, recipient, email_data):
    result = api.send(
        email_id,
        recipient,
        email_data=email_data,
        tags=['tag_one', 'tag_two', 'tag_three']
    )
    assert_success(result)


def test_send_tags_invalid(api, email_id, recipient, email_data):
    result = api.send(
        email_id,
        recipient,
        email_data=email_data,
        tags='bad'
    )
    assert result.status_code != 200


def test_send_headers(api, email_id, recipient, email_data):
    result = api.send(
        email_id,
        recipient,
        email_data=email_data,
        headers={'X-HEADER-ONE': 'header-value'}
    )
    assert_success(result)


def test_send_headers_invalid(api, email_id, recipient, email_data):
    result = api.send(
        email_id,
        recipient,
        email_data=email_data,
        headers='X-HEADER-ONE'
    )
    assert result.status_code != 200


@pytest.yield_fixture
def file():
    with tempfile.NamedTemporaryFile() as tempf:
        data = ('simple file content' + '\n') * 3
        tempf.write(bytes(data, 'utf-8')) \
            if six.PY3 else tempf.write(data)
        tempf.seek(0)
        yield tempf


def test_send_with_files_valid(api, email_id, recipient, email_data, file):
        result = api.send(
            email_id,
            recipient,
            email_data=email_data,
            files=[file])

        assert result.status_code == 200


def test_send_with_inline_valid(api, email_id, recipient, email_data, file):
        result = api.send(
            email_id,
            recipient,
            email_data=email_data,
            inline=file)

        assert result.status_code == 200


def test_send_with_files_explicit_filename(api, email_id,
                                           recipient, email_data, file):
        result = api.send(
            email_id,
            recipient,
            email_data=email_data,
            files=[{'file': file,
                    'filename': 'filename.pdf'}]
        )

        assert result.status_code == 200


def test_send_with_inline_explicit_filename(api, email_id,
                                            recipient, email_data, file):
        result = api.send(
            email_id,
            recipient,
            email_data=email_data,
            inline={'file': file, 'filename': 'filename.pdf'}
        )

        assert result.status_code == 200


def test_send_with_files_valid_1(api, email_id,
                                 recipient, email_data, file):
    result = api.send(
        email_id,
        recipient,
        email_data=email_data,
        files=[{'file': file}]
    )

    assert result.status_code == 200


def test_send_with_inline_valid_1(api, email_id,
                                  recipient, email_data, file):
    result = api.send(
        email_id,
        recipient,
        email_data=email_data,
        inline={'file': file},
    )
    assert result.status_code == 200


def test_send_with_files_invalid(api, email_id,
                                 recipient, email_data, file):
    with pytest.raises(KeyError):
        api.send(
            email_id,
            recipient,
            email_data=email_data,
            files=[{'filename': 'filename.pdf'}]
        )


def test_send_with_inline_invalid(api, email_id,
                                  recipient, email_data, file):
    with pytest.raises(KeyError):
        api.send(
            email_id,
            recipient,
            email_data=email_data,
            inline={'filename': 'filename.pdf'}
        )


def test_send_with_files_invalid_arg(api, email_id, recipient, email_data):
    with pytest.raises(AttributeError):
        api.send(
            email_id,
            recipient,
            email_data=email_data,
            files='1337'
        )


def test_send_with_inline_invalid_arg(api, email_id, recipient, email_data):
    with pytest.raises(AttributeError):
        api.send(
            email_id,
            recipient,
            email_data=email_data,
            inline='1337'
        )


def test_drip_deactivate(api, email_address):
    result = api.drip_deactivate(email_address)
    assert_success(result)


def test_version_name(api, email_id, recipient, email_data):
    result = api.send(
        email_id,
        recipient,
        email_data=email_data,
        email_version_name='version-override'
    )
    assert_success(result)


def test_locale(api, email_id, recipient, email_data):
    result = api.send(
        email_id,
        recipient,
        email_data=email_data,
        locale='sv-SE'
    )
    assert_success(result)


def test_customer_actions(api):
    data = {'first_name': 'Python Client Unit Test'}
    result = api.customer_create('test+python@sendwithus.com', data)
    assert_success(result)
    result = api.customer_delete('test+python@sendwithus.com')
    assert_success(result)


def test_get_customer(api):
    result = api.customer_details('customer@example.com')
    assert_success(result)


def test_list_drip_campaigns(api):
    """ Test listing drip campaigns. """
    result = api.list_drip_campaigns()
    assert_success(result)


def test_start_on_drip_campaign(api, enabled_drip_campaign_id, email_address):
    """ Test starting a customer on a drip campaign. """
    result = api.start_on_drip_campaign(
        enabled_drip_campaign_id,
        {'address': email_address}
    )
    assert_success(result)


def test_start_on_disabled_drip_campaign(
    api,
    disabled_drip_campaign_id,
    email_address
):
    """ Test starting a customer on a drip campaign. """
    result = api.start_on_drip_campaign(
        disabled_drip_campaign_id,
        {'address': email_address}
    )
    assert result.status_code != 200


def test_start_on_false_drip_campaign(api, email_address):
    """ Test starting a customer on a drip campaign. """
    result = api.start_on_drip_campaign(
        'false_drip_campaign_id',
        {'address': email_address}
    )
    assert result.status_code != 200


def test_start_on_drip_campaign_with_data(
    api,
    enabled_drip_campaign_id,
    email_address,
    email_data
):
    """ Test starting a customer on a drip campaign with data. """
    result = api.start_on_drip_campaign(
        enabled_drip_campaign_id,
        {'address': email_address},
        email_data=email_data
    )
    assert_success(result)


def test_remove_from_drip_campaign(
    api,
    email_address,
    enabled_drip_campaign_id
):
    """ Test removing a customer from a drip campaign. """
    result = api.remove_from_drip_campaign(
        email_address,
        enabled_drip_campaign_id
    )
    assert_success(result)


def test_drip_campaign_details(api, enabled_drip_campaign_id):
    """ Test listing drip campaign details. """
    result = api.drip_campaign_details(enabled_drip_campaign_id)
    assert_success(result)


def test_batch_create_customer(api):
    batch_api_one = api.start_batch()
    batch_api_two = api.start_batch()

    data = {'segment': 'Batch Updated Customer'}
    for x in range(10):
        batch_api_one.customer_create(
            'test+python+%s@sendwithus.com' % x,
            data
        )
        assert batch_api_one.command_length() == x + 1

        if (x % 2) == 0:
            batch_api_two.customer_create(
                'test+python+%s+again@sendwithus.com' % x,
                data
            )
            assert batch_api_two.command_length() == x / 2 + 1

    # Run batch 1
    result = batch_api_one.execute().json()
    assert len(result) == 10
    for response in result:
        assert response['status_code'] == 200

    # Batch one should be empty, batch two still full
    assert batch_api_one.command_length() == 0
    assert batch_api_two.command_length() == 5

    result = batch_api_two.execute().json()
    assert len(result) == 5
    for response in result:
        assert response['status_code'] == 200

    # Both batches now empty
    assert batch_api_one.command_length() == 0
    assert batch_api_two.command_length() == 0


def test_render(api, email_id, email_data):
    result = api.render(email_id, email_data)
    assert_success(result)


def test_authentication_error(api_options):
    """Test raises AuthenticationError with invalid api key"""
    invalid_api = sendwithus.api(
        'INVALID_KEY',
        raise_errors=True,
        **api_options
    )

    with pytest.raises(AuthenticationError):
        invalid_api.emails()


def test_invalid_request(api_key, api_options):
    """Test raises APIError with invalid api request & raise_errors=True"""
    swu_api = sendwithus.api(
        api_key,
        raise_errors=True,
        **api_options
    )

    with pytest.raises(APIError):
        swu_api.create_email(
            'name',
            '',
            '<html><head></head><body></body></html>'
        )


def test_raise_errors_option(api_key, api_options):
    """Test raises no exception if raise_errors=False"""
    swu_api = sendwithus.api(
        api_key,
        raise_errors=False,
        **api_options
    )
    response = swu_api.create_email(
        'name',
        '',
        '<html><head></head><body></body></html>'
    )

    assert 400 == response.status_code
