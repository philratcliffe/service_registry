"""

This module contains the tests for registry service.

"""

import unittest
import requests
import json

import http_status

class TestServiceRegistry(unittest.TestCase):

    def setUp(self):
        """ Populate the service registry. """

        #
        # Add test 0.0.1 (twice)
        #
        headers = {'Content-type': 'application/json'}
        data = {'service_name': 'test', 'service_version': '0.0.1'}
        data_json = json.dumps(data)
        requests.post(
            'http://localhost:5000/services/v1.0',
            data=data_json,
            headers=headers)
        requests.post(
            'http://localhost:5000/services/v1.0',
            data=data_json,
            headers=headers)

        #
        # Add test 0.0.2 (twice)
        #
        headers = {'Content-type': 'application/json'}
        data = {'service_name': 'test', 'service_version': '0.0.2'}
        data_json = json.dumps(data)
        requests.post(
            'http://localhost:5000/services/v1.0',
            data=data_json,
            headers=headers)
        requests.post(
            'http://localhost:5000/services/v1.0',
            data=data_json,
            headers=headers)

        #
        # Add test2 0.0.2 (twice)
        #
        headers = {'Content-type': 'application/json'}
        data = {'service_name': 'test2', 'service_version': '0.0.2'}
        data_json = json.dumps(data)
        requests.post(
            'http://localhost:5000/services/v1.0',
            data=data_json,
            headers=headers)
        requests.post(
            'http://localhost:5000/services/v1.0',
            data=data_json,
            headers=headers)

    def tearDown(self):
        """ Delete services from service registry. """
        requests.delete(
            'http://localhost:5000/services/v1.0/test')
        requests.delete(
            'http://localhost:5000/services/v1.0/test2')


    def test_add_service(self):
        data = {'service_name': 'test', 'service_version': '0.0.1'}
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}

        response = requests.post(
            'http://localhost:5000/services/v1.0',
            data=data_json,
            headers=headers)

        exptected_result = {
            "resp": {
                "service": "test",
                "version": "0.0.1",
                "change": "created",
            }
        }

        self.assertEqual(response.status_code, http_status.CREATED)
        self.assertEqual(response.json(), exptected_result)

    def test_invalid_add_service(self):
        data = {'srvc_nam': 'test', 'service_version': '0.0.1'}
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}

        response = requests.post(
            'http://localhost:5000/services/v1.0',
            data=data_json,
            headers=headers)

        self.assertEqual(response.status_code, http_status.BAD_REQUEST)


    def test_invalid_url(self):
        data = {'service_name': 'test', 'service_version': '0.0.1'}
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}

        response = requests.post(
            'http://localhost:5000/sevices/v1.0',
            data=data_json,
            headers=headers)

        self.assertEqual(response.status_code, http_status.NOT_FOUND)


    def test_delete_service(self):
        response = requests.delete(
            'http://localhost:5000/services/v1.0/test')

        exptected_result = {
            "resp": {
                "change": "removed",
                "service": "test"
            }
        }

        self.assertEqual(response.status_code, http_status.OK)
        self.assertEqual(response.json(), exptected_result)

    def test_find_existing_service_with_version(self):
        response = requests.get('http://localhost:5000/services/v1.0/test2/0.0.2')

        exptected_result = {
            "resp": {
                "service": "test2",
                "version": "0.0.2",
                "count": 2,
            }
        }

        self.assertEqual(response.status_code, http_status.OK)
        self.assertEqual(response.json(), exptected_result)


    def test_find_non_existing_service_with_version(self):
        response = requests.get('http://localhost:5000/services/v1.0/test/0.0.4')

        exptected_result = {
            "resp": {
                "service": "test",
                "version": "0.0.4",
                "count": 0,
            }
        }

        self.assertEqual(response.status_code, http_status.OK)
        self.assertEqual(response.json(), exptected_result)

    def test_find_non_existing_service_without_version(self):
        response = requests.get('http://localhost:5000/services/v1.0/test')

        exptected_result = {
            "resp": {
                "service": "test",
                "count": 4,
                }
        }
        self.assertEqual(response.status_code, http_status.OK)
        self.assertEqual(response.json(), exptected_result)



if __name__ == "__main__":
    unittest.main()
