#!flask/bin/python
"""

This is the main module for the registry service.  It uses a Flask and a
simple in memory solution to demo the restful API.

"""

import http_status
from flask import Flask, jsonify, request, make_response, abort

app = Flask(__name__)

SERVICES = {}


@app.errorhandler(http_status.NOT_FOUND)
def not_found(error):
    return make_response(
        jsonify({
            'error': 'Not found'
        }), http_status.NOT_FOUND)


# NOTE: This is not in the requirements; it is for developement purposes only.
@app.route('/services/v1.0', methods=['GET'])
def list_services():
    """Retrieves a list of all services. (N.B. FOR DEV VERSION ONLY)"""
    return make_response(jsonify({'services': SERVICES}), http_status.OK)


@app.route('/services/v1.0', methods=['POST'])
def add_service():
    """Creates a service."""
    if not request.json \
        or not 'service_name' in request.json \
        or not 'service_version' in request.json:
        abort(http_status.BAD_REQUEST)

    service_name = request.json['service_name']
    service_version = request.json['service_version']

    key = get_key(service_name, service_version)
    entry = get_entry(key)

    if entry:
        entry['count'] += 1
    else:
        entry = {
            'service': service_name,
            'version': service_version,
            'count': 1,
        }
        SERVICES[key] = entry

    resp = dict(entry)
    resp['change'] = "created"
    resp.pop('count', None)
    return make_response(jsonify({'resp': resp}), http_status.CREATED)


@app.route('/services/v1.0/<service_name>', methods=['DELETE'])
def delete_service(service_name):
    """ Deletes a service. """
    resp, http_return_status = delete_service_records(service_name)
    return make_response(jsonify({'resp': resp}), http_return_status)


@app.route(
    '/services/v1.0/<service_name>',
    defaults={'service_version': None},
    methods=['GET'])
@app.route('/services/v1.0/<service_name>/<service_version>', methods=['GET'])
def find_service(service_name, service_version):
    """
    Retrieves a service using the service name and optionally a version.
    """
    if service_version:
        resp = find_service_with_version(service_name, service_version)
        return make_response(jsonify({'resp': resp}), http_status.OK)

    resp = find_service_without_version(service_name)
    return make_response(jsonify({'resp': resp}), http_status.OK)


@app.route('/services/v1.0/<service_name>', methods=['PUT'])
def update_service():
    """
    Update a service.
    """
    # TODO
    return make_response(jsonify({}), http_status.NOT_IMPLEMENTED)


def find_service_with_version(service_name, service_version):
    key = get_key(service_name, service_version)
    if key in SERVICES:
        return SERVICES[key]
    else:
        return {
            'service': service_name,
            'version': service_version,
            'count': 0
        }


def find_service_without_version(service_name):
    resp = {'service': service_name, 'count': 0}
    print(SERVICES)
    for k, v in SERVICES.items():
        if v['service'] == service_name:
            resp['count'] += v['count']

    return resp


def delete_service_records(service_name):
    keys_to_delete = []
    for k, v in SERVICES.items():
        if v['service'] == service_name:
            keys_to_delete.append(get_key(v['service'], v['version']))

    service_deleted = False
    for key in keys_to_delete:
        del SERVICES[key]
        service_deleted = True

    resp = {}
    http_return_status = http_status.OK
    resp['service'] = service_name

    if service_deleted:
        resp['change'] = 'removed'
    else:
        resp['change'] = 'notfound'
        http_return_status = http_status.NOT_FOUND

    return resp, http_return_status


def get_entry(key):
    return SERVICES.get(key, {})


def get_key(service, version):
    return service + '-v' + version


def delete_service_records(service_name):
    keys_to_delete = []
    for k, v in SERVICES.items():
        if v['service'] == service_name:
            keys_to_delete.append(get_key(v['service'], v['version']))

    service_deleted = False
    for key in keys_to_delete:
        del SERVICES[key]
        service_deleted = True

    resp = {}
    http_return_status = http_status.OK
    resp['service'] = service_name

    if service_deleted:
        resp['change'] = 'removed'
    else:
        resp['change'] = 'notfound'
        http_return_status = http_status.NOT_FOUND

    return resp, http_return_status


def get_entry(key):
    return SERVICES.get(key, {})


def get_key(service, version):
    return service + '-v' + version


if __name__ == '__main__':
    app.run(debug=True)
