sendwithus python-client
========================

## status
BETA - this client implements v1_0 of SWU API and is functional and tested

[![Build Status](https://travis-ci.org/sendwithus/sendwithus_python.png)](https://travis-ci.org/sendwithus/sendwithus_python)

## requirements
python requests library

## installation
	pip install sendwithus

## to run tests
	python setup.py test 

## usage

For all examples, assume:
```python
import sendwithus
api = sendwithus.api(api_key='YOUR-API-KEY')
```

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

* email_id not found

	    >>> r.status_code
	    404

### packaging (internal)
        python setup.py sdist upload

