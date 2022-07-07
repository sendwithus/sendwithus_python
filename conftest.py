import pytest
import sendwithus
import os


@pytest.fixture
def api_key():
    return os.environ.get('SWU_API_KEY')


@pytest.fixture
def api_options():
    return {'DEBUG': False}


@pytest.fixture
def api(api_key, api_options):
    return sendwithus.api(api_key, **api_options)


@pytest.fixture
def email_id():
    return os.environ.get('TEMPLATE_ID')

@pytest.fixture
def version_id():
    return os.environ.get('VERSION_ID')

@pytest.fixture
def translation_template_id():
    return os.environ.get('TEMPLATE_ID')


@pytest.fixture
def email_address():
    return 'person@example.com'


@pytest.fixture
def enabled_drip_campaign_id():
    return os.environ.get('DRIP_CAMPAIGN_ID')


@pytest.fixture
def disabled_drip_campaign_id():
    return os.environ.get('DRIP_CAMPAIGN_DISABLED_ID')


@pytest.fixture
def drip_campaign_step_id():
    return os.environ.get('DRIP_CAMPAIGN_STEP_ID')


@pytest.fixture
def recipient():
    return {
        'name': 'Test User',
        'address': 'person@example.com'
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
        'address': 'company@example.com',
        'reply_to': 'info@example.com'
    }


@pytest.fixture
def cc_test():
    return [
        {
            'name': 'Test CC',
            'address': 'test+cc@example.com'
        }
    ]


@pytest.fixture
def bcc_test():
    return [
        {
            'name': 'Test BCC',
            'address': 'test+bcc@example.com'
        }
    ]


@pytest.fixture
def translation_file_test():
    return './fixtures/translations.zip'


@pytest.fixture
def translation_tag_test():
    return 'translate'
