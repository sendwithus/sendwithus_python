"""
sendwithus - Python Client
For more information, visit http://www.sendwithus.com
"""

import base64
import json
import logging
import warnings

import requests
import six
from six import string_types

from .encoder import SendwithusJSONEncoder
from .exceptions import APIError, AuthenticationError, ServerError
from .version import version

LOGGER_FORMAT = '%(asctime)-15s %(message)s'
logger = logging.getLogger('sendwithus')
logger.propagate = False


class api:
    API_PROTO = 'https'
    API_PORT = '443'
    API_HOST = 'api.sendwithus.com'
    API_VERSION = '1'
    API_HEADER_KEY = 'X-SWU-API-KEY'
    API_HEADER_CLIENT = 'X-SWU-API-CLIENT'

    HTTP_GET = 'GET'
    HTTP_POST = 'POST'
    HTTP_PUT = 'PUT'
    HTTP_DELETE = 'DELETE'

    LOGS_ENDPOINT = 'logs'
    GET_LOG_ENDPOINT = 'logs/%s'
    GET_LOG_EVENTS_ENDPOINT = 'logs/%s/events'
    TEMPLATES_ENDPOINT = 'templates'
    TEMPLATES_SPECIFIC_ENDPOINT = 'templates/%s'
    TEMPLATES_LOCALES_ENDPOINT = 'templates/%s/locales'
    TEMPLATES_SPECIFIC_LOCALE_VERSIONS_ENDPOINT = \
        'templates/%s/locales/%s/versions'
    TEMPLATES_NEW_VERSION_ENDPOINT = 'templates/%s/versions'
    TEMPLATES_VERSION_ENDPOINT = 'templates/%s/versions/%s'
    SNIPPETS_ENDPOINT = 'snippets'
    SNIPPET_ENDPOINT = 'snippets/%s'
    SEND_ENDPOINT = 'send'
    SEGMENTS_ENDPOINT = 'segments'
    RUN_SEGMENT_ENDPOINT = 'segments/%s/run'
    SEND_SEGMENT_ENDPOINT = 'segments/%s/send'
    DRIPS_DEACTIVATE_ENDPOINT = 'drips/deactivate'
    CUSTOMER_CREATE_ENDPOINT = 'customers'
    CUSTOMER_DETAILS_ENDPOINT = 'customers/%s'
    CUSTOMER_DELETE_ENDPOINT = 'customers/%s'
    CUSTOMER_CONVERSION_ENDPOINT = 'customers/%s/conversions'
    CUSTOMER_GROUPS_ENDPOINT = 'customers/%s/groups/%s'
    GROUPS_ENDPOINT = 'groups'
    GROUP_ENDPOINT = 'groups/%s'
    DRIP_CAMPAIGN_LIST_ENDPOINT = 'drip_campaigns'
    DRIP_CAMPAIGN_ACTIVATE_ENDPOINT = 'drip_campaigns/%s/activate'
    DRIP_CAMPAIGN_DEACTIVATE_ENDPOINT = 'drip_campaigns/%s/deactivate'
    DRIP_CAMPAIGN_DETAILS_ENDPOINT = 'drip_campaigns/%s'
    DRIP_CAMPAIGN_CUSTOMERS_ENDPOINT = 'drip_campaigns/%s/customers'
    DRIP_CAMPAIGN_STEP_CUSTOMERS_ENDPOINT = \
        'drip_campaigns/%s/steps/%s/customers'
    BATCH_ENDPOINT = 'batch'
    RENDER_ENDPOINT = 'render'

    API_CLIENT_LANG = 'python'
    API_CLIENT_VERSION = version
    API_KEY = 'THIS_IS_A_TEST_API_KEY'

    DEBUG = False
    DEFAULT_TIMEOUT = None

    def __init__(
        self,
        api_key=None,
        json_encoder=SendwithusJSONEncoder,
        raise_errors=False,
        default_timeout=None,
        **kwargs
    ):
        """Constructor, expects api key"""

        if not api_key:
            raise Exception("You must specify an api key")

        self.API_KEY = api_key
        self.DEFAULT_TIMEOUT = default_timeout
        self._json_encoder = json_encoder
        self._raise_errors = raise_errors

        if 'API_HOST' in kwargs:
            self.API_HOST = kwargs['API_HOST']
        if 'API_PROTO' in kwargs:
            self.API_PROTO = kwargs['API_PROTO']
        if 'API_PORT' in kwargs:
            self.API_PORT = kwargs['API_PORT']
        if 'API_VERSION' in kwargs:
            self.API_VERSION = kwargs['API_VERSION']
        if 'DEBUG' in kwargs:
            self.DEBUG = kwargs['DEBUG']

        if self.DEBUG:
            logging.basicConfig(format=LOGGER_FORMAT, level=logging.DEBUG)
            logger.debug('Debug enabled')
            logger.propagate = True

    def _build_http_auth(self):
        return (self.API_KEY, '')

    def _build_request_headers(self, custom_headers=None):
        client_header = '%s-%s' % (
            self.API_CLIENT_LANG,
            self.API_CLIENT_VERSION
        )

        headers = {
            self.API_HEADER_CLIENT: client_header,
            'Content-type': 'application/json',
            'Accept': 'text/plain'
        }

        if custom_headers:
            headers.update(custom_headers)

        return headers

    def _build_request_path(self, endpoint, absolute=True):
        path = '/api/v%s/%s' % (self.API_VERSION, endpoint)
        if absolute:
            path = "%s://%s:%s%s" % (
                self.API_PROTO,
                self.API_HOST,
                self.API_PORT,
                path
            )
        return path

    def _build_payload(self, data):
        if not data:
            return None
        return json.dumps(data, cls=self._json_encoder)

    def _parse_response(self, response):
        """Parses the API response and raises appropriate errors if
        raise_errors was set to True
        """
        if not self._raise_errors:
            return response

        is_4xx_error = str(response.status_code)[0] == '4'
        is_5xx_error = str(response.status_code)[0] == '5'
        content = response.content

        if response.status_code == 403:
            raise AuthenticationError(content)
        elif is_4xx_error:
            raise APIError(content)
        elif is_5xx_error:
            raise ServerError(content)

        return response

    def _api_request(self, endpoint, http_method, *args, **kwargs):
        """Private method for api requests"""
        logger.debug(' > Sending API request to endpoint: %s' % endpoint)

        auth = self._build_http_auth()

        headers = self._build_request_headers(kwargs.get('headers'))
        logger.debug('\theaders: %s' % headers)

        path = self._build_request_path(endpoint)
        logger.debug('\tpath: %s' % path)

        data = self._build_payload(kwargs.get('payload'))
        logger.debug('\tdata: %s' % data)

        req_kw = dict(
            auth=auth,
            headers=headers,
            timeout=kwargs.get('timeout', self.DEFAULT_TIMEOUT)
        )

        # do some error handling
        if (http_method == self.HTTP_POST):
            if (data):
                r = requests.post(path, data=data, **req_kw)
            else:
                r = requests.post(path, **req_kw)
        elif http_method == self.HTTP_PUT:
            if (data):
                r = requests.put(path, data=data, **req_kw)
            else:
                r = requests.put(path, **req_kw)
        elif http_method == self.HTTP_DELETE:
            r = requests.delete(path, **req_kw)
        else:
            r = requests.get(path, **req_kw)

        logger.debug('\tresponse code:%s' % r.status_code)
        try:
            logger.debug('\tresponse: %s' % r.json())
        except:
            logger.debug('\tresponse: %s' % r.content)

        return self._parse_response(r)

    def logs(self, timeout=None):
        """ API call to get a list of logs """
        return self._api_request(
            self.LOGS_ENDPOINT,
            self.HTTP_GET,
            timeout=timeout
        )

    def get_log(self, log_id, timeout=None):
        """ API call to get a specific log entry """
        return self._api_request(
            self.GET_LOG_ENDPOINT % log_id,
            self.HTTP_GET,
            timeout=timeout
        )

    def get_log_events(self, log_id, timeout=None):
        """ API call to get a specific log entry """
        return self._api_request(
            self.GET_LOG_EVENTS_ENDPOINT % log_id,
            self.HTTP_GET,
            timeout=timeout
        )

    def emails(self):
        """ [DEPRECATED] API call to get a list of emails """
        return self.templates()

    def templates(self, timeout=None):
        """ API call to get a list of templates """
        return self._api_request(
            self.TEMPLATES_ENDPOINT,
            self.HTTP_GET,
            timeout=timeout
        )

    def get_template(self, template_id, version=None, timeout=None):
        """ API call to get a specific template """
        if (version):
            return self._api_request(
                self.TEMPLATES_VERSION_ENDPOINT % (template_id, version),
                self.HTTP_GET,
                timeout=timeout
            )
        else:
            return self._api_request(
                self.TEMPLATES_SPECIFIC_ENDPOINT % template_id,
                self.HTTP_GET,
                timeout=timeout
            )

    def create_email(self, name, subject, html, text=''):
        """ [DECPRECATED] API call to create an email """
        return self.create_template(name, subject, html, text)

    def create_template(
        self,
        name,
        subject,
        html,
        text='',
        timeout=None
    ):
        """ API call to create a template """
        payload = {
            'name': name,
            'subject': subject,
            'html': html,
            'text': text
        }

        return self._api_request(
            self.TEMPLATES_ENDPOINT,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )

    def create_new_locale(
        self,
        template_id,
        locale,
        version_name,
        subject,
        text='',
        html='',
        timeout=None
    ):
        """ API call to create a new locale and version of a template """
        payload = {
            'locale': locale,
            'name': version_name,
            'subject': subject
        }

        if html:
            payload['html'] = html
        if text:
            payload['text'] = text

        return self._api_request(
            self.TEMPLATES_LOCALES_ENDPOINT % template_id,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )

    def create_new_version(
        self,
        name,
        subject,
        text='',
        template_id=None,
        html=None,
        locale=None,
        timeout=None
    ):
        """ API call to create a new version of a template """
        if(html):
            payload = {
                'name': name,
                'subject': subject,
                'html': html,
                'text': text
            }
        else:
            payload = {
                'name': name,
                'subject': subject,
                'text': text
            }

        if locale:
            url = self.TEMPLATES_SPECIFIC_LOCALE_VERSIONS_ENDPOINT % (
                template_id,
                locale
            )
        else:
            url = self.TEMPLATES_NEW_VERSION_ENDPOINT % template_id

        return self._api_request(
            url,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )

    def update_template_version(
        self,
        name,
        subject,
        template_id,
        version_id,
        text='',
        html=None,
        timeout=None
    ):
        """ API call to update a template version """
        if(html):
            payload = {
                'name': name,
                'subject': subject,
                'html': html,
                'text': text
            }
        else:
            payload = {
                'name': name,
                'subject': subject,
                'text': text
            }

        return self._api_request(
            self.TEMPLATES_VERSION_ENDPOINT % (template_id, version_id),
            self.HTTP_PUT,
            payload=payload,
            timeout=timeout
        )

    def snippets(self, timeout=None):
        """ API call to get list of snippets """
        return self._api_request(
            self.SNIPPETS_ENDPOINT,
            self.HTTP_GET,
            timeout=timeout
        )

    def get_snippet(self, snippet_id, timeout=None):
        """ API call to get a specific Snippet """
        return self._api_request(
            self.SNIPPET_ENDPOINT % (snippet_id),
            self.HTTP_GET,
            timeout=timeout
        )

    def create_snippet(self, name, body, timeout=None):
        """ API call to create a Snippet """
        payload = {
            'name': name,
            'body': body
        }
        return self._api_request(
            self.SNIPPETS_ENDPOINT,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )

    def update_snippet(self, snippet_id, name, body, timeout=None):
        payload = {
            'name': name,
            'body': body
        }

        return self._api_request(
            self.SNIPPET_ENDPOINT % (snippet_id),
            self.HTTP_PUT,
            payload=payload,
            timeout=timeout
        )

    def drip_deactivate(self, email_address, timeout=None):
        payload = {'email_address': email_address}

        return self._api_request(
            self.DRIPS_DEACTIVATE_ENDPOINT,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )

    def send(
        self,
        email_id,
        recipient,
        email_data=None,
        sender=None,
        cc=None,
        bcc=None,
        tags=[],
        headers={},
        esp_account=None,
        locale=None,
        email_version_name=None,
        inline=None,
        files=[],
        timeout=None
    ):
        """ API call to send an email """
        if not email_data:
            email_data = {}

        # for backwards compatibility, will be removed
        if isinstance(recipient, string_types):
            warnings.warn(
                "Passing email directly for recipient is deprecated",
                DeprecationWarning)
            recipient = {'address': recipient}

        payload = {
            'email_id': email_id,
            'recipient': recipient,
            'email_data': email_data
        }

        if sender:
            payload['sender'] = sender
        if cc:
            if not type(cc) == list:
                logger.error(
                    'kwarg cc must be type(list), got %s' % type(cc))
            payload['cc'] = cc
        if bcc:
            if not type(bcc) == list:
                logger.error(
                    'kwarg bcc must be type(list), got %s' % type(bcc))
            payload['bcc'] = bcc

        if tags:
            if not type(tags) == list:
                logger.error(
                    'kwarg tags must be type(list), got %s' % (type(tags)))
            payload['tags'] = tags

        if headers:
            if not type(headers) == dict:
                logger.error(
                    'kwarg headers must be type(dict), got %s' % (
                        type(headers)
                    )
                )
            payload['headers'] = headers

        if esp_account:
            if not isinstance(esp_account, string_types):
                logger.error(
                    'kwarg esp_account must be a string, got %s' % (
                        type(esp_account)
                    )
                )
            payload['esp_account'] = esp_account

        if locale:
            if not isinstance(locale, string_types):
                logger.error(
                    'kwarg locale must be a string, got %s' % (type(locale))
                )
            payload['locale'] = locale

        if email_version_name:
            if not isinstance(email_version_name, string_types):
                logger.error(
                    'kwarg email_version_name must be a string, got %s' % (
                        type(email_version_name)))
            payload['version_name'] = email_version_name

        if inline:
            if isinstance(inline, file):  # noqa, until #47 is fixed
                image = {
                    'id': inline.name,
                    'data': (
                        base64.b64encode(inline.read()).decode()
                        if six.PY3 else base64.b64encode(inline.read())
                    )
                }

                payload['inline'] = image

            else:
                logger.error(
                    'kwarg files must be type(file), got %s' % type(inline))

        if files:
            file_list = []
            if isinstance(files, list):
                for f in files:
                    if isinstance(f, dict):
                        file_obj = f['file']
                        if 'filename' in f:
                            file_name = f['filename']
                        else:
                            file_name = file_obj.name
                    else:
                        file_obj = f
                        file_name = f.name

                    file_list.append(
                        {'id': file_name,
                         'data': base64.b64encode(file_obj.read()).decode()
                         if six.PY3 else base64.b64encode(file_obj.read())}
                    )

                payload['files'] = file_list

            else:
                logger.error(
                    'kwarg files must be type(list), got %s' % type(files))

        return self._api_request(
            self.SEND_ENDPOINT,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )

    def segments(self, timeout=None):
        """ API call to get a list of segments """
        return self._api_request(
            self.SEGMENTS_ENDPOINT,
            self.HTTP_GET,
            timeout=timeout
        )

    def run_segment(self, segment_id, timeout=None):
        """ API call to run a segment, and return the customers"""
        return self._api_request(
            self.RUN_SEGMENT_ENDPOINT % segment_id,
            self.HTTP_GET,
            timeout=timeout
        )

    def send_segment(
        self,
        email_id,
        segment_id,
        email_data=None,
        timeout=None
    ):
        """ API call to send a template, with data, to an entire segment"""
        if not email_data:
            email_data = {}

        payload = {
            'email_id': email_id,
            'email_data': email_data
        }

        return self._api_request(
            self.SEND_SEGMENT_ENDPOINT % segment_id,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )

    def customer_create(self, email, data=None, timeout=None):
        if not data:
            data = {}

        payload = {
            'email': email,
            'data': data
        }

        return self._api_request(
            self.CUSTOMER_CREATE_ENDPOINT,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )

    def customer_details(self, email, timeout=None):
        endpoint = self.CUSTOMER_DETAILS_ENDPOINT % email

        return self._api_request(
            endpoint,
            self.HTTP_GET,
            timeout=timeout
        )

    def customer_delete(self, email, timeout=None):
        endpoint = self.CUSTOMER_DELETE_ENDPOINT % email

        return self._api_request(
            endpoint,
            self.HTTP_DELETE,
            timeout=timeout
        )

    def customer_conversion(self, email, revenue=None, timeout=None):
        endpoint = self.CUSTOMER_CONVERSION_ENDPOINT % email

        payload = {
            'revenue': revenue
        }

        return self._api_request(
            endpoint,
            self.HTTP_POST,
            payload=payload,
            timeout=None
        )

    def create_customer_group(
        self,
        name,
        description='',
        timeout=None
    ):
        endpoint = self.GROUPS_ENDPOINT

        payload = {
            "name": name,
            "description": description
        }
        return self._api_request(
            endpoint,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )

    def delete_customer_group(self, group_id, timeout=None):
        endpoint = self.GROUP_ENDPOINT % group_id

        return self._api_request(
            endpoint,
            self.HTTP_DELETE,
            timeout=timeout
        )

    def update_customer_group(
        self,
        group_id,
        name='',
        description='',
        timeout=None
    ):
        endpoint = self.GROUP_ENDPOINT % group_id

        payload = {
            "name": name,
            "description": description
        }

        return self._api_request(
            endpoint,
            self.HTTP_PUT,
            payload=payload,
            timeout=timeout
        )

    def add_customer_to_group(self, email, group_id, timeout=None):
        endpoint = self.CUSTOMER_GROUPS_ENDPOINT % (email, group_id)
        return self._api_request(
            endpoint,
            self.HTTP_POST,
            timeout=timeout
        )

    def remove_customer_from_group(
        self,
        email,
        group_id,
        timeout=None
    ):
        endpoint = self.CUSTOMER_GROUPS_ENDPOINT % (email, group_id)
        return self._api_request(
            endpoint,
            self.HTTP_DELETE,
            timeout=timeout
        )

    def list_drip_campaigns(self, timeout=None):
        return self._api_request(
            self.DRIP_CAMPAIGN_LIST_ENDPOINT,
            self.HTTP_GET,
            timeout=timeout
        )

    def start_on_drip_campaign(
        self,
        drip_campaign_id,
        recipient,
        email_data={},
        sender=None,
        cc=None,
        bcc=None,
        tags=[],
        esp_account=None,
        locale=None,
        timeout=None
    ):
        endpoint = self.DRIP_CAMPAIGN_ACTIVATE_ENDPOINT % drip_campaign_id

        payload = {
            'recipient': recipient,
            'email_data': email_data
        }

        # Optional params

        if sender:
            payload['sender'] = sender

        if cc:
            if not type(cc) == list:
                logger.error(
                    'kwarg cc must be type(list), got %s' % type(cc))
            payload['cc'] = cc

        if bcc:
            if not type(bcc) == list:
                logger.error(
                    'kwarg bcc must be type(list), got %s' % type(bcc))
            payload['bcc'] = bcc

        if tags:
            if not type(tags) == list:
                logger.error(
                    'kwarg tags must be type(list), got %s' % (type(tags)))
            payload['tags'] = tags

        if esp_account:
            if not isinstance(esp_account, string_types):
                logger.error(
                    'kwarg esp_account must be a string, got %s' % (
                        type(esp_account)
                    )
                )
            payload['esp_account'] = esp_account

        if locale:
            if not isinstance(locale, string_types):
                logger.error(
                    'kwarg locale must be a string, got %s' % (type(locale))
                )
            payload['locale'] = locale

        return self._api_request(
            endpoint,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )

    def remove_from_drip_campaign(
        self,
        recipient_address,
        drip_campaign_id,
        timeout=None
    ):
        endpoint = self.DRIP_CAMPAIGN_DEACTIVATE_ENDPOINT % drip_campaign_id
        payload = {
            'recipient_address': recipient_address
        }

        return self._api_request(
            endpoint,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )

    def drip_campaign_details(self, drip_campaign_id, timeout=None):
        endpoint = self.DRIP_CAMPAIGN_DETAILS_ENDPOINT % drip_campaign_id

        return self._api_request(
            endpoint,
            self.HTTP_GET,
            timeout=timeout
        )

    def start_batch(self):
        return BatchAPI(
            api_key=self.API_KEY,
            API_HOST=self.API_HOST,
            API_PROTO=self.API_PROTO,
            API_PORT=self.API_PORT,
            API_VERSION=self.API_VERSION,
            DEBUG=self.DEBUG,
            json_encoder=self._json_encoder
        )

    def render(
        self,
        email_id,
        email_data,
        version_id=None,
        version_name=None,
        strict=False,
        timeout=None
    ):

        payload = {
            "template_id": email_id,
            "template_data": email_data
        }

        if version_id:
            payload['version_id'] = version_id

        if version_name:
            payload['version_name'] = version_name

        if strict:
            payload['strict'] = strict

        return self._api_request(
            self.RENDER_ENDPOINT,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )


