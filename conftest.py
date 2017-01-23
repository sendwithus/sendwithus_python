import pytest
import sendwithus


@pytest.fixture
def api_key():
    return 'THIS_IS_A_TEST_API_KEY'


@pytest.fixture
def api_options():
    return {'DEBUG': False}


@pytest.fixture
def api(api_key, api_options):
    return sendwithus.api(api_key, **api_options)


@pytest.fixture
def email_id():
    return 'test_fixture_1'


@pytest.fixture
def email_address():
    return 'person@example.com'


@pytest.fixture
def enabled_drip_campaign_id():
    return 'dc_Rmd7y5oUJ3tn86sPJ8ESCk'


@pytest.fixture
def disabled_drip_campaign_id():
    return 'dc_AjR6Ue9PHPFYmEu2gd8x5V'


@pytest.fixture
def drip_campaign_step_id():
    return 'dcs_yaAMiZNWCLAEGw7GLjBuGY'


@pytest.fixture
def recipient():
    return {
        'name': 'Matt',
        'address': 'us@sendwithus.com'
    }


@pytest.fixture
def email_data():
    return {
        'name': 'Jimmy',
        'plants': ['Tree', 'Bush', 'Shrub']
    }


@pytest.fixture
def sender():
    return {
        'name': 'Company',
        'address': 'company@company.com',
        'reply_to': 'info@company.com'
    }


@pytest.fixture
def cc_test():
    return [
        {
            'name': 'Matt CC',
            'address': 'test+cc@sendwithus.com'
        }
    ]


@pytest.fixture
def bcc_test():
    return [
        {
            'name': 'Matt BCC',
            'address': 'test+bcc@sendwithus.com'
        }
    ]
