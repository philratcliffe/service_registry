#!flask/bin/python
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

SERVICES = {}


# This call is not in the requirements; it is for developement purposes only.
@app.route('/services/v1.0', methods=['GET'])
def list_services():
    """ Retrieves a list of all services. (N.B. FOR DEV VERSION ONLY) """
    return make_response(jsonify({'services': SERVICES}), 200)


@app.route('/services/v1.0', methods=['POST'])
def add_service():
    """ Creates a service.  """
    service_name = request.json['service_name']
    service_version = request.json['service_version']

    key = service_name + service_version
    entry = SERVICES.get(key, {})

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
    return make_response(jsonify({'resp': resp}), 201)

if __name__ == '__main__':
    app.run(debug=True)
