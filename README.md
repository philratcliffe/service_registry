# Simple in memory service registry using Flask 

## Overview
A simple in memory solution using Flask to demo the service registry API.

## Installation
Ensure a Python3 environment
pip install -r requirements.txt

## Running the service
```bash
$ python app.py
```

## Testing
You can run all the Python tests in tests.py using the following command: 

```bash
$ python tests.py
```

You can also run a specific Python test, for example to test the delete
service functionality use the following command:

```bash
$ python tests.py TestServiceRegistry.test_delete_service
```

You can also use curl to investigate and test the service as shown in the
examples below.

### Add a service 
```bash
$ curl -i -H "Content-Type: application/json" -X POST -d '{"service_name":"test2","service_version":"0.0.1"}' http://localhost:5000/services/v1.0
```

### Delete a service 
```bash
$ curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/services/v1.0/test2
```

### List all registered services (N.B. Not in reqs. for development version only)
```bash
$ curl -i http://localhost:5000/services/v1.0
```
## TODO

    - Improve tests
    - Implement Update interface
    - Improve input validation and error handling
    - Add logging
    - Add authentication and run over SSL
    - Use a backend database
    - Improve commenting
    - Add some mechanism for reporting and checking health of services




