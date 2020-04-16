sendwithus python-client
========================

[![Build Status](https://travis-ci.org/sendwithus/sendwithus_python.png)](https://travis-ci.org/sendwithus/sendwithus_python)

## Requirements
- [Python requests library](http://docs.python-requests.org/en/master/user/install/#install)

## Installation
    pip install sendwithus

## Usage

For all examples, assume:
```python
import sendwithus
api = sendwithus.api(api_key='YOUR-API-KEY')
```

### Error Handling
By default, the API calls return a response object. However, you can use
`sendwithus.api(api_key='YOUR-API-KEY', raise_errors=True)` which will raise the following errors:
* `AuthenticationError` - Caused by an invalid API key
* `APIError` - Caused by an invalid API request (4xx error)
* `ServerError` - Caused by a server error (5xx error)

Errors can be imported from the `sendwithus.exceptions` module.

# Templates

### Get Your Templates

```python
api.templates()
```

### Get a Specific Template

```python
api.get_template(
    'YOUR-TEMPLATE-ID'
)
```

### Get a Specific Template Version

```python
api.get_template(
    'YOUR-TEMPLATE-ID',
    version='YOUR-VERSION-ID'
)
```

### Create a Template

```python
api.create_template(
    name='Email Name',
    subject='Email Subject',
    html='<html><head></head><body>Valid HTML</body></html>',
    text='Optional text content'
)
```

### Create a New Locale

```python
api.create_new_locale(
    'YOUR-TEMPLATE-ID',
    locale='fr-FR',
    version_name='Version Name',
    subject='Email Subject',
    html='<html><head></head><body>Valid HTML</body></html>',
    text='Optional text content'
)
```

### Create a New Version

```python
api.create_new_version(
    template_id='YOUR-TEMPLATE-ID',
    name='Version Name',
    subject='Email Subject',
    html='<html><head></head><body>Valid HTML</body></html>',
    text='Optional text content',
    locale='fr-FR'
)
```

### Update a Template Version

```python
api.update_template_version(
    template_id='YOUR-TEMPLATE-ID',
    version_id='YOUR-VERSION-ID',
    name='Email Name'
    subject='Email Subject',
    html='<html><head></head><body>Valid HTML</body></html>',
    text='Optional text content'
)
```

We validate all HTML and will return an error if it's invalid.

```python
r.status_code
# 400
r.content
# 'email html failed to validate'
```

# Send

*NOTE* - If a customer does not exist by the specified email (recipient address), the send call will create a customer.

- email_id                      &mdash; Template ID to send
- recipient
   - address                    &mdash; The recipient's email address
   - name (optional)            &mdash; The recipient's name
- email_data (optional)         &mdash; Object containing email template data
- sender (optional)
   - address                    &mdash; The sender's email address
   - reply_to                   &mdash; The sender's reply-to address
   - name                       &mdash; The sender's name
- cc (optional)                 &mdash; A list of CC recipients, of the format {'address': 'cc@email.com'}
- bcc (optional)                &mdash; A list of BCC recipients, of the format {'address': 'bcc@email.com'}
- headers (options)             &mdash; Object contain SMTP headers to be included with the email
- esp\_account (optional)       &mdash; ID of the ESP Account to send this email through. ex: esp\_1a2b3c4d5e
- files (optional)              &mdash; List of file attachments (combined maximum 7MB)
- inline (optional)             &mdash; Inline attachment object
- locale (optional)             &mdash; Template locale to send (ie: en-US)
- email_version_name (option)   &mdash; Template version to send (ie: Version A)

### Call with REQUIRED parameters only
The `email_data` field is optional, but highly recommended!

```python
r = api.send(
    email_id='YOUR-TEMPLATE-ID',
    recipient={
        'address': 'us@sendwithus.com'
    }
)
print r.status_code
# 200
```

### Call with REQUIRED parameters and email_data
```python
r = api.send(
    email_id='YOUR-TEMPLATE-ID',
    recipient={
        'address': 'us@sendwithus.com'
    },
    email_data={
        'first_name': 'Matt'
    }
)
print r.status_code
# 200
```

### Optional Sender
The `sender['address']` is a required sender field. `sender['name']` and `sender['reply_to']` are both optional.

```python
r = api.send(
    email_id='YOUR-TEMPLATE-ID',
    recipient={
        'name': 'Matt',
        'address': 'us@sendwithus.com'
    },
    email_data={
        'first_name': 'Matt'
    },
    sender={
        'address': 'company@company.com',
        'reply_to':'info@company.com',  # Optional
        'name': 'Company'  # Optional
    }
)
print r.status_code
# 200
```

### Optional CC

```python
r = api.send(
    email_id='YOUR-TEMPLATE-ID',
    recipient={
        'name': 'Matt',
        'address': 'us@sendwithus.com'
    },
    cc=[
        {'address': 'company@company.com'},
        {'address': 'info@company.com'}
    ]
)
print r.status_code
# 200
```

### Optional BCC

```python
r = api.send(
    email_id='YOUR-TEMPLATE-ID',
    recipient={
        'name': 'Matt',
        'address': 'us@sendwithus.com'
    },
    bcc=[
        {'address': 'company@company.com'},
        {'address': 'info@company.com'}
    ]
)
print r.status_code
# 200
```

### Optional Headers

```python
r = api.send(
    email_id='YOUR-TEMPLATE-ID',
    recipient={
        'name': 'Matt',
        'address': 'us@sendwithus.com'
    },
    headers={
        'X-HEADER-ONE': 'header-value'
    }
)
print r.status_code
# 200
```

### Optional ESP Account

```python
r = api.send(
    email_id='YOUR-TEMPLATE-ID',
    recipient={
        'name': 'Matt',
        'address': 'us@sendwithus.com'
    },
    esp_account='YOUR-ESP-ID'
)
print r.status_code
# 200
```

### Optional File Attachments

```python
r = api.send(
    email_id='YOUR-TEMPLATE-ID',
    recipient={
        'name': 'Matt',
        'address': 'us@sendwithus.com'
    },
    files=[
        open('/home/Matt/report1.txt', 'r'),
        open('/home/Matt/report2.txt', 'r')
    ]
)
print r.status_code
# 200
```

### Optional File Attachments with explicit file names

```python
r = api.send(
    email_id='YOUR-TEMPLATE-ID',
    recipient={
        'name': 'Matt',
        'address': 'us@sendwithus.com'
    },
    files=[{
        'file': open('/home/Matt/report1.txt', 'r'),
        'filename': 'arbitrary_file_name.xyz'
    }]
)
print r.status_code
# 200
```

### Optional Inline Image

```python
r = api.send(
    email_id='YOUR-TEMPLATE-ID',
    recipient={
        'name': 'Matt',
        'address': 'us@sendwithus.com'
    },
    inline=open('image.jpg', 'r')
)
print r.status_code
# 200
```

### Optional Inline Image with explicit file names

```python
r = api.send(
    email_id='YOUR-TEMPLATE-ID',
    recipient={
        'name': 'Matt',
        'address': 'us@sendwithus.com'
    },
    inline={
        'file': open('/home/Matt/image.jpg', 'r'),
        'filename': 'cool_image.jpg'
    }
)
print r.status_code
# 200
```

### Optional Locale
```python
r = api.send(
    email_id='YOUR-TEMPLATE-ID',
    recipient={
        'name': 'Matt',
        'address': 'us@sendwithus.com'
    },
    locale='fr-FR'
)
print r.status_code
# 200
```

### Optional Version Name
```python
r = api.send(
    email_id='YOUR-TEMPLATE-ID',
    recipient={
        'name': 'Matt',
        'address': 'us@sendwithus.com'
    },
    email_version_name='Version A'
)
print r.status_code
# 200
```

# Drip Campaigns

### List all Drip Campaigns

List all drip campaigns for the current profile

```python
api.list_drip_campaigns()
```

### Start a Customer on a Drip Campaign

Starts a customer on the first step of a specified drip campaign

```python
api.start_on_drip_campaign(
    'dc_1234asdf1234',
    {'address': 'customer@email.com'}
)
```

### Start a Customer on a Drip Campaign with email_data

You may specify extra data to be merged into the templates in the drip campaign.

*Note* — Any data provided in the `email_data` parameter for `start_on_drip_campaign()` will be used throughout the entire drip campaign.

```python
api.start_on_drip_campaign(
    'dc_1234asdf1234',
    {'address': 'customer@email.com'},
    email_data={'color': 'blue'},
    sender={'address': 'from@email.com'},
    cc=[{'address': 'cc@email.com'}],
    tags=['tag_one', 'tag_two'],
    esp_account='esp_1234',
    locale='fr-FR'
)
```

### Remove a Customer from a Drip Campaign

Deactivates all pending emails for a customer on a specified drip campaign

```python
api.remove_from_drip_campaign(
    'customer@email.com',
    'dc_1234asdf1234'
)
```

### Remove a Customer from all Drip Campaigns

You can deactivate all pending drip campaign emails for a customer

```python
api.drip_deactivate(
    'customer@example.com'
)
```

### Remove a Customer from a Single Drip Campaigns

```python
api.remove_from_drip_campaign(
    'customer@example.com',
    'dc_1234asdf1234'
)
```

### List the details of a specific Drip Campaign

```python
api.drip_campaign_details(
    'dc_1234asdf1234'
)
```

# Customers

### Get a Customer

```python
api.customer_details(
    'customer@example.com'
)
```

### Create/Update Customer Locale

You can use the same endpoint to create or update a customer. This is primarily
used to associate a locale with an email address so Sendwithus can
automatically send them the correct template. Note that if your templates are
only in one language then you don't need to use this feature.

```python
api.customer_create(
    'customer@example.com',
    locale="fr-FR"
)
```


### Delete a Customer

```python
api.customer_delete(
    'customer@example.com'
)
```

# Snippets

### Get All Snippets

```python
api.snippets()
```

### Get a Specific Snippet

```python
api.get_snippet(
    'snp_1234asdf1234'
)
```

### Create a Snippet

```python
api.create_snippet(
    name='My Snippet',
    body='<h1>Snippets!</h1>'
)
```

### Update a Snippet

```python
api.update_snippet(
    'snp_1234asdf1234',
    name='My Snippet',
    body='<h1>Snippets!</h1>'
)
```

# Internationalization (i18n) API

### Get translation package (.pot file)

```python
api.get_translation_template(
    `my_translation_tag`
)
```

### Post translated strings and .po files

```python
with open('my_translation_file', 'rb') as f:
    api.create_translation_file(
        `my_translation_tag`,
        f.read()
    )
```

# Render

### Render a Template with data

The Render API allows you to render a template with data, using the exact same rendering workflow that Sendwithus uses when delivering your email.
`Strict` is set to `False` as a default, if `Strict=True` this API call will fail on any missing `email_data`.

```python
api.render(
    email_id='YOUR-TEMPLATE-ID',
    email_data={
        'amount': '$12.00'
    },
    locale='fr-FR',
    version_name='French-Version',
    strict=False
)
```

# Batch API

Sendwithus' API has a [batch endpoint](https://support.sendwithus.com/api/#batchapi) that can take multiple requests and execute them concurrently. 
*Note* that Sendwithus recommends keeping batch requests to 10 items or less.

### Creating and Executing a Batch Request

```python
api = sendwithus.api('YOUR-API-KEY')
batch = api.start_batch()

emails = [
    'user+1@example.com',
    'user+2@example.com',
    # ...
    'user+10@example.com'
]

# Generate the batch request
for email in emails:
    batch.send(
        email_id='YOUR-TEMPLATE-ID',
        recipient={
            'address': email
        }
    )

print batch.command_length()  # show number of items in the batch request
results = batch.execute()     # returns a `requests` Response Object
```

# Expected Responses

### Success
```bash
    >>> r.status_code
    200

    >>> r.json().get('success')
    True

    >>> r.json().get('status')
    u'OK'

    >>> r.json().get('receipt_id')
    u'numeric-receipt-id'
```

### Error cases
* malformed request
```bash
    >>> r.status_code
    400
```

* bad API key
```bash
    >>> r.status_code
    403
```

## Run Tests
Use [tox](https://tox.readthedocs.io/en/latest/) to run the tests:

```bash
tox
```

### Testing Multiple Python Versions
This assumes you have [tox](https://tox.readthedocs.io/en/latest/) installed and used
[pyenv](https://github.com/yyuu/pyenv) to install multiple versions of python.

Once all the supported python versions are installed simply run:

```bash
tox
```

This will run the tests against all the versions specified in `tox.ini`.

## Troubleshooting

### General Troubleshooting

-   Enable debug mode
-   Make sure you're using the latest Python client
-   Capture the response data and check your logs &mdash; often this will have the exact error

### Enable Debug Mode

Debug mode prints out the underlying request information as well as the data payload that gets sent to Sendwithus. You will most likely find this information in your logs. To enable it, simply put `DEBUG=True` as a parameter when instantiating the API object. Use the debug mode to compare the data payload getting sent to [Sendwithus' API docs](https://support.sendwithus.com/api "Official Sendwithus API Docs").

```python
import sendwithus
api = sendwithus.api(api_key='YOUR-API-KEY', DEBUG=True)
```
### Response Ranges

Sendwithus' API typically sends responses back in these ranges:

-   2xx – Successful Request
-   4xx – Failed Request (Client error)
-   5xx – Failed Request (Server error)

If you're receiving an error in the 400 response range follow these steps:

-   Double check the data and ID's getting passed to Sendwithus
-   Ensure your API key is correct
-   Log and check the body of the response

### Internal
To package
```bash
  python setup.py sdist bdist_wheel upload
```
