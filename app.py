#!flask/bin/python
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

SERVICES = {}


# This call is not in the requirements; it is for developement purposes only.
@app.route('/services/v1.0', methods=['GET'])
def list_services():
    """
    Retrieves a list of all services. (N.B. FOR DEV VERSION ONLY)
    """
    return make_response(jsonify({'services': SERVICES}), 200)

if __name__ == '__main__':
    app.run(debug=True)
