sendwithus python-client
========================

## status
BETA - this client implements v1_0 of SWU API and is functional and tested

## requirements
python requests library

## installation
	pip install sendwithus

## to run tests
	python setup.py test 

## usage

### Call with REQUIRED parameters only
	>>> import sendwithus
	>>> api = sendwithus.api(api_key='YOUR-API-KEY')
	>>> r = api.send(
	        email_id='YOUR-EMAIL-ID',
	        recipient={'address': 'us@sendwithus.com'},
	        email_data={ 'first_name': 'Matt' })
	>>> r.status_code
	200

### Request with REQUIRED and OPTIONAL parameters
	>>> import sendwithus
	>>> api = sendwithus.api(api_key='YOUR-API-KEY')
	>>> r = api.send(
			email_id='YOUR-EMAIL-ID',
			recipient={ 'name': 'Matt',
						'address': 'us@sendwithus.com'},
			email_data={ 'first_name': 'Matt' },
			sender={ 'name': 'Company',
					 'address':'company@company.com',
					 'reply_to':'info@company.com'})
	>>> r.status_code
	200

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
        python setup.py sdist bdist_wininst upload

