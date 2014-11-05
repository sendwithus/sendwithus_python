sendwithus python-client
========================

[![Build Status](https://travis-ci.org/sendwithus/sendwithus_python.png)](https://travis-ci.org/sendwithus/sendwithus_python)

## requirements
python requests library

## installation
    pip install sendwithus

## usage

For all examples, assume:
```python
import sendwithus
api = sendwithus.api(api_key='YOUR-API-KEY')
```

# Templates

## Get your templates

```python
api.templates()
```

## Create a template

```python
api.create_template(
    name='Email Name',
    subject='Email Subject',
    html='<html><head></head><body>Valid HTML</body></html>',
    text='Optional text content')
```

We validate all HTML and will return an error if it's invalid.

```python
r.status_code
# 400
r.content
# 'email html failed to validate'
```

# Send

### Call with REQUIRED parameters only
The `email_data` field is optional, but highly recommended!

```python
r = api.send(
    email_id='YOUR-EMAIL-ID',
    recipient={'address': 'us@sendwithus.com'})
print r.status_code
# 200
```

### Call with REQUIRED parameters and email_data
```python
r = api.send(
    email_id='YOUR-EMAIL-ID',
    recipient={'address': 'us@sendwithus.com'},
    email_data={ 'first_name': 'Matt' })
print r.status_code
# 200
```

### Optional Sender
The `sender['address']` is a required sender field

```python
r = api.send(
    email_id='YOUR-EMAIL-ID',
    recipient={ 'name': 'Matt',
                'address': 'us@sendwithus.com'},
    email_data={ 'first_name': 'Matt' },
    sender={ 'address':'company@company.com' })
print r.status_code
# 200
```

### Optional Sender with reply_to address
`sender['name']` and `sender['reply_to']` are both optional

```python
r = api.send(
    email_id='YOUR-EMAIL-ID',
    recipient={ 'name': 'Matt',
                'address': 'us@sendwithus.com'},
    email_data={ 'first_name': 'Matt' },
    sender={ 'name': 'Company',
                'address':'company@company.com',
                'reply_to':'info@company.com'})
print r.status_code
# 200
```

### Optional CC

```python
r = api.send(
    email_id='YOUR-EMAIL-ID',
    recipient={'name': 'Matt',
                'address': 'us@sendwithus.com'},
    cc=[
        {'address': 'company@company.com'},
        {'address': 'info@company.com'}
    ])
print r.status_code
# 200
```

### Optional BCC

```python
r = api.send(
    email_id='YOUR-EMAIL-ID',
    recipient={'name': 'Matt',
                'address': 'us@sendwithus.com'},
    bcc=[
        {'address': 'company@company.com'},
        {'address': 'info@company.com'}
    ])
print r.status_code
# 200
```

### Optional ESP Account

```python
r = api.send(
    email_id='YOUR-EMAIL-ID',
    recipient={'name': 'Matt',
                'address': 'us@sendwithus.com'},
    esp_account='esp_1234asdf1234')
print r.status_code
# 200
```

### Optional File Attachments

```python
r = api.send(
    email_id='YOUR-EMAIL-ID',
    recipient={'name': 'Matt',
               'address': 'us@sendwithus.com'},
    files=[open('/home/Matt/report1.txt', 'r'), open('/home/Matt/report2.txt', 'r')])
print r.status_code
# 200
```

# Drip Campaigns

## List all drip campaigns

List all drip campaigns for the current profile

```python
api.list_drip_campaigns()
```

## Start a customer on a drip campaign

Starts a customer on the first step of a specified drip campaign

```python
api.start_on_drip_campaign('customer@email.com', 'dc_1234asdf1234')
```

### Extra Data

You may specify extra data to be merged into the templates in the drip campaign

```python
api.start_on_drip_campaign('customer@email.com', 'dc_1234asdf1234', email_data={'color': 'blue'})
```

## Remove a customer from a drip campaign

Deactivates all pending emails for a customer on a specified drip campaign

```python
api.remove_from_drip_campaign('customer@email.com', 'dc_1234asdf1234')
```

## Remove a customer from all drip campaigns

You can deactivate all pending drip campaign emails for a customer

```python
api.drip_deactivate('customer@example.com')
```

## List the details of a specific campaign

```python
api.drip_campaign_details('dc_1234asdf1234')
```

# Customers

## Create/update Customer

You can use the same endpoint to create or update a customer. Sendwithus
will peform a merge of the data on the customer profile, preferring the new data.

```python
api.customer_create('customer@example.com', data={'first_name': 'Matt'})
```


## Delete a Customer

```python
api.customer_delete('customer@example.com')
```

# Segmentation

## Send Template to Segment

You can use the Segments api to send a template to all customers who match a
segment. The Segment must be created in the Sendwithus dashboard, which is
where you will find the `segment_id` for use in this api.

```python
api.send_segment('tem_12345', 'seg_1245')
```

### Extra Data

You may specify extra data to be merged into the template, alongside the
individual customer profiles

```python
api.send_segment('tem_12345', 'seg_12345', email_data={'color': 'blue'})
```

# Render

## Render a Template with data

The render api allows you to render a template with data, using the exact same rendering workflow that Sendwithus uses when delivering your email.

```python
api.render('tem_12345', { "amount": "$12.00" })
```

## expected response

### Success
    >>> r.status_code
    200

    >>> r.json().get('success')
    True

    >>> r.json().get('status')
    u'OK'

    >>> r.json().get('receipt_id')
    u'numeric-receipt-id'

### Error cases
* malformed request

        >>> r.status_code
        400

* bad api key

        >>> r.status_code
            403

## to run tests
    python setup.py test

### packaging (internal)
        python setup.py sdist upload