class BatchAPI(api):

    def __init__(self, *args, **kwargs):
        api.__init__(self, *args, **kwargs)
        self._commands = []

    def _api_request(self, endpoint, http_method, *args, **kwargs):
        """Private method for api requests"""
        logger.debug(' > Queing batch api request for endpoint: %s' % endpoint)

        path = self._build_request_path(endpoint, absolute=False)
        logger.debug('\tpath: %s' % path)

        data = None
        if 'payload' in kwargs:
            data = kwargs['payload']
        logger.debug('\tdata: %s' % data)

        command = {
            "path": path,
            "method": http_method
        }
        if data:
            command['body'] = data

        self._commands.append(command)

    def execute(self, timeout=None):
        """Execute all currently queued batch commands"""
        logger.debug(' > Batch API request (length %s)' % len(self._commands))

        auth = self._build_http_auth()

        headers = self._build_request_headers()
        logger.debug('\tbatch headers: %s' % headers)

        logger.debug('\tbatch command length: %s' % len(self._commands))

        path = self._build_request_path(self.BATCH_ENDPOINT)

        data = json.dumps(self._commands, cls=self._json_encoder)
        r = requests.post(
            path,
            auth=auth,
            headers=headers,
            data=data,
            timeout=(self.DEFAULT_TIMEOUT if timeout is None else timeout)
        )

        self._commands = []

        logger.debug('\tresponse code:%s' % r.status_code)
        try:
            logger.debug('\tresponse: %s' % r.json())
        except:
            logger.debug('\tresponse: %s' % r.content)

        return r

    def command_length(self):
        return len(self._commands)
